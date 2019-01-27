from datetime import datetime
import datetime
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError, DatabaseError, Error
from django.db.models import Count
from django.contrib.auth.models import User

from eStore.models import Ecom_site, Main_slider, New_arrival, Promotion, Menu, Product_category
from eStore.models import New_arrival_images, Promotion_images, Product, Product_image, Cart
from django.http import HttpResponse
from django.conf import settings

from django import template

today = datetime.date.today()

register = template.Library()
@register.inclusion_tag('eStore/topbar.html')
def topbar(request , auth_user):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	return {'ecom_site':ecom, 'request':request, 'user': request.user, 'auth_user' : auth_user}


@register.inclusion_tag('eStore/eStore_admin_menu.html')
def admin_menu(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	return {'ecom_site':ecom, 'request':request, 'user': request.user}	
	
	
@register.inclusion_tag('eStore/estore_menu.html')	
def menubar(request):

	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	
	#Level 0
	level0_menuitems = Menu.objects.filter(store = ecom, effective_from__lte = today, 
		effective_to__gte = today, level=0).order_by('sort_order')

	# Level 1
	level1_menuitems = Product_category.objects.annotate(Count(
			'product_product_category')).filter(parent_id__isnull = True,
			product_product_category__count__gt = 100).order_by('-product_product_category__count')

	# Level 2
	level2_menuitems = Product_category.objects.filter(parent_id__in = level1_menuitems)

	''' Get cart for total items in the cart '''
	sessionid = request.session.session_key
	if sessionid is None:
		request.session.create()
		sessionid = request.session.session_key

	usercart = {}

	
	try:
		if request.user.is_authenticated:
			
			userid = User.objects.get(username = request.user)
			usercart = Cart.objects.get(user_id = userid)
		else:
			usercart = Cart.objects.get(session_id = sessionid)
	
	except Cart.DoesNotExist:
			usercart = {}
	
	return {'level0_menuitems':level0_menuitems, 
			'level1_menuitems':level1_menuitems,
			'level2_menuitems':level2_menuitems,
			'usercart':usercart}

@register.inclusion_tag('eStore/footer.html')	
def site_footer():
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	return {'ecom_site':ecom}

@register.inclusion_tag('eStore/copy_right.html')	
def copy_right():
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	return {'ecom_site':ecom}


@register.inclusion_tag('eStore/cart_update_message.html')	
def update_cart_message(result):
	return ({'result':result})
	