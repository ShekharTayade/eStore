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
from eStore.models import New_arrival_images, Promotion_images, Product
from eStore.models import Cart, Cart_item, Tax, Order, Order_items
from eStore.models import Menu
from .frame_views import *
from .image_views import *
from .product_views import *
from .tax_views import *

today = datetime.date.today()
ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

@csrf_protect
@csrf_exempt
def add_to_cart(request):
	prod_id = request.GET.get('prod_id', '')
	qty = int(request.GET.get('qty', '0'))
	moulding_id = request.GET.get('moulding_id', '')
	if moulding_id == '0':
		moulding_id = None

	moulding_size = Decimal(request.GET.get('moulding_size', '0'))
	print_medium_id = request.GET.get('print_medium_id', '')
	print_medium_size = Decimal(request.GET.get('print_medium_size', '0'))
	mount_id = request.GET.get('mount_id', '')
	if mount_id == '0':
		mount_id = None
	mount_size = Decimal(request.GET.get('mount_size', '0'))
	mount_w_left = Decimal(request.GET.get('mount_w_left', '0'))
	mount_w_right = Decimal(request.GET.get('mount_w_right', '0'))
	mount_w_left = Decimal(request.GET.get('mount_w_top', '0'))
	mount_w_left = Decimal(request.GET.get('mount_w_bottom', '0'))
	acrylic_id = request.GET.get('acrylic_id', '')
	if acrylic_id == '0':
		acrylic_id = None
	acrylic_size = Decimal(request.GET.get('acrylic_size', '0'))
	board_id = request.GET.get('board_id', '')
	if board_id == '0':
		board_id = None
	board_size = Decimal(request.GET.get('board_size', '0'))
	stretch_id = Decimal(request.GET.get('stretch_id', ''))
	if stretch_id == '0':
		stretch_id = None
	total_price = Decimal(request.GET.get('total_price', '0'))
	product_tag_id = request.GET.get('product_tag_id', '')
	if product_tag_id == '':
		product_tag_id = None

	userid = None
	image_width = Decimal(request.GET.get('image_width', '0'))
	image_height = Decimal(request.GET.get('image_height', '0'))

	discount = request.GET.get('discount', '')

	promo_str = request.GET.get('promotion_id', '0')
	
	if promo_str == '':
		promo_str = '0'
	promo_id = int(promo_str)
	
	# Get the product
	try:
		prod = Product.objects.get(product_id=prod_id)
	except Product.DoesNotExist:
		msg = "Product " + prod_id + " does not exist"
		return( JsonResponse({'msg':msg, 'cart_qty':qty}, safe=False) )

		
	# Get any discount on the product
	promo = get_product_promotion(prod_id)
	#promo_id = promo['promotion_id'] ### To be taken from the input to this function, so the promo code flows here
	cash_disc = promo['cash_disc']
	percent_disc = promo['percent_disc']
	
	# get Promotion object
	promotion = {}
	if promo != 0:
		promotion = Promotion.objects.filter(promotion_id = promo_id).first()
		
		
	msg = "Success"
	cart_exists = False
	usercart = {}
	cart_qty = 0
	''' Let's check if the user has a cart open '''
	
	sessionid = request.session.session_key
	if request.user.is_authenticated:
		try:
			userid = User.objects.get(username = request.user)
			usercart = Cart.objects.get(user_id = userid) 
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
				usercart = Cart.objects.get(session_id = sessionid)
				#cart.objects.filter(session_id = sessionid)[:1]
			except Cart.DoesNotExist:
				usercart = {}
				cart_exists = False
			
			if usercart:
				cart_exists = True
			else:
				cart_exists = False;

	if cart_exists:

		''' Check if product exists in cart '''
		#cart_prods = Cart_item.objects.filter(cart_id = usercart.cart_id, product_id = prod_id).values(
		#	'cart_item_id', 'quantity', 'product__price', 'moulding_id')

		cart_prods = Cart_item.objects.filter(cart_id = usercart.cart_id, 
					product_id = prod_id, moulding_id = moulding_id,
					print_medium_id = print_medium_id, mount_id = mount_id,
					mount_size = mount_size, acrylic_id = acrylic_id,
					board_id = board_id, stretch_id = stretch_id ).first()

		item_qty = 0
		cartitem_id = 0 
		item_price = 0
		mouldingid = 0
		prod_exits_in_cart = False 
		if cart_prods:
			
			prod_exits_in_cart = True
			cartitem_id = cart_prods.cartitem_id
			item_qty = cart_prods.quantity
			item_price = cart_prods.item_total
			
			# Apply Discount, if any
			if cash_disc > 0:
				item_price = item_price - cash_disc
			elif percent_disc > 0:
				item_price = item_price - (item_price * percent_disc / 100)
	
		try :
			
			#Update the existing cart
			newusercart = Cart(
				cart_id = usercart.cart_id,
				store = ecom,
				user = userid,
				cart_total = Decimal(usercart.cart_total) + (total_price),
				session_id = sessionid,
				quantity =  usercart.quantity + qty,
				updated_date = today,
				cart_status = usercart.cart_status
			)

			newusercart.save()
			
			''' If the product with same moulding, print_medium etc. already exists in the cart items, then update it, else insert new item '''
			if prod_exits_in_cart:
				usercartitems = Cart_item(
					cart_item_id = cartitem_id,
					cart = usercart,
					product_id = prod_id,
					promotion = promotion,
					quantity = item_qty + qty,
					item_total = item_price + total_price,
					print_medium_id = print_medium_id,
					print_medium_size = print_medium_size,
					moulding_id = moulding_id,
					moulding_size = moulding_size,
					mount_id = mount_id,
					mount_size = mount_size,
					acrylic_id = acrylic_id,
					acrylic_size = acrylic_size,
					board_id = board_id,
					board_size = board_size,
					image_width = image_width,
					image_height = image_height,
					updated_date = today
				)
				usercartitems.save()
			else:
				usercartitems = Cart_item(
					cart = usercart,
					product_id = prod_id,
					promotion = promotion,
					quantity = qty,
					item_total = total_price,
					print_medium_id = print_medium_id,
					print_medium_size = print_medium_size,
					moulding_id = moulding_id,
					moulding_size = moulding_size,
					mount_id = mount_id,
					mount_size = mount_size,
					acrylic_id = acrylic_id,
					acrylic_size = acrylic_size,
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
				cart_total = total_price,
				session_id = sessionid,
				quantity =  qty,
				updated_date = today,
				cart_status = 'AA'
			)

			newusercart.save()
				
			usercartitems = Cart_item(
				cart = newusercart,
				product = prod,
				promotion = promotion,
				quantity = qty,
				item_total = total_price,
				print_medium_id = print_medium_id,
				print_medium_size = print_medium_size,
				moulding_id = moulding_id,
				moulding_size = moulding_size,
				mount_id = mount_id,
				mount_size = mount_size,
				acrylic_id = acrylic_id,
				acrylic_size = acrylic_size,
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

	
	return( JsonResponse({'msg':msg, 'cart_qty':cart_qty}, safe=False) )
	

@csrf_exempt
def show_cart(request):

	usercart = {}
	usercartitems = {}
	''' Let's check if the user has a cart open '''
	try:
		if request.user.is_authenticated:
			usr = User.objects.get(username = request.user)
			usercart = Cart.objects.get(user = usr)
		else:
			sessionid = request.session.session_key		
			if sessionid is None:
				request.session.create()
				sessionid = request.session.session_key
				
			usercart = Cart.objects.get(session_id = sessionid)

		usercartitems = Cart_item.objects.select_related('product', 'promotion').filter(cart = usercart.cart_id,
			product__product_image__image_type='THUMBNAIL').values(
			'cart_item_id', 'product_id', 'quantity', 'item_total', 'moulding_id',
			'moulding__name', 'moulding__width_inches', 'print_medium_id', 'mount_id', 'mount__name',
			'acrylic_id', 'mount_size', 'product__name', 'image_width', 'image_height',
			'product__product_image__url', 'cart_id', 'promotion__discount_value', 'promotion__discount_type', 'mount__color'
			)
			
			
	except Cart.DoesNotExist:
			usercart = {}

	## Get Tax rates
	taxes = get_taxes()
	image_tax_rate = taxes['image_tax_rate']
	oth_tax_rate = taxes ['oth_tax_rate']

	
	image_tax = 0
	#moulding_tax = 0
	#mount_tax = 0
	#acrylic_tax = 0
	#board_tax = 0
	#stretch_tax = 0
	total_tax = 0
	sub_total = 0
	disc_amt = 0
	
	for c in usercartitems:

	
		# Get image price on paper and canvas
		per_sqinch_price = get_per_sqinch_price(c['product_id'])
		per_sqinch_paper = per_sqinch_price['per_sqin_paper']
		per_sqinch_canvas = per_sqinch_price['per_sqin_canvas']

		# Get price for the product in cart
		item_total_price = get_item_price_by_cart_item(c['cart_item_id'])
		
		# image tax
		#if c['print_medium_id'] == 'PAPER':
		#	image_price = c['image_width'] * c['image_height'] * per_sqinch_paper
		#else :
		#	image_price = c['image_width'] * c['image_height'] * per_sqinch_canvas
		
		net_image_price = item_total_price['image_price'] / (1 + (image_tax_rate/100))
		image_tax = item_total_price['image_price'] - net_image_price
		total_tax = total_tax + image_tax
		sub_total = sub_total + net_image_price
		
		# All other prices - All other items carry equal tax rate (it can be separated later on, if required
		if 	oth_tax_rate != 0:
			oth_prices = c['item_total'] - item_total_price['image_price']
			net_oth_price = oth_prices / (1 + oth_tax_rate/100)
			oth_tax = oth_prices - net_oth_price
			total_tax = total_tax + oth_tax
			sub_total = sub_total + net_oth_price


		# Get any discount on the product
		promo = get_product_promotion(c['product_id'])
		if promo :
			cash_disc = promo['cash_disc']
			percent_disc = promo['percent_disc']
			# Apply Discount, if any
			d_amt = 0
			if cash_disc > 0:
				d_amt = cash_disc
			elif percent_disc > 0:
				d_amt = (c['item_total'] * percent_disc / 100)
							
			disc_amt = disc_amt + d_amt
	
	if request.is_ajax():

		template = "eStore/cart_include.html"
	else :
		template = "eStore/cart.html"
	
	
	return render(request, template, {'usercart':usercart, 
		'usercartitems': usercartitems, 'sub_total': sub_total, 'total_tax':total_tax, 'disc_amt':disc_amt})

@csrf_exempt
def update_cart_item(request):

	json_data = json.loads(request.body.decode("utf-8"))

	# Get existing cart items
	cart_item = Cart_item.objects.filter( cart_item_id = json_data['cart_item_id'], cart_id = json_data['cart_id'] ).first()
	msg = ''

	if not cart_item:
		return JsonResponse({'msg':'Not cart items found for cart # ' + cart_item_id}, safe=False)	
	
	# Get the cart this item is associated with
	cart = Cart.objects.filter(cart_id = cart_item.cart_id).first()
	
	# number of items in the cart
	num_cart_item = Cart_item.objects.filter(cart = cart)
	
	# Get price for this cart item (by each pricing component )
	total_price = 0

	
	updated_qty = int(json_data['updated_qty'])
	##############################################
	#get item_price
	##############################################
	image_price = 0
	item_price = 0
	# Get image price on paper and canvas
	per_sqinch_price = get_per_sqinch_price(cart_item.product_id)
	per_sqinch_paper = per_sqinch_price['per_sqin_paper']
	per_sqinch_canvas = per_sqinch_price['per_sqin_canvas']
					
	# Image Price
	if cart_item.image_width > 0 and cart_item.image_width > 0:
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
	

		print( "Item Price: " + str(image_price) )
		
		# Acrylic Price		
		acrylic_price = cart_item.image_width * cart_item.image_height * get_acrylic_price_by_id(cart_item.acrylic_id)
		item_price = item_price + acrylic_price

		print( "Acrylic Price: " + str(acrylic_price))
		
		# Moulding price
		moulding_price = (cart_item.image_width + cart_item.image_height) * 2 * get_moulding_price_by_id(cart_item.moulding_id)
		item_price = item_price + moulding_price

		print( "Moulding Price: " + str(moulding_price))
		
		# Mount price
		mount_price = Decimal( ((cart_item.image_width + cart_item.image_height) * 2 * cart_item.mount_size) ) * get_mount_price_by_id(cart_item.mount_id)
		item_price = item_price + mount_price

		print( "Mount Price: " + str(mount_price))
		
		# Board price
		board_price = cart_item.image_width * cart_item.image_height * get_board_price_by_id(cart_item.board_id)
		item_price = item_price + board_price

		print( "Board Price: " + str(board_price))

		print( "Total Price: " + str(item_price))
		
		
	elif cart_item.print_medium_id == "CANVAS":

		# Image price
		image_price = cart_item.image_width * cart_item.image_height * per_sqinch_canvas
		item_price = item_price + image_price

		print( "Item Price: " + str(image_price))

		# Moulding price
		moulding_price = (cart_item.image_width + cart_item.image_height) * 2 * get_moulding_price_by_id(cart_item.moulding_id)
		item_price = item_price + moulding_price

		print( "Moulding Price: " + str(moulding_price))
		
		# Stretch price
		stretch_price = cart_item.image_width * cart_item.image_height * get_stretch_price_by_id(cart_item.stretch_id)
		item_price = item_price + stretch_price
	
		print( "Stretch Price: " + str(stretch_price))

		print( "Total Price: " + str(item_price))

	item_price = round(item_price)			
	#########################################
	## END: Get Item Price
	#########################################
	item_total = item_price*updated_qty
	
	# Cart Price
	cart_total = cart.cart_total - cart_item.item_total + item_total

	## Get Tax rates
	taxes = get_taxes()
	image_tax_rate = taxes['image_tax_rate']
	oth_tax_rate = taxes ['oth_tax_rate']

	net_image_price = image_price / (1 + (image_tax_rate/100))
	image_tax = image_price - net_image_price
	oth_tax = 0
	oth_price = 0
	# All other prices - All other items carry equal tax rate (it can be separated later on, if required
	if 	oth_tax_rate != 0:
		oth_price = item_total - image_price
		net_oth_price = oth_price / (1 + oth_tax_rate/100)
		oth_tax = oth_price - net_oth_price
	
	msg = "SUCESS"

	# Update the cart item and the cart
	try :

		newusercart = Cart(
			cart_id = cart.cart_id,
			store = cart.store,
			user_id = cart.user_id,
			cart_total = cart_total ,
			session_id = cart.session_id,
			quantity =  cart.quantity - cart_item.quantity + updated_qty,
			updated_date = today,
			cart_status = cart.cart_status

		)

		newusercart.save()
			
		usercartitems = Cart_item(
			cart_item_id = cart_item.cart_item_id,
			cart = cart_item.cart,
			product = cart_item.product,
			quantity = updated_qty,
			item_total = item_total,
			print_medium_id = cart_item.print_medium_id,
			print_medium_size = cart_item.print_medium_size,
			moulding_id = cart_item.moulding_id,
			moulding_size = cart_item.moulding_size,
			mount_id = cart_item.mount_id,
			mount_size = cart_item.mount_size,
			acrylic_id = cart_item.acrylic_id,
			acrylic_size = cart_item.acrylic_size,
			board_id = cart_item.board_id,
			board_size = cart_item.board_size,
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

	import pdb
	pdb.set_trace()
	
	cart_item_id = request.POST.get('cart_item_id','')
	sub_total = request.POST.get('sub_total','')
	cart_total = request.POST.get('cart_total','')
	tax = request.POST.get('tax','')
	item_total = request.POST.get('item_total','')
	
	cart_item = Cart_item.objects.filter(cart_item_id = cart_item_id).first()
	
	if not cart_item:
		return JsonResponse({'msg':'Not cart items found for cart # ' + cart_item_id}, safe=False)	
	
	# Get the cart this item is associated with
	cart = Cart.objects.filter(cart_id = cart_item.cart_id).first()
	
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
					stretch_size = cart_item.stretch,
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
			
				# Get image price on paper and canvas
				per_sqinch_price = get_per_sqinch_price(order_item.product_id)
				per_sqinch_paper = per_sqinch_price['per_sqin_paper']
				per_sqinch_canvas = per_sqinch_price['per_sqin_canvas']
				
				if order_item.print_medium_id == 'PAPER':
					image_price = order_item.image_width * order_item.image_height * per_sqinch_paper
				else :
					image_price = order_item.image_width * order_item.image_height * per_sqinch_canvas

				# Calculate the total image tax and sub total
				net_image_price = image_price / (1 + (image_tax_rate/100))
				image_tax = image_price - net_image_price
				
				# All other prices - All other items carry equal tax rate (it can be separated later on, if required
				if 	oth_tax_rate != 0:
					oth_prices = cart_item.item_total - image_price
					net_oth_price = oth_prices / (1 + oth_tax_rate/100)
					oth_tax = oth_prices - net_oth_price
					
				
				order_item.delete()
			
			if order :
				o = Order (
					order_id = order.order_id,
					cart_id = cart_item.cart_id, 
					quantity = cart.quantity - cart_item.quantity,
					store_id = settings.STORE_ID,
					session_id = cart.session_id,
					user = cart.user,
					voucher_id = order.voucher_id,
					sub_total = order.sub_total - (net_image_price + net_oth_price),
					tax = order.tax - (image_tax + oth_tax),
					order_total = cart.cart_total - cart_item.item_total,
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
				cart_status = cart.cart_status
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
		usercart = Cart.objects.get(session_id = sessionid, user = None)
	except Cart.DoesNotExist:
		return JsonResponse({"status":"NOCART"})
	
	if usercart:
		if request.user.is_authenticated:
			try:
				userid = User.objects.get(username = request.user)
				# Update the Carr with current user id
				updcart = Cart(
					cart_id = usercart.cart_id,
					store = usercart.store,
					user_id = userid,
					cart_total = usercart.cart_total,
					session_id = usercart.session_id,
					quantity =  usercart.quantity,
					updated_date = usercart.updated_date,
					cart_status = usercart.cart_status
				)						
				
				updcart.save()

			finally:
				return JsonResponse({"status":"NOUSER"})
				
			return JsonResponse({"status":"SYNCHED"})
			
		else:
			return JsonResponse({"status":"NOUSER"})
	
	return JsonResponse({"status":"NOCART"})
		