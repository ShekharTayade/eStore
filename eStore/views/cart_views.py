from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import IntegrityError, DatabaseError, Error
from django.contrib.auth.models import User

from datetime import datetime
import datetime
from decimal import Decimal
import json

from eStore.models import Ecom_site, Main_slider, New_arrival, Promotion, Menu, Product_category
from eStore.models import New_arrival_images, Promotion_images, Product, User_image, Frame_promotion
from eStore.models import Cart, Cart_item, Tax, Order, Order_items, Voucher_user, Voucher
from eStore.models import Menu
from .frame_views import *
from .image_views import *
from .product_views import *
from .tax_views import *
from .user_image_views import *

today = datetime.date.today()
ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

@csrf_protect
@csrf_exempt
def add_to_cart(request):
	prod_id = request.POST.get('prod_id', '')
	user_image_id = request.POST.get('user_image_id', '')
	qty = int(request.POST.get('qty', '0'))

	image_width = Decimal(request.POST.get('image_width', '0'))
	image_height = Decimal(request.POST.get('image_height', '0'))
	
	sqin = image_width * image_height
	rnin = (image_width + image_height) * 2
	
	moulding_id = request.POST.get('moulding_id', '')
	if moulding_id == '0' or moulding_id == 'None':
		moulding_id = None

	#moulding_size = Decimal(request.POST.get('moulding_size', '0'))
	if moulding_id:
		moulding_size = rnin
	else: 
		moulding_size = None
	print_medium_id = request.POST.get('print_medium_id', '')
	print_medium_size = Decimal(request.POST.get('print_medium_size', '0'))
	mount_id = request.POST.get('mount_id', '0')
	if mount_id == '0' or mount_id == 'None':
		mount_id = None
	if mount_id:
		mount_size = Decimal(request.POST.get('mount_size', '0'))
		mount_w_left = Decimal(request.POST.get('mount_w_left', '0'))
		mount_w_right = Decimal(request.POST.get('mount_w_right', '0'))
		mount_w_left = Decimal(request.POST.get('mount_w_top', '0'))
		mount_w_left = Decimal(request.POST.get('mount_w_bottom', '0'))
	else:
		mount_size = None
		mount_w_left = None
		mount_w_right = None
		mount_w_top = None
		mount_w_bottom = None
	acrylic_id = request.POST.get('acrylic_id', '0')
	if acrylic_id == '0' or acrylic_id == 'None':
		acrylic_id = None
	if acrylic_id:
		#acrylic_size = Decimal(request.POST.get('acrylic_size', '0'))
		acrylic_size = sqin
	else:
		acrylic_size = None
	
	board_id = request.POST.get('board_id', '')
	if board_id == '0' or board_id == 'None':
		board_id = None
	if board_id:
		#board_size = Decimal(request.POST.get('board_size', '0'))
		board_size = sqin
	else:
		board_size = None

	stretch_id = request.POST.get('stretch_id', '0')
	if stretch_id == '0' or stretch_id == 'None':
		stretch_id = None
	if stretch_id:
		#stretch_size = Decimal(request.POST.get('stretch_size', '0'))
		stretch_size = rnin
	else:
		stretch_size = None
	
	str_item_unit_price = request.POST.get('item_unit_price', '0')
	if str_item_unit_price == '':
		str_item_unit_price = '0'
	item_unit_price = Decimal(str_item_unit_price)
	
	str_total_price = request.POST.get('total_price', '0')
	if str_total_price == '':
		str_total_price = 0
	total_price = Decimal(str_total_price)
	
	str_disc_amt = request.POST.get('disc_amt', '0')
	if str_disc_amt == '':
		str_disc_amt = 0
	disc_amt = Decimal(str_disc_amt)

	
	userid = None


	discount = request.POST.get('discount', '')

	promo_str = request.POST.get('promotion_id', '0')

	if promo_str == '':
		promo_str = '0'
	promo_id = int(promo_str)
	
	# Get the product or User Image
	prod = None
	user_image = None
	
	try:
		if prod_id != '':
			prod = Product.objects.get(product_id=prod_id)
		else :
			if request.user.is_authenticated:
				user = User.objects.get(username = request.user)
				user_image = User_image.objects.filter(user = user, status = "INI").first()
			else:
				session_id = request.session.session_key
				user_image = User_image.objects.filter(session_id = session_id, status = "INI").first()		
		
	except Product.DoesNotExist:
		msg = "Product " + prod_id + " does not exist"
		return( JsonResponse({'msg':msg, 'cart_qty':qty}, safe=False) )
	except User_image.DoesNotExist:
		msg = "Couldn't find the uploaded image. Pease try again."
		return( JsonResponse({'msg':msg, 'cart_qty':qty}, safe=False) )

		
	# TAX Calculations
	item_tax = 0
	item_sub_total = 0
	taxes = get_taxes()
	#if product exists then it's an image tax
	if prod :
		tax_rate = taxes['image_tax_rate']
	else :
		tax_rate = taxes['moulding_tax_rate']
	
	# Calculate tax and sub_total
	item_sub_total = round( total_price / (1 + (tax_rate/100)), 2 )
	item_tax = total_price - item_sub_total
	#############################################################

	promo = {}
	promo['cash_disc']= 0
	promo['percent_disc'] = 0
	# Get any discount on the product
	if prod:
		promo = get_product_promotion(prod_id)
	if user_image:
		promo = get_frame_promotion(moulding_id)
	#promo_id = promo['promotion_id'] ### To be taken from the input to this function, so the promo code flows here
	cash_disc = promo['cash_disc']
	percent_disc = promo['percent_disc']
	
	# get Promotion object for adding it in the cart item
	p_promotion = None
	f_promotion = None
	if promo :
		if prod:
			p_promotion = Promotion.objects.filter(promotion_id = promo_id).first()
		if user_image:
			promo_id = promo['promotion_id']
			f_promotion = Frame_promotion.objects.filter(promotion_id = promo_id).first()
	
	
	#################################################################################
	##	total_price contains the price after promotion discounts. The promotion
	##  details obtained above are only for the purpose of saving it into the tables 
	#################################################################################
		
	msg = "Success"
	cart_exists = False
	usercart = {}
	cart_qty = 0
	''' Let's check if the user has a cart open '''
	
	sessionid = request.session.session_key
	if request.user.is_authenticated:
		try:
			userid = User.objects.get(username = request.user)
			usercart = Cart.objects.get(user_id = userid, cart_status = "AC") 
			#cart.objects.filter(user_id = userid)[:1]
		except Cart.DoesNotExist:
			usercart = {}
			cart_exists = False
			
		if usercart:
			cart_exists = True
		else:
			cart_exists = False
	else:
		if sessionid is None:
			request.session.create()
			sessionid = request.session.session_key
			cart_exists = False
		 
		else:
			try:
				# Get usercart by session
				usercart = Cart.objects.get(session_id = sessionid, cart_status="AC")
				#cart.objects.filter(session_id = sessionid)[:1]
			except Cart.DoesNotExist:
				usercart = {}
				cart_exists = False
			
			if usercart:
				cart_exists = True
			else:
				cart_exists = False;

	if cart_exists:

		''' Check if product or user image exists in cart '''
		cart_prods = {}
		cart_user_images = {}
		if prod:
			cart_prods = Cart_item.objects.filter(cart_id = usercart.cart_id, 
						product_id = prod_id, moulding_id = moulding_id,
						print_medium_id = print_medium_id, mount_id = mount_id,
						mount_size = mount_size, acrylic_id = acrylic_id,
						board_id = board_id, stretch_id = stretch_id ).first()
		if user_image:
			cart_user_images = Cart_item.objects.filter(cart_id = usercart.cart_id, 
						user_image_id = user_image_id, moulding_id = moulding_id,
						print_medium_id = print_medium_id, mount_id = mount_id,
						mount_size = mount_size, acrylic_id = acrylic_id,
						board_id = board_id, stretch_id = stretch_id ).first()
		

		prod_exits_in_cart = False 

		if cart_prods or cart_user_images:
			
			prod_exits_in_cart = True
	
		try :
			
			#Update the existing cart
			newusercart = Cart(
				cart_id = usercart.cart_id,
				store = ecom,
				user = userid,
				cart_sub_total = usercart.cart_sub_total + item_sub_total,
				cart_disc_amt = usercart.cart_disc_amt + disc_amt,
				cart_tax  = usercart.cart_tax + item_tax,
				cart_total = Decimal(usercart.cart_total) + (total_price),
				session_id = sessionid,
				quantity =  usercart.quantity + qty,
				voucher_id = usercart.voucher_id,
				voucher_disc_amount = usercart.voucher_disc_amount,
				updated_date = today,
				cart_status = usercart.cart_status
			)

			newusercart.save()
			
			''' If the product with same moulding, print_medium etc. already exists in the cart items, then update it, else insert new item '''
			if prod_exits_in_cart:
				usercartitems = Cart_item(
					cart_item_id = cart_prods.cart_item_id,
					cart = usercart,
					product_id = cart_prods.product_id,
					user_image = cart_prods.user_image,
					promotion = cart_prods.promotion,
					frame_promotion = cart_prods.frame_promotion,
					quantity = cart_prods.quantity + qty,
					item_unit_price = item_unit_price,
					item_sub_total = cart_prods.item_sub_total + item_sub_total,
					item_disc_amt = cart_prods.item_disc_amt + disc_amt,
					item_tax  = cart_prods.item_tax + item_tax,
					item_total = cart_prods.item_total + total_price,
					moulding_id = moulding_id,
					moulding_size =  mount_size,
					print_medium_id = print_medium_id,
					print_medium_size = print_medium_size,
					mount_id = mount_id,
					mount_size = mount_size,
					board_id =  board_id,
					board_size = board_size,
					acrylic_id = acrylic_id,
					acrylic_size = acrylic_size,
					stretch_id = stretch_id,
					stretch_size = stretch_size,
					image_width = image_width,
					image_height = image_height,
					updated_date =  today
					
				)
				usercartitems.save()
			else:
				# add new product in the cart
				if prod:
					usercartitems = Cart_item(
						cart = usercart,
						product_id = prod_id,
						user_image = user_image,
						promotion = p_promotion,
						frame_promotion = f_promotion,
						quantity = qty,
						item_unit_price = item_unit_price,
						item_sub_total = item_sub_total,
						item_tax  = item_tax,
						item_disc_amt = disc_amt,
						item_total = total_price,
						print_medium_id = print_medium_id,
						print_medium_size = print_medium_size,
						moulding_id = moulding_id,
						moulding_size = moulding_size,
						mount_id = mount_id,
						mount_size = mount_size,
						acrylic_id = acrylic_id,
						acrylic_size = acrylic_size,
						stretch_id = stretch_id,
						stretch_size = stretch_size,
						board_id = board_id,
						board_size = board_size,
						image_width = image_width,
						image_height = image_height,
						updated_date = today
					)
				elif user_image:
					usercartitems = Cart_item(
						cart = usercart,
						product_id = prod_id,
						user_image = user_image,
						promotion = p_promotion,
						frame_promotion = f_promotion,
						quantity = qty,
						item_unit_price = item_unit_price,
						item_sub_total = item_sub_total,
						item_tax  = item_tax,
						item_disc_amt = disc_amt,
						item_total = total_price,
						print_medium_id = print_medium_id,
						print_medium_size = print_medium_size,
						moulding_id = moulding_id,
						moulding_size = moulding_size,
						mount_id = mount_id,
						mount_size = mount_size,
						acrylic_id = acrylic_id,
						acrylic_size = acrylic_size,
						stretch_id = stretch_id,
						stretch_size = stretch_size,
						board_id = board_id,
						board_size = board_size,
						image_width = image_width,
						image_height = image_height,
						updated_date = today
					)
				
				usercartitems.save()
				
			cart_qty = usercart.quantity + qty
				
		except IntegrityError as e:
			msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

		except Error as e:
			msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

	
	# Create a new cart
	else:
	
		try :

			newusercart = Cart(
				store = ecom,
				user = userid,
				session_id = sessionid,
				quantity =  qty,
				cart_sub_total = item_sub_total,
				cart_disc_amt = disc_amt,
				cart_tax  = item_tax,
				cart_total = total_price,
				updated_date = today,
				cart_status = 'AC'		
			)

			newusercart.save()
			
			if prod :
				usercartitems = Cart_item(
					cart = newusercart,
					product = prod,
					user_image = user_image,
					promotion = p_promotion,
					frame_promotion = f_promotion,
					quantity = qty,
					item_unit_price = item_unit_price,
					item_sub_total = item_sub_total,
					item_tax  = item_tax,
					item_disc_amt = disc_amt,
					item_total = total_price,
					print_medium_id = print_medium_id,
					print_medium_size = print_medium_size,
					moulding_id = moulding_id,
					moulding_size = moulding_size,
					mount_id = mount_id,
					mount_size = mount_size,
					acrylic_id = acrylic_id,
					acrylic_size = acrylic_size,
					stretch_id = stretch_id,
					stretch_size = stretch_size,
					board_id = board_id,
					board_size = board_size,
					image_width = image_width,
					image_height = image_height,
					updated_date = today
				)
			elif user_image:
				usercartitems = Cart_item(
					cart = usercart,
					product_id = prod_id,
					user_image = user_image,
					promotion = p_promotion,
					frame_promotion = f_promotion,
					quantity = qty,
					item_unit_price = item_unit_price,
					item_sub_total = item_sub_total,
					item_tax  = item_tax,
					item_disc_amt = disc_amt,
					item_total = total_price,
					print_medium_id = print_medium_id,
					print_medium_size = print_medium_size,
					moulding_id = moulding_id,
					moulding_size = moulding_size,
					mount_id = mount_id,
					mount_size = mount_size,
					acrylic_id = acrylic_id,
					acrylic_size = acrylic_size,
					stretch_id = stretch_id,
					stretch_size = stretch_size,
					board_id = board_id,
					board_size = board_size,
					image_width = image_width,
					image_height = image_height,
					updated_date = today
				)
			
			usercartitems.save()

			cart_qty = qty
			
		except IntegrityError as e:
			msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

		except Error as e:
			msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

	# Update the status of the User_image to "MTC" (Moved to Cart)
	if user_image:
		try: 
			u = User_image (
				id = user_image.id,
				session_id = user_image.session_id,
				user = user_image.user,
				image_to_frame = user_image.image_to_frame,
				status = 'MTC',
				created_date = user_image.created_date
			)
			u.save()
		except Error as e:
			msg = 'Apologies!! We had a system issue. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'
	
	return( JsonResponse({'msg':msg, 'cart_qty':cart_qty}, safe=False) )
	

