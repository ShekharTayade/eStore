from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse

from datetime import datetime
import datetime
import json
import os

from eStore.models import Ecom_site, User_image, Print_medium, Promotion_frame, Cart_item

from .frame_views import *
from .image_views import *

from eStore.forms import User_imageForm
from PIL import ExifTags

today = datetime.date.today()

def user_image(request):

	# get mouldings
	mouldings = get_mouldings(request)
	# defaul we send is for PAPER
	paper_mouldings_apply = mouldings['paper_mouldings_apply']
	paper_mouldings_show = mouldings['paper_mouldings_show']

	
	# get mounts
	mounts = get_mounts(request)

	# get arylics
	acrylics = get_acrylics(request)

	# get boards
	boards = get_boards(request)

	# get Stretches
	stretches = get_stretches(request)

	printmedium = Print_medium.objects.all()

	
	if request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		user_instance = User_image.objects.filter(user = user, status = "INI").first()
	else:
		session_id = request.session.session_key
		user_instance = User_image.objects.filter(session_id = session_id, status = "INI").first()

	# If user uploaded image is not found then display the default image in frames
	if not user_instance:
		user_instance = User_image.objects.filter(status = "DEF").first()		

	return render(request, "eStore/user_image.html", {'mounts':mounts,
			'mouldings_appply':paper_mouldings_apply, 
			'mouldings_show':paper_mouldings_show, 'mounts':mounts,
			'printmedium':printmedium, 'user_instance':user_instance,
			'acrylics':acrylics, 'boards':boards, 'stretches':stretches,			
			})


@csrf_exempt
def upload_user_image(request):
	
	if request.method == 'POST':
	
		file = request.FILES.get('file')
		session_id = request.session.session_key
		user = None
		
		if request.user.is_authenticated:
			try:
				user = User.objects.get(username = request.user)
				user_instance = User_image.objects.filter(user = user, status = "INI").first()
			except User.DoesNotExist:
				user = None
		else:
			if session_id is None:
				request.session.create()
				session_id = request.session.session_key
			user_instance = User_image.objects.filter(session_id = session_id, status = "INI").first()

		if user_instance :
			user_img = User_image(
				id = user_instance.id,
				user = user_instance.user,
				image_to_frame = file,
				session_id = session_id,
				created_date = user_instance.created_date,
				status = user_instance.status
			)
			user_img.save()
		else :
			user_img = User_image(
				user = user,
				session_id = session_id,
				image_to_frame = file,
				status = 'INI'
			)
			user_img.save()

		# Read the image
		im=Image.open(user_img.image_to_frame)
		
		# Rotate image, if orientation is not 1
		exifData = {}
		exif_data = im._getexif()
		if exif_data:
			for tag, value in exif_data.items():
				decodedTag = ExifTags.TAGS.get(tag, tag)
				exifData[decodedTag] = value		
				
			print('Orientation')
			print(exifData['Orientation'])
		
			if exifData :
				if exifData['Orientation'] == 6:
					im.rotate(90)
				if exifData['Orientation'] == 3:
					im.rotate(180)
				if exifData['Orientation'] == 8:
					im.rotate(270)
			
		buffered = BytesIO()
		im.save(buffered, format='JPEG')
		img_data = buffered.getvalue()
		img_str = base64.b64encode(img_data)
					
		return HttpResponse(img_str)			

	else :
		return ({'msg':'FAILURE'})


		

def show_mouldings_for_user_image(request):

	print_medium = request.GET.get('print_medium', '')

	if print_medium == '' or print_medium == '0':
		return

	if not request.is_ajax():
		return

	# get mouldings
	mouldings = get_mouldings(request)
	
	if print_medium == "CANVAS":
		mouldings_apply = mouldings['canvas_mouldings_apply']
		mouldings_show = mouldings['canvas_mouldings_show']
	if print_medium == "PAPER":
		mouldings_apply = mouldings['paper_mouldings_apply']
		mouldings_show = mouldings['paper_mouldings_show']
		

	session_id = request.session.session_key
	
	if request.user.is_authenticated:
		try:
			user = User.objects.get(username = request.user)
			user_instance = User_image.objects.filter(user = user, status = "INI").first()
		except User.DoesNotExist:
			user = None
	else:
		if session_id is None:
			request.session.create()
			session_id = request.session.session_key
		user_instance = User_image.objects.filter(session_id = session_id, status = "INI").first()

	# If user uploaded image is not found then display the default image in frames
	if not user_instance:
		user_instance = User_image.objects.filter(status = "DEF").first()
		
	
	return render(request, "eStore/mouldings_include_for_user_image.html", {
		'mouldings_apply':mouldings_apply, 'mouldings_show':mouldings_show,
		'user_instance':user_instance} )




