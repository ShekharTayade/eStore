from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.fields import DecimalField

from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from PIL import Image, ExifTags

class Ecom_site(models.Model):
	store_id = models.AutoField(primary_key=True, null=False)
	html_meta_title = models.CharField(max_length = 256, blank=False, unique=True)
	html_meta_name = models.CharField(max_length = 256, blank=True, default='')	
	seo_keywords = models.CharField(max_length = 256, blank=True, default='')	
	store_name = models.CharField(max_length = 100, blank=False)	
	tag_line = models.CharField(max_length = 50, blank=True, default='')
	show_copyright = models.BooleanField(null=False, default=False)
	copyright_year = models.CharField(max_length = 4, blank=True, default='')
	store_address1 = models.CharField(max_length = 1000 , blank=True, default='')
	store_address2 = models.CharField(max_length = 1000 , blank=True, default='')	
	store_city = models.CharField(max_length = 256 , blank=True, default='')
	store_state = models.CharField(max_length = 256 , blank=True, default='')	
	store_zip = models.CharField(max_length = 256 , blank=True, default='')	
	store_country = models.CharField(max_length = 256 , blank=True, default='')		
	phone_support_available = models.BooleanField(null=False, default=False)
	support_phonenumber = models.CharField(max_length = 50, blank=True, default='')
	phone_support_start_time = models.TimeField(blank=True, null=True)
	phone_support_end_time = models.TimeField(blank=True, null=True)
	phone_support_days = models.CharField(max_length = 50, blank=True, default='')
	show_promotion_section = models.BooleanField(null=False, default=False)
	number_of_promotion_slides = models.IntegerField(null=True, blank=True)
	show_featured_section = models.BooleanField(null=False, default=False)
	featured_header = models.CharField(max_length = 50, blank=True, default='')
	number_of_featured_slides = models.IntegerField(null=True, blank=True)
	show_frame_my_art_section = models.BooleanField(null=False, default=False)
	frame_my_art_header = models.CharField(max_length = 50 , blank=True, default='')
	number_of_frame_my_art_slides = models.IntegerField(null=True, blank=True)
	#email_support_enabled = models.BooleanField(null=False, default=False)
	#support_email = models.EmailField(blank=True, default='')

class Contact_us(models.Model):
    first_name = models.CharField(max_length=150, blank=False, null =False)
    last_name = models.CharField(max_length=150, blank=False, null =False)
    email_id = models.EmailField(blank=False, null=False)
    phone_number = models.CharField(max_length=30, blank=True, default='')
    subject = models.CharField(max_length=200, blank=False, null =False)
    message = models.CharField(max_length=4000, blank=False, null =False)
    msg_datetime = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    response = models.CharField(max_length=4000, blank=True, default='',editable=False)
    resp_datetime = models.DateTimeField(null=True, editable=False)
    reponded_by = models.CharField(max_length=30, blank=True, default='', editable=False)
    
    def __str__(self):
        return self.name
		
	
# Model - voucher
# This model stores vouchers that the Store grants.	
class Voucher(models.Model):
	voucher_id = models.AutoField(primary_key=True, null=False)
	voucher_code = models.CharField(max_length = 20, null=False)
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	discount_type = models.CharField(max_length = 10, null=False)  # PERCETNAGE or CASH
	discount_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	all_applicability = models.BooleanField(null=False, default=False)

	class meta:
		unique_together = (('store', 'voucher_id', 'effective_from', 'discount_type'),)
    
	def __str__(self):
		return self.voucher_id

class Voucher_user(models.Model):
	voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	used_date = models.DateField(blank=True, null=True)

	class meta:
		unique_together = (('voucher', 'user'),)

	def __str__(self):
		return self.user

	
class New_arrival(models.Model):
	new_arival_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	product_tag = models.CharField(max_length = 20, blank=True, default='')
	discount_type = models.CharField(max_length = 10, null=False)  # PERCETNAGE or CASH
	discount_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

	def __str__(self):
		return self.new_arrival_id
	
	