@csrf_exempt
def show_cart(request):
	usercart = {}
	usercartitems = {}
	shipping_cost = 0 
	user_image = None
	''' Let's check if the user has a cart open '''
	try:
		if request.user.is_authenticated:
			usr = User.objects.get(username = request.user)
			usercart = Cart.objects.get(user = usr, cart_status = "AC")
		else:
			sessionid = request.session.session_key		
			if sessionid is None:
				request.session.create()
				sessionid = request.session.session_key
				
			usercart = Cart.objects.get(session_id = sessionid, cart_status = "AC")

		# If any order exists against this cart
		order = Order.objects.filter(cart_id = usercart.cart_id).first()
		if order:
			shipping_cost = order.shipping_cost
		else:
			shipping_cost = 0
			
		usercartitems = Cart_item.objects.select_related('product', 'promotion').filter(cart = usercart.cart_id,
			product__product_image__image_type='THUMBNAIL').values(
			'cart_item_id', 'product_id', 'quantity', 'item_total', 'moulding_id',
			'moulding__name', 'moulding__width_inches', 'print_medium_id', 'mount_id', 'mount__name',
			'acrylic_id', 'mount_size', 'product__name', 'image_width', 'image_height',
			'product__product_image__url', 'cart_id', 'promotion__discount_value', 'promotion__discount_type', 'mount__color',
			'item_unit_price', 'item_sub_total', 'item_disc_amt', 'item_tax', 'item_total'
			)
		
		# Let's get the user uploaded images, if any
		user_image = Cart_item.objects.select_related('user_image', 'frame_promotion').filter(
			cart = usercart.cart_id, product__isnull = True).values(
			'cart_item_id', 'user_image_id', 'user_image__image_to_frame', 'quantity', 'item_total', 'moulding_id',
			'moulding__name', 'moulding__width_inches', 'print_medium_id', 'mount_id', 'mount__name',
			'acrylic_id', 'mount_size', 'product__name', 'image_width', 'image_height',
			'product__product_image__url', 'cart_id', 'promotion__discount_value', 'promotion__discount_type', 'mount__color',
			'item_unit_price', 'item_sub_total', 'item_disc_amt', 'item_tax', 'item_total'
			)
		
			
	except Cart.DoesNotExist:
			usercart = {}

	## Get Tax rates
	taxes = get_taxes()
	image_tax_rate = taxes['image_tax_rate']
	oth_tax_rate = taxes ['oth_tax_rate']


	
	if request.is_ajax():

		template = "eStore/cart_include.html"
	else :
		template = "eStore/cart.html"
	
	
	total_bare = 0
	
	if usercart :
		total_bare = usercart.cart_total  - shipping_cost - usercart.voucher_disc_amount
	
	return render(request, template, {'usercart':usercart, 
		'usercartitems': usercartitems, 'shipping_cost':shipping_cost, 'total_bare':total_bare,
		'user_image':user_image})

