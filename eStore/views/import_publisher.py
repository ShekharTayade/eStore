from eStore.models import Publisher_price, Publisher
import csv

from django.contrib.staticfiles.templatetags.staticfiles import static
from datetime import datetime
import datetime
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from decimal import Decimal

def importPublisherGroup(): 

	file = 'C:/eCom_Platform/project/MASTER DATA/publisher.txt'
	cnt = 0

	with open(file, encoding="utf8") as csvfile:

		readCSV = csv.reader(csvfile, delimiter='	')
		
		for row in readCSV:
			print(row[0])
			# Skip the first row (header)
			if cnt == 0:
				cnt = cnt + 1
				continue
 
			if row[0]:
				p = Publisher (
					publisher_id = int(row[0]),
					publisher_name = row[1],
					publisher_group = row[2]
				)
				p.save()


def importPublisherPrice(): 

	file = 'C:/eCom_Platform/project/MASTER DATA/publisher_price.txt'
	cnt = 0

	with open(file, encoding="utf8") as csvfile:

		readCSV = csv.reader(csvfile, delimiter='	')
		
		for row in readCSV:
			print(row[4])
			# Skip the first row (header)
			if cnt == 0:
				cnt = cnt + 1
				continue
 
			if row[0]:
				p = Publisher_price (
					publisher_price_id = int(row[3]),
					publisher_id = int(row[4]),
					print_medium_id = row[2],
					price_type_id = row[0],
					price = Decimal(row[1])
				)
				p.save()				
	
			
				
				
				
				