class New_arrival_images(models.Model):
	image_id = models.AutoField(primary_key=True, null=False)
	new_arrival = models.ForeignKey(New_arrival, models.CASCADE)
	image_name = models.CharField(max_length = 1000, blank=True, default='')

	def __str__(self):
		return self.image_name
	
	class Meta:
		unique_together = ("image_id", "new_arrival")

## This drives the main slider on the site. It sequences the contents from Promotions 
# and New Arrivals models		
class Main_slider(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	id = models.AutoField(primary_key=True, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	new_arrival_seq = models.IntegerField(null=True, blank=True)
	promotion_seq = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.id

class Country(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	country_code = models.CharField(max_length=80, primary_key = True) 
	country_name = models.CharField(max_length=100, blank = True, null=True, unique=True)

	def __str__(self):
		return self.country_code

class State(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	state_code = models.CharField(max_length=100, primary_key = True) 
	state_name = models.CharField(max_length=100, blank = True, null=True, unique=True)
	country = models.ForeignKey(Country, models.CASCADE, null=False)

	def __str__(self):
		return self.state_code

class City(models.Model):
	city = models.CharField(max_length=100, primary_key = True) 
	state = models.ForeignKey(State, models.CASCADE, null=False)

	
class Pin_code(models.Model):
	pin_code = models.CharField(primary_key = True, max_length=10, null=False)


class Pin_city_state_country(models.Model):
	pin_code = models.ForeignKey(Pin_code, models.CASCADE, null=False)
	taluk =  models.CharField(max_length=500, null = True)
	city = models.ForeignKey(City, models.CASCADE, null=False) 
	state  = models.ForeignKey(State, models.CASCADE, null=False)
	country  = models.ForeignKey(Country, models.CASCADE, null=False)
	
	class Meta:
		unique_together = ("pin_code", "city", "taluk", "state", "country")

		
	
class Shipping_method (models.Model):
	shipping_method_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	name = models.CharField(max_length = 128, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.name

class Shipping_cost_slabs (models.Model):
	slab_from = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
	slab_to = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
	flat_shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	
	
class Shipper (models.Model):
	shipper_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	name = models.CharField(max_length = 128, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.name
	
	
class Shipper_shipping_method (models.Model):
	shipper_shipping_method = models.AutoField(primary_key=True, null=False) 
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	shipper = models.ForeignKey(Shipper, models.CASCADE, null=False)
	shipping_method_id = models.ForeignKey(Shipping_method, models.CASCADE, null=False)
	rate_type = models.CharField(max_length = 128, null=False) #KG (per KG), #SQFT (per Sqft) etc.....
	rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.shipper
	

class Shipping_status (models.Model):
	shipping_status_id = models.AutoField(primary_key=True, null=False)
	shipping_status_code = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 1000, null=True)

	def __str__(self):
		return self.shipping_status_code

	
class  User_billing_address (models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	billing_address_id = models.AutoField(primary_key=True, null=False)
	full_name = models.CharField(max_length=600, blank=False, null=False)
	company = models.CharField(max_length=600, blank=True, default='')
	address_1 = models.CharField(max_length=600, blank=False, null=False)
	address_2 = models.CharField(max_length=600, blank=True, default='')
	land_mark = models.CharField(max_length=600, blank=True, default='')
	city = models.CharField(max_length=600, blank=False, null=False)
	state = models.ForeignKey(State, on_delete = models.PROTECT, null=True)
	pin_code = models.ForeignKey(Pin_code, on_delete = models.PROTECT, null=True)
	country = models.ForeignKey(Country, on_delete = models.PROTECT, null=False, default= "IND")
	phone_number = models.CharField(max_length=30, blank=True, default='')
	email_id = models.EmailField(blank=True, default='')
	pref_addr = models.NullBooleanField(null=True, default=False)
	updated_date =  models.DateField(blank=True, null=True)

	def __str__(self):
		return self.user

	
class  User_shipping_address (models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	shipping_address_id = models.AutoField(primary_key=True, null=False)
	full_name = models.CharField(max_length=500, blank=False, null=False)
	company = models.CharField(max_length=600, blank=True, default='')
	address_1 = models.CharField(max_length=600, blank=False, null=False)
	address_2 = models.CharField(max_length=600, blank=True, default='')
	land_mark = models.CharField(max_length=600, blank=True, default='')
	city = models.CharField(max_length=600, blank=False, null=False)
	state = models.ForeignKey(State, on_delete = models.PROTECT, null=True)
	pin_code = models.ForeignKey(Pin_code, on_delete = models.PROTECT, null=True)
	country = models.ForeignKey(Country, on_delete = models.PROTECT, null=False, default= "IND")
	phone_number = models.CharField(max_length=30, blank=True, default='')
	email_id = models.EmailField(blank=True, default='')
	pref_addr = models.NullBooleanField(null=True, default=False)
	updated_date =  models.DateField(blank=True, null=True)

	def __str__(self):
		return self.user

class Price_type(models.Model):
	price_type = models.CharField(primary_key=True, max_length = 20, null=False) # RIN (Running inch), SIN (Square Inch)
	description = models.CharField(max_length = 1000, null=True)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)	

	def __str__(self):
		return self.price_type
		

class Tax (models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	tax_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

	def __str__(self):
		return self.name

# Abstrct, People, Animals, Landscape, Portrait etc....
class Stock_image_category(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	category_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 1000, null=True)
	background_image = models.CharField(max_length = 1000, blank=True, default='')
	parent = models.ForeignKey(
		'self', null=True, blank=True, related_name='children',
		on_delete=models.CASCADE)
	trending = models.BooleanField(null=False, default=False)
	url = models.CharField(max_length = 1000, blank=True, default='')
	featured_collection = models.BooleanField(null=False, default=False)

	def __str__(self):
		return self.name
	
	class Meta:
		unique_together = ("store", "category_id", "name")




# Stock Image, User Image, Stock Collage, Original Art etc...etc....	
class Product_type(models.Model):
	TYPE_CHOICES = (
		('STOCK-IMAGE', 'Stock Image'),
		('USER-IMAGE', 'User Uploaded Image'),
		('STOCK-COLLAGE', 'Stock Collage Layout'),
		('ORIGINAL-ART', 'Original Art'),
	)	
	

	store = models.ForeignKey(Ecom_site, models.CASCADE)
	product_type_id = models.CharField(primary_key=True, max_length=10, 
		choices=TYPE_CHOICES)
	is_shipping_required = models.BooleanField(null=False, default=False)
	tax = models.ForeignKey(Tax, models.CASCADE, null=True)

	def __str__(self):
		return self.name		
		
		
class Stock_image(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	product_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 2000, blank=True, default = '')
	price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
	available_on = models.DateField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	part_number = models.CharField(max_length = 30, null=True)
	product_type = models.ForeignKey(Product_type, models.CASCADE, null=True)
	is_published = models.BooleanField(null=False, default=False)
	seo_description = models.CharField(max_length = 300, null=True)
	seo_title  = models.CharField(max_length = 70, null=True)
	charge_taxes = models.BooleanField(null=False, default=False)
	featured = models.BooleanField(null=False, default=False)
	has_variants = models.BooleanField(null=False, default=False)
	aspect_ratio = models.DecimalField(max_digits = 21, decimal_places=18, null=True)
	image_type =  models.CharField(max_length = 1, null=True)
	orientation = models.CharField(max_length = 20, null=True)
	max_width = models.DecimalField(max_digits = 6, decimal_places=2, null=True)
	max_height = models.DecimalField(max_digits = 6, decimal_places=2, null=True)
	min_width = models.DecimalField(max_digits = 6, decimal_places=2, null=True)
	publisher = models.CharField(max_length = 600, null=True)
	artist = models.CharField(max_length = 600, null=True)
	colors = models.CharField(max_length = 600, null=True)
	key_words = models.CharField(max_length = 2000, null=True)
	url = models.CharField(max_length = 1000, blank=True, default='')

	def __str__(self):
		return str( self.product_id ) + " " + self.name
		
class User_image (models.Model):
	user_image_id = models.AutoField(primary_key=True, null=False)
	image_to_frame = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, default="")
	status = models.CharField(max_length = 3, blank=True, null=False)
	created_date = models.DateTimeField(auto_now_add=True, null=False)	
	updated_date = models.DateTimeField(auto_now=True, null=False)	

	def __str__(self):
		return str( self.user_image_id ) + " " + self.image_to_frame.name

class Stock_collage(models.Model):
	stock_collage_id = models.AutoField(primary_key=True, null=False)
	collage_layout = models.ForeignKey('Collage_layout', models.CASCADE, null=False)
	name = models.CharField(max_length = 200, null=False)
	is_published = models.BooleanField(null=False, default=False)

	def __str__(self):
		return str( self.stock_collage_id ) + " " + self.name
	
class Original_art(models.Model):
	art_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 200, null=False)
	artist = models.CharField(max_length = 500, null=False)
	is_published = models.BooleanField(null=False, default=False)

	def __str__(self):
		return self.name + " - By " + self.artist


class stock_image_stock_image_category(models.Model):
	stock_image = models.ForeignKey(Product, models.CASCADE, null=False)
	stock_image_category = models.ForeignKey(Stock_image_category, models.CASCADE, null=True) 

	
#################################################################################
#     Promotions
###################
# Model - promotion
# This model stores promotions that the Store runs.	
# New Arrival, Sale, Promotion etc...
class Promotion(models.Model):
	promotion_id = models.AutoField(primary_key=True, null=False)
	product_type = models.ForeignKey(Product_type, models.CASCADE, null=False) 
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	discount_type = models.CharField(max_length = 10, null=False)  # PERCETNAGE or CASH
	discount_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

	class meta:
		unique_together = (('store', 'promotion_id', 'effective_from', 'product_tag', 'discount_type'),)
	def __str__(self):
		return self.promotion_id

class Promotion_images(models.Model):
	image_id = models.AutoField(primary_key=True, null=False)
	promotion = models.ForeignKey(Promotion, models.CASCADE)
	image_name = models.CharField(max_length = 1000, blank=True, default='')

	class Meta:
		unique_together = ("image_id", "promotion")
	def __str__(self):
		return self.image_name

class Promotion_stock_image(models.Model):
	promotion = models.ForeignKey(Promotion, models.CASCADE, null=False)
	stock_image = models.ForeignKey(Stock_image, models.CASCADE, null=False)

	def __str__(self):
		return str(self.promotion_id)
		
	class Meta:
		unique_together = ("promotion", "stock_image")	

class Promotion_stock_collage(models.Model):
	promotion = models.ForeignKey(Promotion, models.CASCADE, null=False)
	stock_collage = models.ForeignKey(Stock_collage, models.CASCADE, null=False)

	def __str__(self):
		return str(self.promotion_id)
		
	class Meta:
		unique_together = ("promotion", "stock_collage")	

class Promotion_original_art(models.Model):
	promotion = models.ForeignKey(Promotion, models.CASCADE, null=False)
	original_art = models.ForeignKey(Original_art, models.CASCADE, null=False)

	def __str__(self):
		return str(self.promotion_id)
		
	class Meta:
		unique_together = ("promotion", "original_art")	
		
###################
#  END:  Promotions
###################


#################################################################################
#  FRAMING COMPONENTS 
###################
class Mount (models.Model):
	mount_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 2000, null=False, default="")
	type = models.CharField(max_length = 30, blank='', default = '')
	color = models.CharField(max_length = 30, null=False)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)

	def __str__(self):
		return self.name
	
	
class Board (models.Model):
	board_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 2000, null=False, default="")
	type = models.CharField(max_length = 30, blank='', default = '')
	color = models.CharField(max_length = 30, null=False)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)

	def __str__(self):
		return self.name
	
	
class Acrylic (models.Model):
	acrylic_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 2000, null=False, default="")
	type = models.CharField(max_length = 30, blank='', default = '')
	color = models.CharField(max_length = 30, null=False)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)

	def __str__(self):
		return self.name

	
