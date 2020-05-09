"""
author: Stella Zhu
"""

import requests
from US_city_extracter import city_locator

google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
api_key = "AIzaSyCQ1URNVCMsTp3bZAuIP0WG8Ljto28WEko"

us_county_code = "us"


def restaurants_searcher(state_name, city_name):
    """
    search for opening status of restaurants in a particular city in US
    :param state_name: case-insensitive state_name
    :param city_name: case-insensitive city_name
    :return: a dictionary with restaurants as keys and opening status as values
    """
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
        try:
            name = restaurant["name"]
            opening = restaurant["opening_hours"]["open_now"]
            result[name] = opening
        except:
            name = restaurant["name"]
            result[name] = None
    # print(city_url)
    return result


if __name__ == "__main__":
    print(restaurants_searcher("new york", "washingtonville"))