from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
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


# Model - promotion
# This model stores promotions that the Store runs.	
# New Arrival, Sale, Promotion etc...
class Promotion(models.Model):
	promotion_id = models.AutoField(primary_key=True, null=False)
	type = models.CharField(max_length = 5, null=True) # Not used at the moment
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	discount_type = models.CharField(max_length = 10, null=False)  # PERCETNAGE or CASH
	discount_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

	class meta:
		unique_together = (('store', 'promotion_id', 'effective_from', 'product_tag', 'discount_type'),)
    
	def __str__(self):
		return self.promotion_id

class Frame_promotion(models.Model):
	promotion_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	discount_type = models.CharField(max_length = 10, null=False)  # PERCETNAGE or CASH
	discount_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)		
	
class Promotion_images(models.Model):
	image_id = models.AutoField(primary_key=True, null=False)
	promotion = models.ForeignKey(Promotion, models.CASCADE)
	image_name = models.CharField(max_length = 1000, blank=True, default='')

	class Meta:
		unique_together = ("image_id", "promotion")

	def __str__(self):
		return self.image_name

# Product tags to displayed with for promotions	
class Promotion_product_tag(models.Model):
	promotion = models.ForeignKey(Promotion, models.CASCADE)
	tag_name = models.CharField(max_length = 50, null=False, default="")
	description = models.CharField(max_length = 2000, null=False, default="")
	tag_url = models.CharField(max_length = 1000, blank=True, default='')
		
		
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

	
class Menu(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	id = models.AutoField(primary_key=True, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	name = models.CharField(max_length = 128, null=False)
	level = models.IntegerField(null=False)  # level 0 is main menu
	parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE) # Should be id field of the parent
	sort_order = models.IntegerField(null=False)
	url = models.CharField(max_length = 256, null=True)
	

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

	
	
class Tax (models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	tax_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

	def __str__(self):
		return self.name
	
	
class Price_type(models.Model):
	price_type = models.CharField(primary_key=True, max_length = 20, null=False) # RIN (Running inch), SIN (Square Inch)
	description = models.CharField(max_length = 1000, null=True)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)	

	def __str__(self):
		return self.price_type

	
# Painting, Frame, Handicraft, Art Flowers, Painted Vase etc...etc....	
class Product_type(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	type_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	is_shipping_required = models.BooleanField(null=False, default=False)
	tax = models.ForeignKey(Tax, models.CASCADE, null=True)

	def __str__(self):
		return self.name
	
	class Meta:
		unique_together = ("store", "name")
	
# Abstrct, People, Animals, Landscape, Portrait etc....
class Product_category(models.Model):
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
		

class Frame (models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	frame_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 128, null=False)
	description = models.CharField(max_length = 2000, blank=True, default = '')
	price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
	price_type = models.ForeignKey(Price_type, models.CASCADE, null=True)
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
	size = models.CharField(max_length = 10, null=True) # in INCHES

	class Meta:
		unique_together = ("store", "name")
				
		
class Product(models.Model):
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
	tax = models.ForeignKey(Tax, models.CASCADE, null=True)
	tax_rate = models.CharField(max_length = 120, null=True)
	featured = models.BooleanField(null=False, default=False)
	has_variants = models.BooleanField(null=False, default=False)
	size = models.CharField(max_length = 200, null=True)
	default_frame = models.ForeignKey(Frame, models.CASCADE, null=True)

		

class Product_product_category(models.Model):
	product = models.ForeignKey(Product, models.CASCADE, null=False)
	product_category = models.ForeignKey(Product_category, models.CASCADE, null=True) 

	
class Product_variant(models.Model):
	variant_id = models.AutoField(primary_key=True, null=False)
	variant_part_number = models.CharField(max_length = 30, null=True)
	name = models.CharField(max_length = 128, null=False)
	product = models.ForeignKey(Product, models.CASCADE, null=False)
	price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
	quantity = models.IntegerField(null=True)
	tax = models.ForeignKey(Tax, models.CASCADE, null=True)

	class Meta:
		unique_together = ("product", "name")
	

# Store unique attributes for a product - such as Publisher, Artist(s) (Multiple authors will be stored as single value),
# quote (to be dijsplayed along side the product), orientation, key words (stored value as comma separated) etc...
class Product_attribute(models.Model):
	product = models.ForeignKey(Product, models.CASCADE)
	name = models.CharField(max_length = 128, null=False)
	value = models.CharField(max_length = 2000, null=False)
	display_as_filter = models.NullBooleanField(null=True)  # in products details pages, left side Filters

	class Meta:
		unique_together = ("product", "name")
	
	
class Product_variant_attribute(models.Model):
	product_variant = models.ForeignKey(Product, models.CASCADE)
	name = models.CharField(max_length = 128, null=False)
	value = models.CharField(max_length = 128, null=False)
	display_as_filter = models.NullBooleanField(null=True)  # in products details pages, left side Filters

	class Meta:
		unique_together = ("product_variant", "name")


class Promotion_product(models.Model):
	promotion = models.ForeignKey(Promotion, models.CASCADE, null=False)
	product = models.ForeignKey(Product, models.CASCADE, null=False)

	def __str__(self):
		return str(self.promotion_id)
		
	class Meta:
		unique_together = ("promotion", "product")	
		
	
class Product_collection(models.Model):
	store = models.ForeignKey(Ecom_site, models.CASCADE)
	collection_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length = 20, null=False, default="")
	description = models.CharField(max_length = 2000, null=False, default="")
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)
	url = models.CharField(max_length = 1000, blank=True, default='')

	def __str__(self):
		return self.name