class Print_medium(models.Model):
	medium_id = models.CharField(primary_key=True, max_length = 30)
	description = models.CharField(max_length = 1000, blank=True, default = '')
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)

	def __str__(self):
		return self.medium_id

class Stretch (models.Model):
	stretch_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 2000, null=False, default="")
	type = models.CharField(max_length = 30, blank='', default = '')
	color = models.CharField(max_length = 30, null=False)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)

	def __str__(self):
		return self.name
		
	
class Moulding(models.Model):
	PAPER = 'P'
	CANVAS = 'C'
	BOTH = 'B'
	APPLIES_TO = (
		(PAPER, 'Applies to Paper Only'),
		(CANVAS, 'Applies to Canvas Only'),
		(BOTH, 'Applies to Paper and Canvas'),
	)
	
	moulding_id = models.CharField(primary_key=True, null=False, max_length = 20,)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 1000, blank=True, default = '')
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)
	width_inches = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	depth_inches = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	available_on = models.DateField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	part_number = models.CharField(max_length = 30, null=True)
	product_type = models.ForeignKey(Product_type, models.CASCADE, null=True)
	is_published = models.BooleanField(null=False, default=False)
	seo_description = models.CharField(max_length = 300, null=True)
	seo_title  = models.CharField(max_length = 70, null=True)
	charge_taxes = models.BooleanField(null=False, default=False)
	tax = models.ForeignKey(Tax, models.CASCADE, null=True)
	tax_rate = models.CharField(max_length = 120, null=True)
	featured = models.BooleanField(null=False, default=False)
	has_variants = models.BooleanField(null=False, default=False)
	applies_to = models.CharField(max_length = 1, null=False, choices=APPLIES_TO, default=BOTH)

	def __str__(self):
		return self.name

	
