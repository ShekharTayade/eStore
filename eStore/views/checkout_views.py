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

from eStore.models import Cart, Cart_item, Order, Order_items
from eStore.models import User_billing_address, User_shipping_address
from eStore.models import Order_billing, Order_shipping
from eStore.models import Country, State, City, Pin_code, Pin_city_state_country

today = datetime.date.today()

def checkout_step1_address(request):

	cart_id = request.POST.get('cart_id', '')
	sub_total = Decimal(request.POST.get('sub_total', '0'))
	tax = Decimal(request.POST.get('tax', '0'))	
	disc_amt = request.POST.get('disc_amt', '')
	#discounted_amt = Decimal(request.POST.get('discounted_amt', '0'))
	msg = ''

	if cart_id == '':
		return render(request, "eStore/checkout_step1_address_new.html", {})		
	
	#############################################################
	### CREATE THE ORDER
	#############################################################
	# get cart details
	usercart = Cart.objects.filter(cart_id = cart_id).first()
	usercart_items = Cart_item.objects.filter(cart_id = cart_id)

	if not usercart_items:
		return render(request, "eStore/checkout_step1_address.html", {'order_total':0,
					'sub_total':sub_total, 'tax':tax})	
	
	# get shipping and billing addresses if it's a logged in user
	billing_addr = {}
	shipping_addr = {}
	
	order_id = None
	
	# Check if order for cart_id is already created
	order = Order.objects.filter(cart_id = cart_id).first()
	if order :
		# to retain these from the existing order. Other fields will be
		# taken from the usercart
		shipping_method = order.shipping_method
		shipper = order.shipper
		shipping_status = order.shipping_status

		order_items = Order_items.objects.filter(order = order)
		order_id = order.order_id

		#ord_total = order.order_total
		#sub_total = order.sub_total
		#tax = order.tax		
		
		try:
		
			# Check if product is already in the order, if not add
			for c in usercart_items:
				update_ord_itm = False
			
				ord_itm = order_items.filter( order = order,
					product = c.product,
					promotion = c.promotion,
					moulding = c.moulding,
					moulding_size = c.moulding_size,
					item_total = c.item_total,
					print_medium = c.print_medium,
					print_medium_size = c.print_medium_size,
					mount = c.mount,
					mount_size = c.mount_size,
					board = c.board,
					board_size = c.board_size,
					acrylic = c.acrylic,
					acrylic_size = c.acrylic_size,
					stretch = c.stretch,
					stretch_size = c.stretch,
					image_width = c.image_width,
					image_height = c.image_height, 
					updated_date =  today
				).first()
			
				# If same item is found, then update only the quantity if different
				if ord_itm:
					if ord_itm.quantity != c.quantity:
						update_ord_itm = True
						## Update existing order item
						ord_item = Order_items(
							order_item_id = ord_itm.order_item_id,
							order = order,
							product = c.product,
							promotion = c.promotion,
							moulding = c.moulding,
							moulding_size = c.moulding_size,
							quantity = c.quantity,
							item_total = c.item_total,
							print_medium = c.print_medium,
							print_medium_size = c.print_medium_size,
							mount = c.mount,
							mount_size = c.mount_size,
							board = c.board,
							board_size = c.board_size,
							acrylic = c.acrylic,
							acrylic_size = c.acrylic_size,
							stretch = c.stretch,
							stretch_size = c.stretch,
							image_width = c.image_width,
							image_height = c.image_height,
							updated_date =  today
						)
						ord_item.save()

				else:
					update_ord_itm = True
					# Insert the new order item
					new_ord_item = Order_items(
						order = order,
						product = c.product,
						promotion = c.promotion,
						moulding = c.moulding,
						moulding_size = c.moulding_size,
						quantity = c.quantity,
						item_total = c.item_total,
						print_medium = c.print_medium,
						print_medium_size = c.print_medium_size,
						mount = c.mount,
						mount_size = c.mount_size,
						board = c.board,
						board_size = c.board_size,
						acrylic = c.acrylic,
						acrylic_size = c.acrylic_size,
						stretch = c.stretch,
						stretch_size = c.stretch,
						image_width = c.image_width,
						image_height = c.image_height,
						updated_date =  today
					)
					new_ord_item.save()
				
			# If there was an update to the order item, then update Order for the quantity
			if update_ord_itm :
				# Update Order for the quantity
				ord = Order(
					order_id = order.order_id,
					store_id = settings.STORE_ID,
					session_id = usercart.session_id, 
					user = usercart.user,
					voucher = usercart.voucher,
					quantity = usercart.quantity,
					order_total = usercart.cart_total,
					sub_total = sub_total,
					tax = tax,
					shipping_method = shipping_method,
					shipper = shipper,	
					shipping_status = shipping_status,
					cart = usercart,
					updated_date =  today,
					discount_amt = disc_amt,
					order_status = order.order_status
				)
				ord.save()
				order_id = ord.order_id
		except Error as e:
			msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'
		
	
	else :
		
		try:
			new_ord = Order(
				store_id = settings.STORE_ID,
				session_id = usercart.session_id, 
				user = usercart.user,
				voucher = usercart.voucher,
				quantity = usercart.quantity,
				order_total = usercart.cart_total,
				sub_total = sub_total,
				tax = tax,
				shipping_method = None,
				shipper = None,	
				shipping_status = None,
				cart = usercart,
				updated_date =  today,
				discount_amt = disc_amt,
				order_status = 'PP'
				
			)
			
			new_ord.save()
			order_id = new_ord.order_id

			ord_total = new_ord.order_total

			for c in usercart_items:
					
				new_ord_items = Order_items(
					order = new_ord,
					product = c.product,
					promotion = c.promotion,
					moulding = c.moulding,
					moulding_size = c.moulding_size,
					quantity = c.quantity,
					item_total = c.item_total,
					print_medium = c.print_medium,
					print_medium_size = c.print_medium_size,
					mount = c.mount,
					mount_size = c.mount_size,
					board = c.board,
					board_size = c.board_size,
					acrylic = c.acrylic,
					acrylic_size = c.acrylic_size,
					stretch = c.stretch,
					stretch_size = c.stretch,
					image_width = c.image_width,
					image_height = c.image_height,
					updated_date =  today
				)
				new_ord_items.save()
				
	
		except Error as e:
			msg = 'Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.'

	# Let's get shipping, billing addressm if exists 	
	# if it already exists, take it from Order Shipping, else get it from preferred addr, if it exists
	shipping_addr = Order_shipping.objects.filter(order = order).select_related('pin_code', 'state', 'country').first()
	billing_addr = Order_billing.objects.filter(order = order).select_related('pin_code', 'state', 'country').first()
	if shipping_addr is None:
		if user.is_authenticated:
			userObj = User.objects.get(username = request.user)
			shipping_addr = User_shipping_address.filter(use = userObj).select_related('pin_code', 'state', 'country')
			billing_addr = User_billing_address.filter(use = userObj).select_related('pin_code', 'state', 'country')
	
	country_list = Country.objects.all()
	country_arr = []
	for c in country_list:
		country_arr.append(c.country_name)
		
	state_list = State.objects.all()
	state_arr = []
	for s in state_list:
		state_arr.append(s.state_name)
		
	
	city_list = City.objects.all()
	city_arr = []
	for ct in city_list:
		city_arr.append(ct.city)
	
	pin_code_list = Pin_code.objects.all()
	pin_code_arr = []
	for p in pin_code_list:
		pin_code_arr.append(p.pin_code)
	
	return render(request, "eStore/checkout_step1_address_new.html", {'order_total':usercart.cart_total,
					'sub_total':sub_total, 'tax':tax,'shipping_addr':shipping_addr, 'billing_addr':billing_addr,
					'disc_amt':disc_amt, 'country_arr':country_arr, 'state_arr':state_arr, 
					'city_arr':city_arr, 'pin_code_arr':pin_code_arr, 'order_id':order_id})
					
