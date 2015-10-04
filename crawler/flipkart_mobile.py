#!/usr/bin/python
import datetime
import requests
import json
import MySQLdb
import re
import sys
import pytz

#base url of search and productinfo apis
search_api_url = "http://mobileapi.flipkart.net/2/discover/getSearch?store=tyy,4io&start="
product_info_url = "http://mobileapi.flipkart.net/2/discover/productInfo/0?pids="
base_url = "http://www.flipkart.com"

#function to search list of products from start number to total(count) to fetch
def search_product(start=0, count=10):
	search_mobiles = requests.get(search_api_url + str(start) + "&count=" + str(count), headers = {"X-User-Agent":"Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Browser-Name" : "Mobile Safari", "Accept-Encoding" : "gzip", "User-Agent" : "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Content-Length" : 0})
	search_mobiles_json = json.loads(search_mobiles.content)
	if search_mobiles_json["STATUS_CODE"] == 200:
		return search_mobiles_json
	else:
		return search_mobiles_json["STATUS_CODE"]

#function to return product info by id
def product_info(product_id):
	product_info = requests.get(product_info_url + str(product_id), headers = {"X-User-Agent":"Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Browser-Name" : "Mobile Safari", "Accept-Encoding" : "gzip", "User-Agent" : "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-S7582 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 FKUA/Retail/610200/Android/Mobile (samsung/GT-S7582/a84f0c65442bc4a19acf65384b6e1a76)", "Content-Length" : 0})
	product_info_json = json.loads(product_info.content)
	if product_info_json["STATUS_CODE"] == 200:
		return product_info_json
	else:
		return product_info_json["STATUS_CODE"]

#total number of products available in mobile category
total_product_data = search_product()
total_product = total_product_data["RESPONSE"]["search"]["metadata"]["totalProduct"]

#start point for loop for fetching list of products
#we can set this anything product list start fetching from this number
start = 0

#connecting database
db = MySQLdb.connect("localhost", "kamkimat", "kamkimat", "kamkimat")
cursor = db.cursor()

#loop start from startpoint to less than total products
while start < total_product:
	try:

		mobile_search_data = search_product(start)
		if type(mobile_search_data) == dict:
			mobile_search_list = mobile_search_data["RESPONSE"]["search"]["storeSearchResult"]["tyy/4io"]["productList"]
			for product_id in mobile_search_list:
				product_data = product_info(product_id)
				if type(product_data) == dict:
					product_main_name = str(product_data["RESPONSE"]["productInfo"][product_id]["mainTitle"])
					product_sub_name = str(product_data["RESPONSE"]["productInfo"][product_id]["subTitle"])
					product_url = base_url + str(product_data["RESPONSE"]["productInfo"][product_id]["productPageUrl"])
					product_price = str(product_data["RESPONSE"]["productInfo"][product_id]["sellingPrice"])
					product_image = str(product_data["RESPONSE"]["productInfo"][product_id]["productAltImage"])
					if product_data["RESPONSE"]["productInfo"][product_id]["availabilityDetails"]["product.availability.status"] == "negative":
						product_status = 0
					else:
						product_status = 1
					try:
						product_offer_1 = str(product_data["RESPONSE"]["productInfo"][product_id]["offers"])
					except:
						product_offer_1 = str('[]')
					try:
						product_offer_2 = str(product_data["RESPONSE"]["productInfo"][product_id]["productOffer"])
					except:
						product_offer_2 = str('[]')
					product_specs = str(product_data["RESPONSE"]["productInfo"][product_id]["productSpecification"])
					try:
						product_key_specs = str(product_data["RESPONSE"]["productInfo"][product_id]["keySpecs"])
					except:
						product_key_specs = str('[]')
					sql_select = "SELECT * FROM scrapper_flipkartmobile WHERE product_u_id = %s"
					try:
						cursor.execute(sql_select,product_id)
						if cursor.rowcount > 0:
							sql_update = "UPDATE scrapper_flipkartmobile SET product_price = %s, product_availability = %s, product_offer_1 = %s, product_offer_2 = %s WHERE product_u_id = %s"
							data = ( product_price, product_status, product_offer_1, product_offer_2, product_id )
							try:
								cursor.execute(sql_update, data)
								db.commit()
								print "Updated %s " % product_id
							except Exception, e:
								print repr(e)
								db.rollback()
						else:

							sql = "INSERT INTO scrapper_flipkartmobile(`product_u_id`, `product_name`, `product_sub_name`, `product_url`, `product_availability`, `product_price`, `product_img_url`, `product_specifications`, \
								  `product_desc`, `product_offer_1`, `product_offer_2`, ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
							try:
								data = (product_id, product_main_name, product_sub_name, product_url, product_status, product_price, product_image, product_specs, product_key_specs, product_offer_1, product_offer_2)
								cursor.execute(sql,data)
								print "Added %s " % product_id
								db.commit()
							except Exception, e:
								print repr(e)
								db.rollback()
					except Exception, e:
						print repr(e)
						db.rollback()
		print start
		start = start + 10
	except:
		print "Unexpected error:", sys.exc_info()[0]