# store images for a Mouldings
class Moulding_image(models.Model):
	moulding = models.ForeignKey(Moulding, models.CASCADE, null=False)
	image_id = models.AutoField(primary_key=True, null=False)
	image_type = models.CharField(max_length = 20, blank=True, default='') # SHOW, APPLY
	url = models.CharField(max_length = 1000, blank=True, default='')
	border_slice = models.CharField(max_length = 10, blank=True, default='')

	def __str__(self):
		return self.moulding
	
	class Meta:
		unique_together = ("moulding", "image_type")	
###########################
#  END:  FRAMING COMPONENTS
###########################



#################################################################################
#  CART 
###################
class Cart(models.Model):
	cart_id = models.AutoField(primary_key=True, null=False)
	product_type = models.ForeignKey('Product_type', models.CASCADE, null=False) 
	store = models.ForeignKey(Ecom_site, models.PROTECT)
	session_id = models.CharField(max_length = 40, blank=True, default='') # to store the session_key in case of anonymous user
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	voucher = models.ForeignKey(Voucher, models.PROTECT, null=True)
	voucher_disc_amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	quantity = models.IntegerField(null=True)
	cart_sub_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	cart_disc_amt  = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	cart_tax  = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	cart_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	cart_status = models.CharField(max_length = 2, blank=True, default='AC') #"AC" Active, "AB":Abandoned, "CO" Checked-out
	created_date = models.DateTimeField(auto_now_add=True, null=False)	
	updated_date = models.DateTimeField(auto_now=True, null=False)	