@csrf_exempt	
def get_user_item_price (request):

	item_price = 0
	img_height = 0
	img_width = 0
	print_medium_size = 0 
	acrylic_size = 0
	moulding_size= 0
	mount_size = 0
	board_size = 0 
	stretch_size = 0
	print_medium_id = ''
	acrylic_id = 0
	moulding_id = 0
	mount_id = 0
	board_id = 0
	stretch_id = 0
	prod_id = 0

	msg = ""

	# Get data from the request.
	json_data = json.loads(request.body.decode("utf-8"))

	major_array = []
	sub_array = []
	for majorkey, subdict in json_data.items():
		for subkey, value in subdict.items():
			
			# Get image height and width
			if majorkey.upper().strip() == "IMAGE":
				if subkey == "HEIGHT":
					img_height = value
				if subkey == "WIDTH":
					img_width = value

			# Get print medium
			if majorkey.upper().strip() == "PRINT_MEDIUM":
				if subkey == "ID":
					print_medium_id = value
				if subkey == "SIZE":
					print_medium_size = value
					

			# Get acrylic
			if majorkey.upper().strip() == "ACRYLIC":
				if subkey == "ID":
					acrylic_id = value
				if subkey == "SIZE":
					acrylic_size = value

			# Get moulding
			if majorkey.upper().strip() == "MOULDING":
				if subkey == "ID":
					moulding_id = value
				if subkey == "SIZE":
					moulding_size = value

			# Get Mount
			if majorkey.upper().strip() == "MOUNT":
				if subkey == "ID":
					mount_id = value
				if subkey == "SIZE":
					mount_size = value
					
			# Get Board
			if majorkey.upper().strip() == "BOARD":
				if subkey == "ID":
					board_id = value
				if subkey == "SIZE":
					baord_size = value

			# Get Stretch
			if majorkey.upper().strip() == "STRETCH":
				if subkey == "ID":
					stretch_id = value
				if subkey == "SIZE":
					stretch_size = value
					
	# Get image price on paper and canvas
	per_sqinch_price = get_per_sqinch_printing_price()
	per_sqinch_paper = per_sqinch_price['per_sqin_paper']
	per_sqinch_canvas = per_sqinch_price['per_sqin_canvas']
					
	# Image Price
	if img_width > 0 and img_height > 0:
		msg = ""
	else :
		msg = "ERROR-Image size missing"
	
	# Get the Item Price
	if print_medium_id == "PAPER":
		# Image price
		image_price = img_width * img_height * per_sqinch_paper
		item_price = item_price + image_price

		print( "Width: " + str(img_width) )
		print( "height: " + str(img_height) )
		print( "Image Price: " + str(image_price) )
		
		# Acrylic Price		
		acrylic_price = img_width * img_height * get_acrylic_price_by_id(acrylic_id)
		item_price = item_price + acrylic_price
		print( "Acrylic Price: " + str(acrylic_price))
		
		# Moulding price
		moulding_price = (img_width + img_height) * 2 * get_moulding_price_by_id(moulding_id)
		item_price = item_price + moulding_price
		print( "Moulding Price: " + str(moulding_price))
		
		# Mount price
		mount_price = ((img_width + img_height) * 2 * mount_size)  * get_mount_price_by_id(mount_id)
		item_price = item_price + Decimal(mount_price)
		print( "Mount Price: " + str(mount_price))
		
		# Board price
		board_price = img_width * img_height * get_board_price_by_id(board_id)
		item_price = item_price + board_price
		print( "Board Price: " + str(board_price))

		print( "======================")
		print( "Total Item Price: " + str(item_price))
		
		
	elif print_medium_id == "CANVAS":

		# Image price
		image_price = img_width * img_height * per_sqinch_canvas
		item_price = item_price + image_price
		print( "Image Price: " + str(image_price))

		# Moulding price
		moulding_price = (img_width + img_height) * 2 * get_moulding_price_by_id(moulding_id)
		item_price = item_price + moulding_price
		print( "Moulding Price: " + str(moulding_price))
		
		# Stretch price
		stretch_price = img_width * img_height * get_stretch_price_by_id(stretch_id)
		item_price = item_price + stretch_price
		print( "Stretch Price: " + str(stretch_price))

		print( "======================")
		print( "Total Item Price: " + str(item_price))

	
	item_price_withoutdisc = round(item_price)
	
	disc_applied = False
	promo = get_frame_promotion(moulding_id)
	print(promo)
		
	disc_amt = 0
	cash_disc = 0
	if promo:
		cash_disc = round(promo['cash_disc'])
		percent_disc = promo['percent_disc']	
		promotion_id = promo['promotion_id']
	else:
		cash_disc = 0
		percent_disc = 0	
		promotion_id = ''
	
	if cash_disc > 0:
		item_price = item_price - cash_disc
		disc_applied = True
		disc_amt = round(cash_disc)
	elif percent_disc > 0:
		disc_amt = round(item_price * percent_disc / 100)
		item_price = item_price - disc_amt
		disc_applied = True
		
	item_price = round(item_price)

	print( "======================")
	print( "Disc Amt: " + str(disc_amt))
	print( "Item Price: " + str(item_price))

	return JsonResponse({"msg":msg, "item_price" : item_price, 'cash_disc':cash_disc,
				'percent_disc':percent_disc, 'item_unit_price':item_price_withoutdisc,
				'disc_amt':disc_amt, 'disc_applied':disc_applied, 'promotion_id':promotion_id})