@csrf_exempt
def update_cart_item(request):

	json_data = json.loads(request.body.decode("utf-8"))

	# Get existing cart items
	cart_item = Cart_item.objects.filter( cart_item_id = json_data['cart_item_id'], cart_id = json_data['cart_id'] ).first()
	msg = ''

	if not cart_item:
		return JsonResponse({'msg':'Not cart items found for cart # ' + cart_item_id}, safe=False)	
	
	# Get the cart this item is associated with
	cart = Cart.objects.filter(cart_id = cart_item.cart_id, cart_status = "AC").first()
	
	# number of items in the cart
	#num_cart_item = Cart_item.objects.filter(cart = cart)
	
	updated_qty = int(json_data['updated_qty'])
	##############################################
	#get item_price
	##############################################
	image_price = 0
	item_price = 0
	disc_amt = 0
	item_unit_price = 0


	if cart_item.product is None:
		c_item = get_user_item_price_by_cart_item(json_data['cart_item_id'])
	else :
		c_item = get_item_price_by_cart_item(json_data['cart_item_id'])
	
	
	if c_item:
		item_price = round(c_item['item_price'])
		disc_amt = round(c_item['disc_amt'])
		item_unit_price = round(c_item['item_unit_price'])
		


	# TAX Calculations
	item_tax = 0
	item_sub_total = 0
	taxes = get_taxes()
	#if product exists then it's an image tax
	if cart_item.product_id :
		tax_rate = taxes['image_tax_rate']
	else :
		tax_rate = taxes['moulding_tax_rate']

		
	# Update the discount, tax, sub_total and item_total as per the updated quantity
	item_total = item_price * updated_qty
	disc_amt = disc_amt * updated_qty
	item_unit_price = item_unit_price * updated_qty
	
	# Calculate tax and sub_total
	item_sub_total = ( item_total / (1 + (tax_rate/100)) )
	item_tax = item_total - item_sub_total
	#############################################################

	
	msg = "SUCESS"

	# Update the cart item and the cart
	try :

		newusercart = Cart(
			cart_id = cart.cart_id,
			store = cart.store,
			user_id = cart.user_id,
			session_id = cart.session_id,
			quantity =  cart.quantity - cart_item.quantity + updated_qty,
			cart_sub_total = cart.cart_sub_total - cart_item.item_sub_total + item_sub_total,
			cart_disc_amt  = cart.cart_disc_amt - cart_item.item_disc_amt + disc_amt,
			cart_tax  = cart.cart_tax - cart_item.item_tax + item_tax,
			cart_total = cart.cart_total - cart_item.item_total + item_total,
			voucher_id = cart.voucher_id,
			voucher_disc_amount = cart.voucher_disc_amount,
			updated_date = today,
			cart_status = cart.cart_status

		)
		newusercart.save()
			
		usercartitems = Cart_item(
			cart_item_id = cart_item.cart_item_id,
			cart_id = cart_item.cart_id,
			product = cart_item.product,
			user_image = cart_item.user_image,
			promotion = cart_item.promotion,
			frame_promotion = cart_item.frame_promotion,
			quantity = updated_qty,
			item_unit_price = item_unit_price,
			item_sub_total = item_sub_total,
			item_disc_amt  = disc_amt,
			item_tax  = item_tax,
			item_total = item_total,
			moulding_id = cart_item.moulding_id,
			moulding_size = cart_item.moulding_size,
			print_medium_id = cart_item.print_medium_id,
			print_medium_size = cart_item.print_medium_size,
			mount_id = cart_item.mount_id,
			mount_size = cart_item.mount_size,
			board_id = cart_item.board_id,
			board_size = cart_item.board_size,
			acrylic_id = cart_item.acrylic_id,
			acrylic_size = cart_item.acrylic_size,
			stretch_id = cart_item.stretch_id,
			stretch_size = cart_item.stretch_size,
			image_width = cart_item.image_width,
			image_height = cart_item.image_height,
			updated_date = today
			)
		usercartitems.save()


	except IntegrityError as e:
		msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

	except Error as e:
		msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

		
			
	
	return( JsonResponse({'msg':msg}, safe=False) )

	