@csrf_exempt					
def get_addr_pin_city_state(request):

	ipin_code = request.POST.get('pin_code', None)
	
	pin_code = {}
	city = {}
	cstate = {}
	country = {}

	if ipin_code :
		pin_codeObj = Pin_code.objects.filter(pin_code = ipin_code)
		pin_code = pin_codeObj.values("pin_code").distinct()
		city = Pin_city_state_country.objects.filter(pin_code__in = pin_codeObj).values("city").distinct()
		cstate = Pin_city_state_country.objects.filter(pin_code__in = pin_codeObj).values("state").distinct()
		country = Pin_city_state_country.objects.filter(pin_code__in = pin_codeObj).values("country__country_name").distinct()
	else :
		pin_code = Pin_city_state_country.objects.values("pin_code").distinct()
		city = Pin_city_state_country.objects.values("city").distinct()
		cstate = Pin_city_state_country.objects.values("state").distinct()
		country = Pin_city_state_country.objects.values("country__country_name").distinct()

		
	return( JsonResponse({'pin_code':list(pin_code), 'city':list(city), 'cstate':list(cstate),
			'country':list(country)}, safe=False) )		


@csrf_exempt
def validate_address(request):
	ipin_code = request.POST.get('pin_code', None)
	icity = request.POST.get('city', None)
	icstate = request.POST.get('cstate', None)
	icountry = request.POST.get('country', None)

	msg = []
	err_flag = False

	if ipin_code is None or ipin_code == '':
		msg.append("Pin code cannot be empty")
		err_flag = True
	if icity is None or icity == '':
		msg.append("City cannot be empty")
		err_flag = True
	if icstate is None or icstate == '':
		msg.append("State cannot be empty")
		err_flag = True
	if icountry is None or icountry == '':
		msg.append("Country cannot be empty")
		err_flag = True
	
	q = Pin_city_state_country.objects.all()
	
	if ipin_code:
		q = q.filter(pin_code_id = ipin_code)
	if icity:
		q = q.filter(city_id = icity)
	if icstate:
		q = q.filter(state_id = icstate)
	if icity:
		cnt = Country.objects.filter(country_name = icountry).first()
		q = q.filter(country = cnt)
	
	if q is None or q.count() == 0:
		msg.append("Entered Pin code, City, State is invalid. Please correct and then proceed.")
		err_flag = True

	if not err_flag:
		msg.append("SUCCESS")
	
	return JsonResponse({'msg':msg})
	
	
