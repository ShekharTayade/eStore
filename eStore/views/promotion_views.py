from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Count

from datetime import datetime
import datetime
import json

from eStore.models import Ecom_site, Product, Product_image, Product_variant, Product_category
from eStore.models import Product_product_category, Product_attribute, Cart, Product_collection, Cart_item
from eStore.models import Product_product_collection, Print_medium, Publisher_price, Promotion_product

from .frame_views import *
from .image_views import *

today = datetime.date.today()

def promotion_products(request):

	return render(request, "eStore/promotion_select_products.html", {})
	