@csrf_exempt	
def delete_cart_item(request):

	cart_item_id = request.POST.get('cart_item_id','')
	sub_total = request.POST.get('sub_total','')
	cart_total = request.POST.get('cart_total','')
	tax = request.POST.get('tax','')
	item_total = request.POST.get('item_total','')
	
	cart_item = Cart_item.objects.filter(cart_item_id = cart_item_id).first()
	
	if not cart_item:
		return JsonResponse({'msg':'Not cart items found for cart # ' + cart_item_id}, safe=False)	
	
	# Get the cart this item is associated with
	cart = Cart.objects.filter(cart_id = cart_item.cart_id, cart_status = "AC").first()
	
	# number of items in the cart
	num_cart_item = Cart_item.objects.filter(cart = cart).count()
	
	# Get related order
	order = Order.objects.filter( cart = cart ).first()
	order_item = {}
	
	## Get Tax rates
	taxes = get_taxes()
	image_tax_rate = taxes['image_tax_rate']
	oth_tax_rate = taxes ['oth_tax_rate']
	
	net_oth_price = 0
	oth_tax = 0
	net_image_price = 0
	image_tax = 0
	
	if order:
		order_item = Order_items.objects.filter(
					order = order,
					product = cart_item.product,
					moulding = cart_item.moulding,
					moulding_size = cart_item.moulding_size,
					item_total = cart_item.item_total,
					print_medium = cart_item.print_medium,
					print_medium_size = cart_item.print_medium_size,
					mount = cart_item.mount,
					mount_size = cart_item.mount_size,
					board = cart_item.board,
					board_size = cart_item.board_size,
					acrylic = cart_item.acrylic,
					acrylic_size = cart_item.acrylic_size,
					stretch = cart_item.stretch,
					stretch_size = cart_item.stretch_size,
					image_width = cart_item.image_width,
					image_height = cart_item.image_height 
				).first()	

	msg = "SUCCESS"
	
	try :

		# If this was the last item in the cart then delete the item as well as cart
		# if there are more items in the cart, then update cart quantity and remove the item
		if num_cart_item == 1:
			# Delete Item
			cart_item.delete()
			cart.delete()

			if order:
				order_item.delete()
				order.delete()
			
		else :

			if order_item :

				order_item.delete()
			
			if order :
				o = Order (
					order_id = order.order_id,
					order_date = order.order_date,
					cart_id = order.cart_id, 
					session_id = order.session_id,
					quantity = cart.quantity - cart_item.quantity,
					store_id = settings.STORE_ID,
					user = cart.user,
					voucher_id = order.voucher_id,
					voucher_disc_amount = order.voucher_disc_amount,
					sub_total = order.sub_total - (cart_item.item_sub_total),
					order_discount_amt = order.order_discount_amt - cart_item.item_disc_amt,
					tax = order.tax - (cart_item.item_tax),
					order_total = cart.cart_total - cart_item.item_total,
					shipping_cost = order.shipping_cost,
					shipping_method = order.shipping_method,
					shipper = order.shipper,
					shipping_status = order.shipping_status,
					updated_date = today,
					order_status = order.order_status	
				)
				o.save()
							
			# update cart Qty
			c = Cart (
				cart_id = cart_item.cart_id, 
				quantity = cart.quantity - cart_item.quantity,
				store_id = settings.STORE_ID,
				session_id = cart.session_id,
				user = cart.user,
				cart_total = cart.cart_total - cart_item.item_total,
				updated_date = today,
				cart_status = cart.cart_status,
				cart_sub_total = cart.cart_sub_total - cart_item.item_sub_total,
				cart_disc_amt  = cart.cart_disc_amt - cart_item.item_disc_amt,
				cart_tax  = cart.cart_tax - cart_item.item_tax,
				voucher_id = cart.voucher_id,
				voucher_disc_amount = cart.voucher_disc_amount,
				
			)
			c.save()
			
			cart_item.delete()
			
		
	except cart.DoesNotExist:
		msg = "Cart does not exist"
	
	except cart_item.DoesNotExist:
		msg = "Cart item does not exist"
	
	except Error as e:
		msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

	
	
	return JsonResponse({'msg':msg}, safe=False)

