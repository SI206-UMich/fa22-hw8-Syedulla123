import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_filename)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as row_count FROM restaurants")
    row_count = cur.fetchall()[0][0]
    restaurants_lst = []

    for x in range(row_count):
        dict = {}
        cur.execute("SELECT name, category_id, building_id, rating FROM restaurants")
        data = cur.fetchall()[x]
        dict['name'] = restaurant[0]
        dict['category'] = restaurant[1]
        dict['building'] = restaurant[2]
        dict['rating'] = restaurant[3]

        cur.execute("SELECT category FROM categories WHERE id = ?", (dict["category"],))
        d["category"] = cur.fetchall()[0][0]
        cur.execute("SELECT building FROM buildings WHERE id = ?", (dict["building"],))
        d["building"] = cur.fetchall()[0][0]

        restaurants_lst.append(dict)

    return restaurants_lst

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    
    restaurant_categories = []
    lst = []

    cur.execute("SELECT category_id FROM restaurants")
    for row in cur:
        restaurant_categories.append(row[0])

    for id in restaurant_categories:
        cur.execute("SELECT category FROM restaurants.categories WHERE id = ?", (id, ))
        for row in cur:
            lst.append(row[0])

    lst = sorted(lst)
    category_dict = {}
    for key in lst:
        if key not in category_dict:
            category_dict[key] = 1
        else:
            category_dict[key] += 1
    
    sorted_category_dict = sorted(category_dict.items(), key = lambda item : item[1], reverse = True)
    sorted_category_dict = dict(sorted_category_dict)

    y-axis = list(sorted_category_dict.values())
    x-axis = list(sorted_category_dict.keys())
    plt.title("Types of Restaurants on South University Ave")
    plt.ylabel("Restaurant Categories")
    plt.xlabel("Number of Restaurants")
    plt.barh(y,x)
    plt.show()

    return sorted_category_dict

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
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
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
