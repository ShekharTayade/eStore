from django import template

from django.shortcuts import render, get_object_or_404
from datetime import datetime
import datetime
from django.db import IntegrityError, DatabaseError, Error

from eStore.models import Ecom_site, Main_slider, New_arrival, Promotion, Product_category, Frame_image, Moulding_image
from eStore.models import New_arrival_images, Promotion_images, Product, Product_image, Product_collection
from django.http import HttpResponse
from django.conf import settings

today = datetime.date.today()

register = template.Library()

@register.inclusion_tag('eStore/main_slider.html')
def show_main_slider_section():
	
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	
	slide_array = []
	''' Get new arrivals '''
	new_arr_images = New_arrival_images.objects.filter(
		new_arrival__effective_from__lte = today, new_arrival__effective_to__gte = today,
		new_arrival__store = ecom)

	''' Get promotions'''
	promo_images = Promotion_images.objects.filter(
		promotion__effective_from__lte = today, promotion__effective_to__gte = today,
		promotion__store = ecom)
	
	'''Let's get the slider sequenc'''
	seq =  Main_slider.objects.filter(effective_from__lte = today, effective_to__gte = today,
			 store = ecom) 
	# main_slider should have only one row for a given date range
	for s in seq:
		if s.new_arrival_seq > s.promotion_seq:
			for n in new_arr_images:
				slide_array.append(n.image_name)
			for p in promo_images:
				slide_array.append(p.image_name)
		else:
			for p in promo_images:
				slide_array.append(p.image_name)
			for n in new_arr_images:
				slide_array.append(n.image_name)
		
	return {'slide_array':slide_array, 'ecom_site':ecom}
	
@register.inclusion_tag('eStore/featured_products.html')
def show_featured_products_section():
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	'''Get the featured products'''
	featured_prod = Product.objects.filter(featured = True, store = ecom)
	featured_prod_img = Product_image.objects.filter(product_id__in = featured_prod, image_type = "FRONT")

	# Let's create the final set for featured prods 
	featured_prods = []
	for p in featured_prod:
		rec = {}
		prod_img = ""
		for i in featured_prod_img:
			if p.product_id == i.product_id:
				prod_img = i.url
		rec['product_id'] = p.product_id
		rec['name'] = p.name
		rec['desription'] = p.description
		rec['price'] = p.price
		rec['url'] = prod_img
		featured_prods.append(rec)

	return {'featured_prods':featured_prods, 'ecom_site':ecom}
	

@register.inclusion_tag('eStore/collections.html')
def show_collections_section():
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	'''Get the collections'''
	prod_collections = Product_collection.objects.filter(store = ecom)

	return {'prod_collections':prod_collections, 'ecom':ecom}

@register.inclusion_tag('eStore/trending_categories.html')
def show_trending_categories():

	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	
	'''Get trending categories'''
	trending_cat = Product_category.objects.filter(trending = True)
	
	
	return {'trending_categories':trending_cat, 'ecom_site':ecom}	


@register.inclusion_tag('eStore/show_frames_section.html')
def show_frame_my_art(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	
	'''Get trending categories'''
	show_frames = Moulding_image.objects.filter(moulding__featured = True, image_type__iexact = "SHOWCASE")
	
	return {'show_frames':show_frames, 'ecom_site':ecom}	