@csrf_exempt	
def sync_cart_session_user(request, sessionid):

	# Get current session id
	#sessionid = request.session.session_key
	
	if sessionid is None:
		return JsonResponse({"status":"NOCART"})
	
	try:
		# Get usercart by session and user is None
		sessioncart = Cart.objects.get(session_id = sessionid, user = None, cart_status = "AC")
	except Cart.DoesNotExist:
		return JsonResponse({"status":"NOCART"})
	
	if sessioncart:
		if request.user.is_authenticated:
			try:
			
				# Check if the user already has a cart open
				userid = User.objects.get(username = request.user)

				cart = Cart.objects.filter(user = userid, cart_status = "AC")
				# User already has a cart open, then return
				if cart:
					# Abondon the existing session cart & return back
					updcart = Cart(
						cart_id = sessioncart.cart_id,
						store = sessioncart.store,
						user_id = userid,
						cart_total = sessioncart.cart_total,
						session_id = sessioncart.session_id,
						quantity =  sessioncart.quantity,
						updated_date = sessioncart.updated_date,
						cart_status = 'AB'
					)						
					updcart.save()
					return JsonResponse({"status":"CARTOPEN"})
			
				# Update the session Carr with current user id
				updcart = Cart(
					cart_id = sessioncart.cart_id,
					store = sessioncart.store,
					user_id = userid,
					cart_total = sessioncart.cart_total,
					session_id = sessioncart.session_id,
					quantity =  sessioncart.quantity,
					updated_date = sessioncart.updated_date,
					cart_status = sessioncart.cart_status
				)						
				
				updcart.save()

			finally:
				return JsonResponse({"status":"NOUSER"})
				
			return JsonResponse({"status":"SYNCHED"})
			
		else:
			return JsonResponse({"status":"NOUSER"})
	
	return JsonResponse({"status":"NOCART"})
	
	
