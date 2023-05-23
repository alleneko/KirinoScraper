import time
import urllib.request as urllib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import config

class Solaris:
	def __init__(self, url):
		self.shipping_setting = config.solaris_shipping
		self.base_url = "https://solarisjapan.com/products/"
		self.url = url if self.base_url in url else self.base_url + url
		self.new_price = 0
		self.used_price = 0
		self.shipping = 0

	def get_figure_page(self):
		self.driver = webdriver.Firefox()
		self.driver.get(self.url)

	def get_figure_prices(self):
		prices = self.driver.find_elements(By.CSS_SELECTOR, ".btn.btn__main-content")
		for price in prices:
			if config.brand_new and "brand new" in price.text.lower() and "sold out" not in price.text.lower():
				new_price = price.text.split("\n")[-1]
				self.new_price = float(new_price.replace("$", ""))
			elif config.pre_owned and "pre owned" in price.text.lower() and "sold out" not in price.text.lower():
				used_price = price.text.split("\n")[-1]
				self.used_price = float(used_price.replace("$", ""))

	def get_shipping_prices(self):
		shipping = self.driver.find_elements(By.CSS_SELECTOR, ".shipment__block")
		for ship in shipping:
			if config.solaris_shipping == "Regular" and "Regular" in ship.text:
				ship_button = ship
			elif config.solaris_shipping == "Saver" and "Saver" in ship.text:
				ship_button = ship
			elif config.solaris_shipping == "Express" and "Express" in ship.text:
				ship_button = ship
		self.shipping = float(ship_button.text.split("\n")[-1].replace("$", ""))

	def download_image(self):
		image = self.driver.find_elements(By.CSS_SELECTOR, ".fade-in.lazyautosizes.lazyloaded")[0]
		image.click()
		time.sleep(2)
		image = self.driver.find_elements(By.CSS_SELECTOR, ".pswp__img")[-1]
		image_url = image.get_attribute("src")
		file_type = image_url.split(".")[-1].split("?")[0]
		file_type = "." + file_type
		self.image_filename = image_url.split("/")[-1].split(".")[0] + file_type
		urllib.urlretrieve(image_url, self.image_filename)