def get_per_sqinch_printing_price():

	per_sqin_paper = 2
	per_sqin_canvas = 3
	 
	return ({'per_sqin_paper':per_sqin_paper, 'per_sqin_canvas' : per_sqin_canvas})



def get_frame_promotion(moulding_id):
	cash_disc = 0
	percent_disc = 0	
	promotion_id = 0

	# Product promotions #	
	promo_frame = Promotion_frame.objects.filter(moulding_id = moulding_id,
			frame_promotion__effective_from__lte = today, 
			frame_promotion__effective_to__gte = today).select_related('frame_promotion').first()

	cash_disc = 0
	percent_disc = 0
	promo_id = None
		
	
	if promo_frame:
		if promo_frame.frame_promotion.discount_type == "CASH":
			cash_disc = promo_frame.frame_promotion.discount_value
		if promo_frame.frame_promotion.discount_type == "PERCENTAGE":
			percent_disc = promo_frame.frame_promotion.discount_value
		promotion_id = promo_frame.frame_promotion_id

		
	return ({'promotion_id':promotion_id, 'cash_disc':cash_disc, 'percent_disc':percent_disc})

	
@csrf_exempt	
def get_user_image_id(request):


	if request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		user_instance = User_image.objects.filter(user = user, status = "INI").first()
	else:
		session_id = request.session.session_key
		user_instance = User_image.objects.filter(session_id = session_id, status = "INI").first()

	user_image_id = 0
	if user_instance:
		user_image_id = user_instance.id
	
	print("USER IMAGE ID============" + str(user_image_id) )
	
	return JsonResponse({'user_image_id':user_image_id})
	

	
