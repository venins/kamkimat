from django.db import models

#Flipkart mobile category
class FlipkartMobile(models.Model):
	product_name = models.CharField(max_length=200)
	product_sub_name = models.CharField(max_length=200, blank=True)
	product_u_id = models.CharField(max_length=200, unique=True)
	product_m_id = models.CharField(max_length=200, blank=True)
	product_availability = models.BooleanField()
	product_price = models.CharField(max_length=200)
	product_desc = models.CharField(max_length=1000, blank=True)
	product_specifications= models.CharField(max_length=10000, blank=True)
	product_url = models.CharField(max_length=1000)
	product_scrape_time = models.DateTimeField('Last Update time')
	product_img_url = models.CharField(max_length=1000)

	def __str__(self):
		return self.product_name
