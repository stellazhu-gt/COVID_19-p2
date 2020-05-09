"""
author: Stella Zhu
"""

from bs4 import BeautifulSoup
import requests
import pymysql
from secret import password
import csv

city_data_url = "https://raw.githubusercontent.com/kelvins/US-Cities-Database/master/us_cities.sql"


# github source: https://github.com/kelvins/US-Cities-Database

def __database_generator():
    """
    private function DONT USE
    """
    response = requests.get(city_data_url)
    soup = BeautifulSoup(response.text, "html.parser").text
    with open("us_cities.sql", "w") as fout:
        fout.write(soup)


def __location_aggregator():
    """
    private function DONT USE
    """
    connection = pymysql.connect(host='localhost', user='root',
                                 password=password, charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        statement = "use US_LOCATIONS;"
        cursor.execute(statement)
        statement = "SELECT "\
                    + "US_CITIES.ID, US_STATES.STATE_CODE, US_STATES.STATE_NAME, "\
                    + "US_CITIES.CITY, US_CITIES.COUNTY, US_CITIES.LATITUDE, US_CITIES.LONGITUDE " \
                    + "FROM " \
                    + "US_STATES " \
                    + "INNER JOIN " \
                    + "US_CITIES " \
                    + "ON " \
                    + "US_STATES.ID = US_CITIES.ID_STATE " \
                    + "ORDER BY " \
                    + "US_CITIES.ID ASC " \
                    + "INTO OUTFILE " \
                    + "'US_Cities.csv' " \
                    + "FIELDS TERMINATED BY " \
                    + "';' "\
                    + "ENCLOSED BY " \
                    + "'' " \
                    + "LINES TERMINATED BY " \
                    + "'\\n';"
        cursor.execute(statement)
        connection.commit()
        connection.close()


def city_locator():
    """
    city_locator() is a function for external use
    :return: a dictionary with all states as keys and all belongs city location as the corresponding value
    location tuple: (LATITUDE, LONGITUDE)
    e.g. the value for "Georgia"
    {'Abbeville': ('31.96484', '-83.306845'), ...
     'Atlanta': ('33.749788', '-84.31685'), ...}
    """
    result = {}
    with open("US_Cities.csv", "r") as fin:
        reader = csv.reader(fin, delimiter=";")
        city_list = [list(line) for line in reader]
        for city in city_list:
            if city[2] not in result:
                # STATE: city[2]
                # CITY: city[3]
                # LATITUDE: city[5]
                # LONGITUDE: city[6]
                result[city[2]] = {city[3]: (city[5], city[6])}
            else:
                if city[3] not in result[city[2]]:
                    result[city[2]][city[3]] = (city[5], city[6])
    return result


if __name__ == "__main__":
    city_locator()