@csrf_exempt	
def get_user_item_price_by_cart_item (cart_item_id):

	item_price = 0
	img_height = 0
	img_width = 0
	stretch_id = 0
	image_price = 0
	moulding_price = 0
	acrylic_price = 0
	mount_price = 0
	stretch_price = 0
	board_price = 0
	
	msg = ""
	
	# Get prod data.
	cart_item = Cart_item.objects.filter(cart_item_id = cart_item_id).first()
	
					
	# Get image price on paper and canvas
	per_sqinch_price = get_per_sqinch_printing_price()
	per_sqinch_paper = per_sqinch_price['per_sqin_paper']
	per_sqinch_canvas = per_sqinch_price['per_sqin_canvas']
					
	# Image Price
	if cart_item.image_width > 0 and cart_item.image_height > 0:
		msg = ""
	else :
		msg = "ERROR-Image size missing"
	
	# Get the Item Price
	if cart_item.print_medium_id == "PAPER":
		# Image price
		image_price = cart_item.image_width * cart_item.image_height * per_sqinch_paper
		item_price = item_price + image_price
		print( "Width: " + str(cart_item.image_width) )
		print( "height: " + str(cart_item.image_height) )
		print( "Image Price: " + str(image_price) )
		
		# Acrylic Price		
		if cart_item.acrylic_id:
			acrylic_price = cart_item.image_width * cart_item.image_height * get_acrylic_price_by_id(cart_item.acrylic_id)
			item_price = item_price + acrylic_price
		print( "Acrylic Price: " + str(acrylic_price))
		
		# Moulding price
		if cart_item.moulding_id:
			moulding_price = (cart_item.image_width + cart_item.image_height) * 2 * get_moulding_price_by_id(cart_item.moulding_id)
			item_price = item_price + moulding_price
		print( "Moulding Price: " + str(moulding_price))
		
		# Mount price
		if cart_item.mount_id:
			mount_price = Decimal( ((cart_item.image_width + cart_item.image_height) * 2 * cart_item.mount_size) ) * get_mount_price_by_id(cart_item.mount_id)
			item_price = item_price + mount_price
		print( "Mount Price: " + str(mount_price))
		
		# Board price
		board_price = cart_item.image_width * cart_item.image_height * get_board_price_by_id(cart_item.board_id)
		item_price = item_price + board_price
		print( "Board Price: " + str(board_price))
		
		print( "======================")
		print( "Total Item Price: " + str(item_price))
		
		
		
	elif cart_item.print_medium_id == "CANVAS":

		# Image price
		image_price = cart_item.image_width * cart_item.image_height * per_sqinch_canvas
		item_price = item_price + image_price
		print( "Image Price: " + str(image_price))

		# Moulding price
		if cart_item.moulding_id:
			moulding_price = (cart_item.image_width + cart_item.image_height) * 2 * get_moulding_price_by_id(cart_item.moulding_id)
			item_price = item_price + moulding_price
		print( "Moulding Price: " + str(moulding_price))
		
		# Stretch price
		if cart_item.stretch_id:
			stretch_price = cart_item.image_width * cart_item.image_height * get_stretch_price_by_id(cart_item.stretch_id)
			item_price = item_price + stretch_price
	
		print( "Stretch Price: " + str(stretch_price))

		print( "======================")
		print( "Total Price: " + str(item_price))

	
	item_price_withoutdisc = item_price
	disc_applied = False
	promo = get_frame_promotion(cart_item.moulding_id)
	print(promo)
		
	disc_amt = 0
	if promo:
		cash_disc = promo['cash_disc']
		percent_disc = promo['percent_disc']	
		promotion_id = promo['promotion_id']
	else:
		cash_disc = 0
		percent_disc = 0	
		promotion_id = ''
	
	if cash_disc > 0:
		item_price = item_price - cash_disc
		disc_applied = True
		disc_amt = cash_disc
	elif percent_disc > 0:
		disc_amt = item_price * percent_disc / 100
		item_price = item_price - ( disc_amt )
		disc_applied = True
		
	item_price = round(item_price)

	print( "======================")
	print( "Disc Amt: " + str(disc_amt))
	print( "Item Price: " + str(item_price))


	return ({"msg":msg, "item_price" : item_price, 'image_price':image_price, 'cash_disc':cash_disc,
				'percent_disc':percent_disc, 'item_unit_price':item_price_withoutdisc,
				'disc_amt':disc_amt, 'disc_applied':disc_applied, 'promotion_id':promotion_id})
	