class Product_product_collection(models.Model):
	product_collection = models.ForeignKey(Product_collection, models.CASCADE, null=False)
	product = models.ForeignKey(Product, models.CASCADE, null=False)	

	def __str__(self):
		return self.product

	
# store images for a product
class Product_image(models.Model):
	product = models.ForeignKey(Product, models.CASCADE, null=False)
	image_id = models.AutoField(primary_key=True, null=False)
	image_type = models.CharField(max_length = 20, blank=True, default='') # FRONT, BACK, BIG, SMALL
	url = models.CharField(max_length = 1000, blank=True, default='')

	class Meta:
		unique_together = ("product", "image_type")

# store images for a product variant
class Product_variant_image(models.Model):
	product_variant = models.ForeignKey(Product_variant, models.CASCADE, null=False)
	image_id = models.AutoField(primary_key=True, null=False)
	image_type = models.CharField(max_length = 20, blank=True, default='') # FRONT, BACK, BIG, SMALL
	url = models.CharField(max_length = 1000, blank=True, default='')

	class Meta:
		unique_together = ("product_variant", "image_type")


# store images for a frames
class Frame_image(models.Model):
	frame = models.ForeignKey(Frame, models.CASCADE, null=False)
	image_id = models.AutoField(primary_key=True, null=False)
	image_type = models.CharField(max_length = 20, blank=True, default='') # SHOW, APPLY
	url = models.CharField(max_length = 1000, blank=True, default='')
	border_slice = models.CharField(max_length = 10, blank=True, default='')

	class Meta:
		unique_together = ("frame", "image_type")	
		
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

class Promotion_frame(models.Model):
	frame_promotion = models.ForeignKey(Frame_promotion, models.CASCADE, null=False)
	moulding = models.ForeignKey(Moulding, models.CASCADE, null=False)

	def __str__(self):
		return str(self.promotion_id)
		
	class Meta:
		unique_together = ("frame_promotion", "moulding")			

		
class User_image (models.Model):
	session_id = models.CharField(max_length = 40, blank=True, default='') # to store the session_key in case of anonymous user
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	image_to_frame = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, default="")
	status = models.CharField(max_length = 3, blank=True, null=False)
	created_date = models.DateTimeField(auto_now_add=True, null=False)	
	updated_date = models.DateTimeField(auto_now=True, null=False)	

		
