#!/usr/bin/python
import sys
import os
import django
import requests
import json
import re

sys.path.append("/home/vishal/kamkimat/kamkimat")
os.environ["DJANGO_SETTINGS_MODULE"] = "kamkimat.settings"
django.setup()

from scrapper.models import FlipkartMobile

#base url of search and productinfo apis
search_api_url = "http://mobileapi.flipkart.net/2/discover/getSearch?store=tyy,4io&start="
product_info_url = "http://mobileapi.flipkart.net/2/discover/productInfo/0?pids="
base_url = "http://www.flipkart.com"

#function to search list of products from start number to total(count) to fetch
def search_product(start=0, count=10):
	search_mobiles = requests.get(search_api_url + str(start) + "&count=" + str(count), headers = {"X-User-Agent":"Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Browser-Name" : "Mobile Safari", "Accept-Encoding" : "gzip", "User-Agent" : "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Content-Length" : 0})
	#search_mobiles_json = json.loads(search_mobiles.content)
	search_mobiles_json = search_mobiles.json()
	if search_mobiles_json["STATUS_CODE"] == 200:
		return search_mobiles_json
	else:
		return search_mobiles_json["STATUS_CODE"]

#function to return product info by id
def product_info(product_id):
	product_info = requests.get(product_info_url + str(product_id), headers = {"X-User-Agent":"Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Browser-Name" : "Mobile Safari", "Accept-Encoding" : "gzip", "User-Agent" : "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Content-Length" : 0})
	#product_info_json = json.loads(product_info.content)
	product_info_json = product_info.json()
	if product_info_json["STATUS_CODE"] == 200:
		return product_info_json
	else:
		return product_info_json["STATUS_CODE"]

#total number of products available in mobile category
total_product_data = search_product()
total_product = total_product_data["RESPONSE"]["search"]["metadata"]["totalProduct"]

#start point for loop for fetching list of products
#we can set this anything product list start fetching from this number
print total_product