@csrf_exempt
def apply_voucher(request):
		
	cart_id = int(request.POST.get('cart_id', '0'))
	voucher_code = request.POST.get('voucher_code', '')
	cart_total = Decimal(request.POST.get('cart_total', '0'))

	if voucher_code == '':
		return JsonResponse({"status":"INVALID-CODE"})
	
	
	voucher = Voucher.objects.filter(voucher_code = voucher_code, effective_from__lte = today, 
			effective_to__gte = today, store_id = settings.STORE_ID).first()
			
	if not voucher :
		return JsonResponse({"status":"INVALID-CODE"})

	voucher_user = Voucher_user.objects.filter(voucher = voucher, effective_from__lte = today, 
			effective_to__gte = today).first()

	if not voucher_user :
		return JsonResponse({"status":"INVALID-CODE"})

	if voucher_user.used_date != None :
		return JsonResponse({"status":"USED"})
		
		
	# get logged in user
	try: 
		user = User.objects.get(username = request.user)
	except User.DoesNotExist:
		user = None
	
	if voucher_user.user != user:
		return JsonResponse({"status":"USER-MISMATCH"})
	
	disc_type = voucher.discount_type
	disc_amount = 0

	status = "SUCCESS"
	
	if disc_type == "PERCENTAGE":
		disc_amount = cart_total * voucher.discount_value/100
		cart_total = cart_total - ( cart_total * voucher.discount_value/100 )
	elif disc_type == "CASH":
		disc_amount = voucher.discount_value
		cart_total = cart_total - voucher.discount_value

	cart = Cart.objects.filter(cart_id = cart_id, cart_status = "AC").first()
	if cart.voucher_id:
		return JsonResponse({"status":"ONLY-ONE"})
		
	status = "SUCCESS"
	disc_amount = round(disc_amount)
	
	# Update the cart with voucher
	if cart :
		
		try:
			c = Cart (
				cart_id = cart_id,
				store = cart.store,
				session_id = cart.session_id,
				user = cart.user,
				voucher_id = voucher.voucher_id,
				voucher_disc_amount = disc_amount,
				quantity = cart.quantity,
				cart_sub_total = cart.cart_sub_total,
				cart_disc_amt  = cart.cart_disc_amt + disc_amount,
				cart_tax  = cart.cart_tax,
				cart_total = cart_total,
				updated_date =  today,
				cart_status = cart.cart_status
			)
			c.save()
			
			v = Voucher_user (
				id = voucher_user.id,
				voucher = voucher_user.voucher,
				user = voucher_user.user,
				effective_from = voucher_user.effective_from,
				effective_to = voucher_user.effective_to,
				used_date = today
			)
			v.save()
			
		except Error as e:
			status = 'INT-ERR'

	return JsonResponse({"status":status, 'disc_amount': disc_amount, 'cart_total':cart_total})
	
	
	