# An abstract class for Cart Item	
class Cart_item(models.model):
	cart_item_id = models.AutoField(primary_key=True, null=False) 
	cart = models.ForeignKey('Cart', models.CASCADE, null=False) 
	promotion = models.ForeignKey(Promotion, models.PROTECT, null=True)
	quantity = models.IntegerField(null=False)
	item_unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	item_sub_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	item_disc_amt  = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	item_tax  = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	item_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	moulding = models.ForeignKey(Moulding,on_delete=models.PROTECT, null=True)
	moulding_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	print_medium = models.ForeignKey(Print_medium, models.PROTECT, null=False, default='PAPER')
	print_medium_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	mount = models.ForeignKey(Mount, models.PROTECT, null=True)
	mount_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	board = models.ForeignKey(Board, models.PROTECT, null=True)
	board_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	acrylic = models.ForeignKey(Acrylic, models.PROTECT, null=True)
	acrylic_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	stretch = models.ForeignKey(Stretch, models.PROTECT, null=True)
	stretch_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	image_width = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)
	image_height = models.DecimalField(max_digits=3, decimal_places=0, blank=False, null=False)	
	updated_date =  models.DateField(blank=True, null=True)

	class meta:
		abstract = True
		
class Cart_stock_image(cart_item):
	stock_image = ForeignKey('Stock_image', models.CASCADE, null=False)

