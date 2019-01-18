from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import datetime

from eStore.models import Menu, Ecom_site

def get_menu(request):
	
	ecom = get_object_or_404(Ecom_site, store_id=settings.STORE_ID )
	today = datetime.date.today()
	
	
	main_menu = Menu.objects.filter(store = ecom, effective_from__lte = today, 
		effective_to__gte = today,
		new_arrival__store = ecom).order_by('sort_order') 

	for m in main_menu:
		
		level1_menu = menu.objects.filter(store = ecom, parent_id = m.id,
			effective_from__lte = today, 
			effective_to__gte = today,
			new_arrival__store = ecom).order_by('sort_order')
		
		for sm in level1_menu:
			level2_menu = menu.objects.filter(store = ecom, parent_id = sm.id,
				effective_from__lte = today, 
				effective_to__gte = today,
				new_arrival__store = ecom).order_by('sort_order')
		
	
	return  main_menu, level1_menu, level2_menu
	
	
	