class Cart(models.Model):
	cart_id = models.AutoField(primary_key=True, null=False)
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
	updated_date =  models.DateField(blank=True, null=True)
	cart_status = models.CharField(max_length = 2, blank=True, default='AC') #"AC" Active, "AB":Abandoned, "CO" Checked-out
	
class Cart_item(models.Model):
	cart_item_id = models.AutoField(primary_key=True, null=False)
	cart = models.ForeignKey(Cart,on_delete=models.PROTECT, null=False)
	product = models.ForeignKey(Product,on_delete=models.PROTECT, null=True)
	user_image = models.ForeignKey(User_image,on_delete=models.PROTECT, null=True)
	promotion = models.ForeignKey(Promotion, models.PROTECT, null=True)
	frame_promotion = models.ForeignKey(Frame_promotion, models.PROTECT, null=True)
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

	class Meta:
		unique_together = ("cart_item_id", "cart")	

		
		
class Order (models.Model):
	order_id = models.AutoField(primary_key=True, null=False)
	order_date =  models.DateField(blank=True, null=True)
	cart = models.ForeignKey(Cart,on_delete=models.PROTECT, null=False)
	store = models.ForeignKey(Ecom_site, models.PROTECT)
	session_id = models.CharField(max_length = 40, blank=True, default='') # to store the session_key in case of anonymous user
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	voucher = models.ForeignKey(Voucher, models.PROTECT, null=True)
	voucher_disc_amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	quantity = models.IntegerField(null=True)
	sub_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	order_discount_amt = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	tax = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	order_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	shipping_method = models.ForeignKey(Shipping_method, models.PROTECT, null=True) #Null is allowed, in case it's a store pickup
	shipper = models.ForeignKey(Shipper, models.PROTECT, null=True) #Null is allowed, in case it's a store pickup	
	shipping_status = models. ForeignKey(Shipping_status, models.PROTECT, null=True) #Null is allowed, in case it's a store pickup
	updated_date =  models.DateField(blank=True, null=True)
	order_status = models.CharField(max_length = 2, blank=True, default='PP') #"PP" Payment Pending, "AB":Abandoned, "CO" Complete
	
class Order_items (models.Model):
	order_item_id = models.AutoField(primary_key=True, null=False)
	order = models.ForeignKey(Order,on_delete=models.PROTECT, null=False)
	product = models.ForeignKey(Product,on_delete=models.PROTECT, null=True)
	user_image = models.ForeignKey(User_image,on_delete=models.PROTECT, null=True)
	promotion = models.ForeignKey(Promotion, models.PROTECT, null=True)
	frame_promotion = models.ForeignKey(Frame_promotion, models.PROTECT, null=True)
	moulding = models.ForeignKey(Moulding,on_delete=models.PROTECT, null=True)
	moulding_size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	quantity = models.IntegerField(null=False)
	item_unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	item_sub_total = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	item_discount_amt = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	item_tax  = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	item_total = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
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
	
	class Meta:
		unique_together = ("order_item_id", "order")	

class Order_shipping (models.Model):
	order_shipping_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.CASCADE, null=False)
	order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	shipping_address = models.ForeignKey(User_shipping_address, models.PROTECT, null=True) # can be null if user ordering is anonymous
	full_name = models.CharField(max_length=500, blank=False, null=False)
	Company = models.CharField(max_length=600, blank=True, default='')
	address_1 = models.CharField(max_length=600, blank=False, null=False)
	address_2 = models.CharField(max_length=600, blank=True, default='')
	land_mark = models.CharField(max_length=600, blank=True, default='')
	city = models.CharField(max_length=600, blank=False, null=False)
	state = models.ForeignKey(State, on_delete = models.PROTECT, null=True)
	pin_code = models.ForeignKey(Pin_code, on_delete = models.PROTECT, null=True)
	country = models.ForeignKey(Country, on_delete = models.PROTECT, null=False, default= "IND")
	phone_number = models.CharField(max_length=30, blank=True, default='')
	email_id = models.EmailField(blank=True, default='')
	updated_date =  models.DateField(blank=True, null=True)
	