class Cart_user_image(cart_item):
	user_image = ForeignKey('User_image', models.CASCADE, null=False)

class Cart_stock_collage(cart_item):
	stock_collage = ForeignKey('Stock_collage', models.CASCADE, null=False)

class Cart_original_art(cart_item):
	original_art = ForeignKey('Original_art', models.CASCADE, null=False)

###################
#  END:  CART
###################



#############################################################################
#  Stock Image Pricing
############################
class Publisher (models.Model):
	publisher_id = models.CharField(primary_key=True, max_length=10, null=False)
	publisher_name = models.CharField(max_length=256, blank=False,  default='')
	publisher_group = models.CharField(max_length=256, null=True)

	def __str__(self):
		return self.publisher_name

	
class Publisher_price (models.Model):
	publisher_price_id = models.AutoField(primary_key=True, null=False)
	publisher = models.ForeignKey(Publisher, models.CASCADE, max_length=10, null=False)
	print_medium = models.ForeignKey(Print_medium, models.CASCADE, null=False, default='PAPER')
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	
	class Meta:
		unique_together = ("publisher", "print_medium", "price_type")	
		
	def __str__(self):
		return self.publisher__name
############################
#  END:  Stock Image Pricing
############################
	

#############################################################################
#  	Business User
############################
class Profile_group (models.Model):
	profile_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length=30, blank=True)
	description = models.CharField(max_length=30, blank=True)
	discount_type = models.CharField(max_length=30, blank=True)
	discount_percentage = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)	

	
class Business_profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="business_user")
	contact_name = models.CharField(max_length=500, blank=False)
	company =  models.CharField(max_length=30, blank=True)
	profile_group = models.ForeignKey(Profile_group, models.CASCADE, null=True)
	address_1 = models.CharField(max_length=600, blank=False, null=False)
	address_2 = models.CharField(max_length=600, blank=True, default='')
	city = models.CharField(max_length=600, blank=False, null=False)
	state = models.ForeignKey(State, on_delete = models.PROTECT, null=False)
	pin_code = models.ForeignKey(Pin_code, on_delete = models.PROTECT, null=True)
	country = models.ForeignKey(Country, on_delete = models.PROTECT, null=False, default= "IND")
	phone_number = models.CharField(max_length=30, blank=False, null=False)
	# email_id  = models.EmailField(blank=True, default='')  -- Same as 'User' email
	gst_number = models.CharField(max_length=600, blank=True, default='')
	tax_id = models.CharField(max_length=600, blank=True, default='')
	approval_date = models.DateField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True, null=False)	
	updated_date = models.DateTimeField(auto_now=True, null=False)	

############################
#  END:  Business User
############################

	

	
	
	
	
	
class Generate_number_by_month(models.Model):
	type = models.CharField(max_length = 50, null=False, primary_key = True)
	description = models.CharField(max_length = 1000, null=True)
	month_year = models.CharField(max_length = 6, null=False)
	current_number = models.IntegerField(null=False)	








	

@receiver(post_save, sender=User_image, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
  if instance.image_to_frame:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fullpath = BASE_DIR + instance.image_to_frame.url
    rotate_image(fullpath)

	
def rotate_image(filepath):
  try:
    image = Image.open(filepath)
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    image.save(filepath)
    image.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass		
	
	