def checkout_saveAddr_shippingMethod(request):

	order_id = int(request.POST.get('order_id', '0'))

	shipping_full_name = request.POST.get('shipping_full_name', '')
	shipping_phone_number = request.POST.get('shipping_phone_number', '')
	shipping_email_id = request.POST.get('shipping_email_id', '')
	shipping_phone_number = request.POST.get('shipping_phone_number', '')
	shipping_company = request.POST.get('shipping_company', '')
	shipping_address_1 = request.POST.get('shipping_address_1', '')
	shipping_address_2 = request.POST.get('shipping_address_2', '')
	shipping_pin_code = request.POST.get('shipping_pin_code', '')
	shipping_city = request.POST.get('shipping_city', '')
	shipping_state = request.POST.getlist('shipping_state', [])
	shipping_country = request.POST.getlist('shipping_country', [])
	s_state = State.objects.filter(state_name = shipping_state[0]).first()
	s_country = Country.objects.filter(country_name = shipping_country[0]).first()
	
	billing_full_name = request.POST.get('billing_full_name', '')
	billing_phone_number = request.POST.get('billing_phone_number', '')
	billing_email_id = request.POST.get('billing_email_id', '')
	billing_phone_number = request.POST.get('billing_phone_number', '')
	billing_company = request.POST.get('billing_company', '')
	billing_address_1 = request.POST.get('billing_address_1', '')
	billing_address_2 = request.POST.get('billing_address_2', '')
	billing_pin_code = request.POST.get('billing_pin_code', '')
	billing_city = request.POST.get('billing_city', '')
	billing_state = request.POST.getlist('billing_state', [])
	billing_country = request.POST.getlist('billing_country', [])
	b_state = State.objects.filter(state_name = billing_state[0]).first()
	b_country = Country.objects.filter(country_name = billing_country[0]).first()
	
	err_msg = []
	if shipping_full_name == '':
		err_msg.append("Ship To name can't be blank")
	if billing_full_name == '':
		err_msg.append("Bill To name can't be blank")		
	if shipping_phone_number == '':
		err_msg.append("Ship To phone can't be blank")
	if billing_phone_number == '':
		err_msg.append("Bill To phone can't be blank")		
	if shipping_email_id == '':
		err_msg.append("Ship To email can't be blank")
	if billing_email_id == '':
		err_msg.append("Bill To email can't be blank")		
	if shipping_address_1 == '':
		err_msg.append("Enter atleast one line of Ship To street address")
	if billing_address_1 == '':
		err_msg.append("Enter atleast one line of Bill To street address")
	if shipping_city == '':
		err_msg.append("Ship To city can't be blank")
	if billing_city == '':
		err_msg.append("Bill To city can't be blank")
	if shipping_state == '':
		err_msg.append("Ship To state can't be blank")
	if billing_state == '':
		err_msg.append("Bill To state can't be blank")
	if shipping_country == '':
		err_msg.append("Ship To country can't be blank")
	if billing_country == '':
		err_msg.append("Bill To country can't be blank")

	# get the order
	order = Order.objects.get(pk = order_id)
	
	
	try:
		user = User.objects.get(username = request.user)
		
		# Check if the order shipping, billing record already exists
		ord_shipping = Order_shipping.objects.filter(order = order).first()
		ord_billing = Order_billing.objects.filter(order = order).first()
		
		# Save the records
		if ord_shipping:
			o = Order_shipping(
				order_shipping_id = ord_shipping.order_shipping_id,
				store = ord_shipping.store,
				order = order,
				user = user,
				shipping_address = ord_shipping.shipping_address,
				full_name = shipping_full_name,
				Company = shipping_company,
				address_1 = shipping_address_1,
				address_2 = shipping_address_2,
				land_mark = '',
				city = shipping_city,
				state_id = s_state,
				pin_code_id = shipping_pin_code,
				country_id = s_country,
				phone_number = shipping_phone_number,
				email_id = shipping_email_id,
				updated_date =  today
			)	
		else :
			o = Order_shipping(
				store_id = settings.STORE_ID,
				order = order,
				user = user,
				shipping_address = None,
				full_name = shipping_full_name,
				Company = shipping_company,
				address_1 = shipping_address_1,
				address_2 = shipping_address_2,
				land_mark = '',
				city = shipping_city,
				state_id = s_state,
				pin_code_id = shipping_pin_code,
				country_id = s_country,
				phone_number = shipping_phone_number,
				email_id = shipping_email_id,
				updated_date =  today
			)	
		
		o.save()
	

		if ord_billing:
			b = Order_billing(
				order_billing_id = ord_billing.order_billing_id,
				store = ord_billing.store,
				order = order,
				user = user,
				billing_address = ord_billing.billing_address,
				full_name = billing_full_name,
				Company = billing_company,
				address_1 = billing_address_1,
				address_2 = billing_address_2,
				land_mark = '',
				city = billing_city,
				state_id = b_state,
				pin_code_id = billing_pin_code,
				country_id = b_country,
				phone_number = billing_phone_number,
				email_id = billing_email_id,
				updated_date =  today
			)	
		else :
			b = Order_billing(
				store_id = settings.STORE_ID,
				order = order,
				user = user,
				billing_address = None,
				full_name = billing_full_name,
				Company = billing_company,
				address_1 = billing_address_1,
				address_2 = billing_address_2,
				land_mark = '',
				city = billing_city,
				state_id = b_state,
				pin_code_id = billing_pin_code,
				country_id = b_country,
				phone_number = billing_phone_number,
				email_id = billing_email_id,
				updated_date =  today
			)	
		
		b.save()

	except IntegrityError as e:
		err_msg.append('Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.')

	except Error as e:
		err_msg.append('Apologies!! Could not save your cart. Please use the "Contact Us" link at the bottom of this page and let us know. We will be glad to help you.')

	
	country_list = Country.objects.all()
	country_arr = []
	for c in country_list:
		country_arr.append(c.country_name)
		
	state_list = State.objects.all()
	state_arr = []
	for s in state_list:
		state_arr.append(s.state_name)
		
	
	city_list = City.objects.all()
	city_arr = []
	for ct in city_list:
		city_arr.append(ct.city)
	
	pin_code_list = Pin_code.objects.all()
	pin_code_arr = []
	for p in pin_code_list:
		pin_code_arr.append(p.pin_code)
	
	
	# if there is any error, return to the same page
	if len(err_msg) > 0 :
		return render(request, "eStore/checkout_step1_address_new.html", {'msg':err_msg, 'order_total':order.order_total,
						'sub_total':order.sub_total, 'tax':order.tax,'shipping_addr':o, 'billing_addr':b,
						'disc_amt':order.discount_amt, 'country_arr':country_arr, 'state_arr':state_arr, 
						'city_arr':city_arr, 'pin_code_arr':pin_code_arr, 'order_id':order_id, 'cart_id':order.cart_id})
	else:
		return render(request, "eStore/checkout_step2_shipping_method.html", {'order_shipping_id': ord_shipping.order_shipping_id, 
				'order_total':order.order_total, 'order_id': order_id,
				'sub_total':order.sub_total, 'tax':order.tax,'shipping_addr':o, 'billing_addr':b,
				'disc_amt':order.discount_amt, 'country_arr':country_arr, 'state_arr':state_arr, 
				'city_arr':city_arr, 'pin_code_arr':pin_code_arr, 'cart_id':order.cart_id})

def checkout_step3_order_review(request):
	

	return render(request, "eStore/checkout_step3_order_Review.html", {})
	
	