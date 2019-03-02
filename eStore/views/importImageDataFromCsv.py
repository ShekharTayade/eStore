from eStore.models import Product, Product_type, Tax, Product_attribute, Product_image, Product_category
from eStore.models import Product_category, Product_product_category, Ecom_site, Publisher_price, Publisher
import csv

from django.contrib.staticfiles.templatetags.staticfiles import static
from datetime import datetime
import datetime
from django.shortcuts import render, get_object_or_404
from django.conf import settings

ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
today = datetime.date.today()

def importImageData(request): 

	file = 'C:/eCom_Platform/project/eComPlatform/eStore/static/image_data/pod_data.csv'
	cnt = 0
	'''Get Product type (IMAGE) '''
	prod_type = Product_type.objects.filter(name__iexact = "IMAGE", store = ecom).first()
	'''Get Tax code for IMAGE '''
	prod_tax = Tax.objects.filter(name__iexact = "IMAGE", store = ecom).first()
	tax_rate = prod_tax.tax_rate

	with open(file, encoding="utf8") as csvfile:

		readCSV = csv.reader(csvfile, delimiter=',')

		
		for row in readCSV:
			# Skip the first row (header)
			if cnt == 0:
				cnt = cnt + 1
				continue

 
			if row[0]:
			
				
				prod = Product.objects.filter(product_id = int(row[0])).first()

				if not prod:

					newprod = Product(
						store = ecom,
						product_id = int(row[0]),
						name = row[4],
						description = '',
						price = 0,
						available_on = today,
						updated_at = today,
						part_number = row[3],
						product_type = prod_type,
						is_published = True,
						charge_taxes = True,
						tax = prod_tax,
						tax_rate = tax_rate,
						featured = False,
						has_variants = False,
						size = None,
						default_frame = None
					)

					newprod.save()
						

					'''Update '''
					'''							'''
					'''Insert into attributes 	'''
					'''							'''
					# ARTIST
					attr_artist = Product_attribute.objects.filter(name__iexact = "ARTIST", product_id = int(row[0])).first()
					if attr_artist :
						# Udpate
						prod_artist = Product_attribute(
							id = attr_artist.id,
							product_id = row[0],
							name = "ARTIST",
							value = row[5],
							display_as_filter = True
							)
					else:
						# Insert
						prod_artist = Product_attribute(
							product_id = row[0],
							name = "ARTIST",
							value = row[5],
							display_as_filter = True
							)
						
					prod_artist.save()
					
					# PUBLISHER
					attr_publisher = Product_attribute.objects.filter(name__iexact = "PUBLISHER", product = prod).first()
					if attr_publisher :
						prod_publisher = Product_attribute(
							id = attr_publisher.id,
							product_id = row[0],
							name = "PUBLISHER",
							value = row[1],
							display_as_filter = False
							)
					else :
						prod_publisher = Product_attribute(
							product_id = row[0],
							name = "PUBLISHER",
							value = row[1],
							display_as_filter = False
							)
					prod_publisher.save()
					
					# ASPECT-RATIO
					attr_aspectratio = Product_attribute.objects.filter(name__iexact = "ASPECT-RATIO", product = prod).first()
					if attr_aspectratio:
						prod_aspectratio = Product_attribute(
							id = attr_aspectratio.id,
							product_id = row[0],
							name = "ASPECT-RATIO",
							value = int(row[6]) / int(row[7]),
							display_as_filter = False
							)
					else :
						prod_aspectratio = Product_attribute(
							product_id = row[0],
							name = "ASPECT-RATIO",
							value = int(row[6]) / int(row[7]),
							display_as_filter = False
							)
					
					prod_aspectratio.save()

					# MIN-WIDTH
					attr_minwidth = Product_attribute.objects.filter(name__iexact = "MIN-WIDTH", product = prod).first()
					# The value of 4 inch as in width is fixed. So if there is no row already present then only
					# we need to insert new row. If a row exists then there is nothing to update, as value is contant 4.
					if not attr_minwidth :
						prod_minwidth = Product_attribute(
							product_id = row[0],
							name = "MIN-WIDTH",
							value = 4,
							display_as_filter = False
							)
						prod_minwidth.save()

					# MAX-WIDTH
					attr_maxwidth = Product_attribute.objects.filter(name__iexact = "MAX-WIDTH", product = prod).first()
					if attr_maxwidth :
						prod_maxwidth = Product_attribute(
							id = attr_maxwidth.id,
							product_id = row[0],
							name = "MAX-WIDTH",
							value = row[6],
							display_as_filter = False
							)
					else:
						prod_maxwidth = Product_attribute(
							product_id = row[0],
							name = "MAX-WIDTH",
							value = row[6],
							display_as_filter = False
							)
					
					prod_maxwidth.save()

					# MAX-HEIGHT
					attr_maxheight = Product_attribute.objects.filter(name__iexact = "MAX-HEIGHT", product = prod).first()
					if attr_maxheight :
						prod_maxheight = Product_attribute(
							id = attr_maxheight.id,
							product_id = row[0],
							name = "MAX-HEIGHT",
							value = row[7],
							display_as_filter = False
							)
					else:
						prod_maxheight = Product_attribute(
							product_id = row[0],
							name = "MAX-HEIGHT",
							value = row[7],
							display_as_filter = False
							)
					prod_maxheight.save()

					# ORIENTATION
					attr_orientation = Product_attribute.objects.filter(name__iexact = "ORIENTATION", product = prod).first()
					if attr_orientation :
						orientation = Product_attribute(
							id = attr_orientation.id,
							product_id = row[0],
							name = "ORIENTATION",
							value = row[8],
							display_as_filter = True
							)
					else :
						orientation = Product_attribute(
							product_id = row[0],
							name = "ORIENTATION",
							value = row[8],
							display_as_filter = True
							)
					orientation.save()

					# IMAGE-TYPE
					attr_imgtype = Product_attribute.objects.filter(name__iexact = "IMAGE-TYPE", product = prod).first()
					if attr_imgtype :
						prod_imgtype = Product_attribute(
							id = attr_imgtype.id,
							product_id = row[0],
							name = "IMAGE-TYPE",
							value = row[9],
							display_as_filter = True
							)
					else :
						prod_imgtype = Product_attribute(
							product_id = row[0],
							name = "IMAGE-TYPE",
							value = row[9],
							display_as_filter = True
							)
					prod_imgtype.save()

					# KEY-WORDS
					attr_kw = Product_attribute.objects.filter(name__iexact = "KEY-WORDS", product = prod).first()
					if attr_kw :
						prod_keywords = Product_attribute(
							id = attr_kw.id,
							product_id = row[0],
							name = "KEY-WORDS",
							value = row[13],
							display_as_filter = True
							)
					else :
						print('Keywords' + row[13] )
						prod_keywords = Product_attribute(
							product_id = row[0],
							name = "KEY-WORDS",
							value = row[13],
							display_as_filter = True
							)
					prod_keywords.save()
					
					'''						'''
					''' Insert Product Images '''
					'''						'''
					img_front = Product_image.objects.filter(image_type__iexact = "FRONT", product = prod).first()
					if img_front:
						prodimg_front = Product_image(
							image_id = img_front.image_id,
							product_id = row[0],
							image_type = "FRONT",
							url = row[11]
							)
					else :
						prodimg_front = Product_image(
							product_id = row[0],
							image_type = "FRONT",
							url = row[11]
							)					
					prodimg_front.save()
					
					img_thumbnail = Product_image.objects.filter(image_type__iexact = "THUMBNAIL", product = prod).first()
					if img_thumbnail:
						prodimg_thumbnail = Product_image(
							image_id = img_thumbnail.image_id,
							product_id = row[0],
							image_type = "THUMBNAIL",
							url = row[12]
						)
					else :
						prodimg_thumbnail = Product_image(
							product_id = row[0],
							image_type = "THUMBNAIL",
							url = row[12]
							)
					prodimg_thumbnail.save()

					'''					'''
					''' Categories 		'''
					'''					'''
					#get the category id
					prod_category = Product_category.objects.filter(name__iexact = row[14]).first()
					if prod_category is None:
						# Insert
						prod_cat = Product_category(
								store = ecom,
								name = row[14],
								description = '',
								background_image = '',
								parent = None,
								trending = False,
								url = '',
								featured_collection = False
						)
						prod_cat.save()
						prod_category = prod_cat
					
					prod_prod_cat = Product_product_category.objects.filter(product_id = row[0]).first()
					if prod_prod_cat :
						prod_cat = Product_product_category(
							id = prod_prod_cat.id,
							product_id = row[0],
							product_category = prod_category
						)
					else :
						prod_cat = Product_product_category(
							product_id = row[0],
							product_category = prod_category
						)
					prod_cat.save()					
						
					'''					'''
					''' Publisher Price '''
					'''					'''
					publisher = Publisher.objects.filter(publisher_id = row[1]).first()
					if not publisher:
						pub = 	Publisher( 
							publisher_id = row[1],
							publisher_name = row[2],
							publisher_group = 'GRP1'
						)
						pub.save()
						
					publ_price = Publisher_price.objects.filter(publisher_id = row[1], 
						print_medium_id = 'PAPER').first()
					if not publ_price:
					
						pub_price = Publisher_price (
							publisher_id = row[1],
							print_medium_id = 'PAPER',
							price_type_id = 'SQIN',
							price = 10.50
						)

						pub_price.save()	

					publ_price = Publisher_price.objects.filter(publisher_id = row[1], 
						print_medium_id = 'CANVAS').first()
					if not publ_price:
					
						pub_price = Publisher_price (
							publisher_id = row[1],
							print_medium_id = 'CANVAS',
							price_type_id = 'SQIN',
							price = 12.50
						)

						pub_price.save()	

					
			cnt = cnt + 1
			print(cnt)
			
			if cnt > 100000:
				break
				
	return render(request, "eStore/import_image_data.html")
	
	
def deleteRemovedImageData(request):

	# Get all products
	prods = Product.objects.all().values('product_id')
	
	file = 'C:/eCom_Platform/project/eComPlatform/eStore/static/image_data/pod_data.csv'
	cnt = 0

	with open(file, encoding="utf8") as csvfile:

		readCSV = csv.reader(csvfile, delimiter=',')

		
		for row in readCSV:	
			if int(row[0]) in prods:
				None
			else:
				# Set product is_published to false
				prod = Product(
						store = ecom,
						product_id = int(row[0]),
						name = row[4],
						description = '',
						price = 0,
						available_on = today,
						updated_at = today,
						part_number = row[3],
						product_type = prod_type,
						is_published = False,
						charge_taxes = True,
						tax = prod_tax,
						tax_rate = tax_rate,
						featured = False,
						has_variants = False,
						size = None,
						default_frame = None
					)
				prod.save()
					
				
			
			cnt = cnt + 1
			print(cnt)
		
	return render(request, "eStore/delete_image_data.html")