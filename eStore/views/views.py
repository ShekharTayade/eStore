from django.shortcuts import render, get_object_or_404
from datetime import datetime
import datetime
from django.db import IntegrityError, DatabaseError, Error

from eStore.models import Ecom_site
from eStore.forms import contactUsForm

#from eStore.models import Product_collection
#from eStore.models import New_arrival_images, Promotion_images, Product, Product_image, Cart
from django.http import HttpResponse
from django.conf import settings


today = datetime.date.today()
ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

def index(request):


	return render(request, "eStore/estore_base.html",{})


def contact_us(request):

	if request.method == 'POST':
		form = contactUsForm(request.POST)
		if form.is_valid():
			contact = form.save()
			return redirect('index')  
	else:
		form = contactUsForm()
		
	return render(request, "eStore/contact_us.html", {'ecom_site':ecom, 'form':form})

def contact_msg(request):	
		return render(request, "eStore/contactUs_confirm.html", {})

	
def about_us(request):

	return render(request, "eStore/about_us.html")
	
def terms_conditions(request):

	return render(request, "terms_conditions.html")

	
def faq(request):

	return render(request, "faq.html")
	
def show_prod_details(request):

	return render(request, "show_prod_details.html")
	
def basket(request):

	return render(request, "basket.html")

def show_frame(request) :
	return render(request, "show_frame.html")
