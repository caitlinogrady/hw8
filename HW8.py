# Your name: Caitlin O'Grady
# Your student id: 6885 0080
# Your email: ceogrady@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
	"""
	This function accepts the file name of a database as a parameter and returns a nested
	dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
	and each inner key is a dictionary, where the key:value pairs should be the category, 
	building, and rating for the restaurant.
	"""
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	cur.execute('SELECT * FROM restaurants')
	outer = {}
	li = []
	for row in cur:
		inner = {}
		name = row[1]
		cat = row[2]
		buil = row[3]
		rat = row[4]
		t = [name,cat,buil,rat]
		li.append(t)
		#print(t)
	for rest in li:
		inner = {}
		cur.execute('SELECT category FROM categories WHERE id = ?',(rest[1],))
		cat = cur.fetchone()
		
		inner['category'] = cat[0]
		cur.execute('SELECT building FROM buildings WHERE id = ?',(rest[2],))
		
		buil = cur.fetchone()
		
		inner['building'] = buil[0]
		
		inner['rating'] = rest[3]
		outer[rest[0]] = inner
		
		
	return outer

def plot_rest_categories(db):
	"""
	This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
	restaurant categories and the values should be the number of restaurants in each category. The function should
	also create a bar chart with restaurant categories and the count of number of restaurants in each category.
	"""
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	cur.execute('SELECT * FROM categories')
	li = []
	d = {}
	for row in cur:
		cat = row[1]
		id = row[0]
		tu = (id,cat)
		li.append(tu)
	for cat in li:
		cur.execute('SELECT COUNT(category_id) FROM restaurants WHERE category_id = ?',(cat[0],))
		count = cur.fetchone()
		d[cat[1]] = count[0]
	x = []
	y = []
	newt = []
	for c,num in d.items():
		newt.append((c,num))
	new = sorted(newt, key = lambda x:x[1])
	for t in new:
		x.append(t[0])
		y.append(t[1])
		
	plt.barh(x,y)
	plt.xlabel("Number of Restaurants")
	plt.ylabel("Categories")
	plt.title("Number of Restaurants in Each Category")
	
	plt.show()
	
	return d

def find_rest_in_building(building_num, db):
	'''
	This function accepts the building number and the filename of the database as parameters and returns a list of 
	restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
	should be sorted by their rating from highest to lowest.
	'''
	
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	cur.execute('SELECT id FROM buildings WHERE building = ?',(building_num,))
	num = cur.fetchone()
	print(num)
	cur.execute('SELECT name,rating FROM restaurants WHERE building_id = ?',(num[0],))
	li = []
	for rest in cur:
		li.append(rest)
	sort = sorted(li, key = lambda x:x[1],reverse=True)
	fi = []
	for s in sort:
		fi.append(s[0])
	return fi

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
	"""
	This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
	and the average rating of the restaurants in that category, and the second tuple contains the building number 
	which has the highest rating of restaurants and its average rating.

	This function should also plot two barcharts in one figure. The first bar chart displays the categories 
	along the y-axis and their ratings along the x-axis in descending order (by rating).
	The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
	in descending order (by rating).
	"""
	pass

#Try calling your functions here
def main():
	load_rest_data("South_U_Restaurants.db")
	plot_rest_categories("South_U_Restaurants.db")
	find_rest_in_building(1300,"South_U_Restaurants.db")

class TestHW8(unittest.TestCase):
	def setUp(self):
		self.rest_dict = {
			'category': 'Cafe',
			'building': 1101,
			'rating': 3.8
		}
		self.cat_dict = {
			'Asian Cuisine ': 2,
			'Bar': 4,
			'Bubble Tea Shop': 2,
			'Cafe': 3,
			'Cookie Shop': 1,
			'Deli': 1,
			'Japanese Restaurant': 1,
			'Juice Shop': 1,
			'Korean Restaurant': 2,
			'Mediterranean Restaurant': 1,
			'Mexican Restaurant': 2,
			'Pizzeria': 2,
			'Sandwich Shop': 2,
			'Thai Restaurant': 1
		}
		self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

	def test_load_rest_data(self):
		rest_data = load_rest_data('South_U_Restaurants.db')
		self.assertIsInstance(rest_data, dict)
		self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
		self.assertEqual(len(rest_data), 25)

	def test_plot_rest_categories(self):
		cat_data = plot_rest_categories('South_U_Restaurants.db')
		self.assertIsInstance(cat_data, dict)
		self.assertEqual(cat_data, self.cat_dict)
		self.assertEqual(len(cat_data), 14)

	def test_find_rest_in_building(self):
		restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
		self.assertIsInstance(restaurant_list, list)
		self.assertEqual(len(restaurant_list), 3)
		self.assertEqual(restaurant_list[0], 'BTB Burrito')

	#def test_get_highest_rating(self):
		#highest_rating = get_highest_rating('South_U_Restaurants.db')
		#self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
	main()
	unittest.main(verbosity=2)