class Order_shipping_status_log (models.Model):
	log_id = models.AutoField(primary_key=True, null=False)
	order = models.ForeignKey(Order, models.PROTECT, null=True)
	order_shipping_status =	models.ForeignKey(Shipping_status, models.PROTECT, null=True)
	status_date = models.DateTimeField(blank=True, null=True)
	updated_date =  models.DateField(blank=True, null=True)
	

class Order_billing (models.Model):
	order_billing_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.PROTECT)
	order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT
    )
	billing_date =  models.DateField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	billing_address = models.ForeignKey(User_billing_address, models.PROTECT, null=True)
	full_name = models.CharField(max_length=500, blank=False, null=False)
	Company = models.CharField(max_length=600, blank=True, default='')
	address_1 = models.CharField(max_length=600, blank=False, null=False)
	address_2 = models.CharField(max_length=600, blank=True, default='')
	land_mark = models.CharField(max_length=600, blank=True, default='')
	city = models.CharField(max_length=600, blank=False, null=False)
	state = models.ForeignKey(State, on_delete = models.PROTECT, null=True)
	pin_code = models.ForeignKey(Pin_code, on_delete = models.PROTECT, null=True)
	country = models.ForeignKey(Country, on_delete = models.PROTECT, null=False, default= "IND")
	phone_number = models.CharField(max_length=30, blank=True, default='')
	email_id = models.EmailField(blank=True, default='')
	updated_date =  models.DateField(blank=True, null=True)


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
	
class Profile_group (models.Model):
	profile_id = models.AutoField(primary_key=True, null=False)
	name = models.CharField(max_length=30, blank=True)
	description = models.CharField(max_length=30, blank=True)
	discount_percentage = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	effective_from = models.DateField(blank=True, null=True)
	effective_to = models.DateField(blank=True, null=True)	

	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	full_name = models.CharField(max_length=500, blank=False)
	company =  models.CharField(max_length=30, blank=True)
	profile_group = models.ForeignKey(Profile_group, models.CASCADE, null=True)
	address_1 = models.CharField(max_length=600, blank=True, null='')
	address_2 = models.CharField(max_length=600, blank=True, default='')
	city = models.CharField(max_length=600, blank=True, default='')
	state = models.ForeignKey(State, on_delete = models.PROTECT, null=True)
	pin_code = models.ForeignKey(Pin_code, on_delete = models.PROTECT, null=True)
	country = models.ForeignKey(Country, on_delete = models.PROTECT, null=False, default= "IND")
	phone_number = models.CharField(max_length=30, blank=True, default='')

	
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




class Wishlist(models.Model):
	wishlist_id = models.AutoField(primary_key=True, null=False)
	store = models.ForeignKey(Ecom_site, models.PROTECT)
	session_id = models.CharField(max_length = 40, blank=True, default='') # to store the session_key in case of anonymous user
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	voucher = models.ForeignKey(Voucher, models.PROTECT, null=True)
	voucher_disc_amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
	quantity = models.IntegerField(null=True)
	wishlist_sub_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	wishlist_disc_amt  = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	wishlist_tax  = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	wishlist_total = models.DecimalField(max_digits=12, decimal_places=2,  null=False, default=0)
	updated_date =  models.DateField(blank=True, null=True)
	wishlist_status = models.CharField(max_length = 2, blank=True, default='AC') #"AC" Active, "AB":Abandoned, "MV" Moved-out to Cart
	
class Wishlist_item(models.Model):
	wishlist_item_id = models.AutoField(primary_key=True, null=False)
	wishlist = models.ForeignKey(Wishlist,on_delete=models.PROTECT, null=False)
	product = models.ForeignKey(Product,on_delete=models.PROTECT, null=True)
	user_image = models.ForeignKey(User_image,on_delete=models.PROTECT, null=True)
	promotion = models.ForeignKey(Promotion, models.PROTECT, null=True)
	frame_promotion = models.ForeignKey(Frame_promotion, models.PROTECT, null=True)
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

	class Meta:
		unique_together = ("wishlist_item_id", "wishlist")	