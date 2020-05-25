"""
author: Stella Zhu
"""

import requests
from US_city_extracter import city_locator
import csv

google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
api_key = "***"


def restaurants_searcher(state_name, city_name):
    """
    search for opening status of restaurants in a particular city in US
    :param state_name: case-insensitive state_name
    :param city_name: case-insensitive city_name
    :return: a dictionary with restaurants as keys and opening status as values
    """
    state_city_location_dict = city_locator()
    location_tup = state_city_location_dict[state_name][city_name]
    city_url = google_url + "location=" + location_tup[0] + "," + location_tup[1] \
               + "&radius=1500" \
               + "&type=restaurant" \
               + "&key=" + api_key
    response = requests.get(city_url)
    city_restaurants_info = response.json()
    result = {}
    for restaurant in city_restaurants_info["results"]:
        name = restaurant["name"]
        lat = restaurant["geometry"]["location"]["lat"]
        lng = restaurant["geometry"]["location"]["lng"]
        try:
            opening = restaurant["opening_hours"]["open_now"]
            result[name] = [opening, lat, lng]
        except:
            result[name] = [None, lat, lng]
    print(city_url)
    return result


def restaurants_csv_generater(state_name, city_name):
    if " " not in state_name:
        state_name = state_name[0].upper() + state_name[1:].lower()
    else:
        state_name = state_name.split()
        state_name[0] = state_name[0][0].upper() + state_name[0][1:].lower()
        state_name[1] = state_name[1][0].upper() + state_name[1][1:].lower()
        state_name = " ".join(state_name)
    if " " not in city_name:
        city_name = city_name[0].upper() + city_name[1:].lower()
    else:
        city_name = city_name.split()
        city_name[0] = city_name[0][0].upper() + city_name[0][1:].lower()
        city_name[1] = city_name[1][0].upper() + city_name[1][1:].lower()
        city_name = " ".join(city_name)

    with open("restaurants.csv", "w") as fout:
        fieldnames = ['city', 'restaurant', 'opening_status', 'latitude', 'longitude']
        dw = csv.DictWriter(fout, fieldnames)
        dw.writeheader()
        restaurants_info = restaurants_searcher(state_name, city_name)
        dw.writerows([{fieldnames[0]: city_name,
                       fieldnames[1]: restaurant,
                       fieldnames[2]: restaurants_info[restaurant][0],
                       fieldnames[3]: restaurants_info[restaurant][1],
                       fieldnames[4]: restaurants_info[restaurant][2]}
                      for restaurant in restaurants_info])


if __name__ == "__main__":
    restaurants_csv_generater("new york", "washingtonville")
