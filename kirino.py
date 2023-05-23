import random
import sys
import time
import json

import config
import solaris as solaris_japan

with open("figures.json") as json_file:
	figures = json.load(json_file)

if "--scrape" in sys.argv or "-s" in sys.argv:
	for figure in figures:
		if "Solaris Japan" in figures[figure]["Shops"]:
			solaris = solaris_japan.Solaris(figures[figure]["Shops"]["Solaris Japan"]["URL"])
			solaris.get_figure_page()
			time.sleep(5)
			solaris.get_figure_prices()
			solaris.get_shipping_prices()
			if "--solaris-image" in sys.argv or "-simg" in sys.argv:
				solaris.download_image()
			solaris.driver.close()

			figures[figure]["Image"] = solaris.image_filename
			figures[figure]["Shops"]["Solaris Japan"]["New"] = solaris.new_price
			figures[figure]["Shops"]["Solaris Japan"]["Used"] = solaris.used_price
			figures[figure]["Shops"]["Solaris Japan"]["Shipping"] = solaris.shipping

			with open("figures.json", "w") as json_file:
				json.dump(figures, json_file, indent=4)
			time.sleep(random.randint(20, 60))

if "--manufacturer" in sys.argv or "-mf" in sys.argv:
	manufacture_count = {}
	for figure in figures:
		if "," in figures[figure]["Manufacturer"]:
			for manufacturer in figures[figure]["Manufacturer"].split(","):
				if manufacturer in manufacture_count:
					manufacture_count[manufacturer] += 1
				else:
					manufacture_count[manufacturer] = 1
		else:
			manufacturer = figures[figure]["Manufacturer"]
			if manufacturer in manufacture_count:
				manufacture_count[manufacturer] += 1
			else:
				manufacture_count[manufacturer] = 1
	print("Manufacturers:")
	print(manufacture_count)

print()

if "--shops" in sys.argv or "-sh" in sys.argv or "--stores" in sys.argv:
	stores = {}
	for figure in figures:
		for store in figures[figure]["Shops"]:
			if store in stores:
				stores[store] += 1
			else:
				stores[store] = 1
	print("Shops:")
	print(stores)

print()

if "--characters" in sys.argv or "-ch" in sys.argv:
	characters = {}
	for figure in figures:
		character = figures[figure]["Character"]
		if character in characters:
			characters[character] += 1
		else:
			characters[character] = 1
	print("Characters:")
	print(characters)