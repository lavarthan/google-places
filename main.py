import time
import os
from pprint import pprint
import requests
import json
from location import get_location
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def find_places(place, type, keyword, radius):
    if radius != '':
        lat, lng = get_location(place)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&nextPage()&keyword={}&key={}".format(
            lat, lng, radius, type, keyword, API_KEY)
        response = requests.get(url)
        res = json.loads(response.text)
    else:
        query = type + '+in+' + place.replace(', ', '+')
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}'.format(
            query,API_KEY)
        response = requests.get(url)
        res = res = json.loads(response.text)
    return res


print('Welcome to the place search system!')
print('* field are mandatory')


while True:
    n = input('Choose a method............\n1. Radius based search\n2. Query based search')
    place = input('Enter the place*: ')
    type = input('Enter the place type*: ')
    if n == '1':
        radius = input('Enter the search area radius(in meter)*: ')
    else:
        radius = ''
    keyword = input('Enter if you have any specified keyword: ')
    file = input('Enter file name*: ')

    output = []
    res = find_places(place, type, keyword, radius)
    page_available = True
    while page_available:
        print('getting.....')
        results = res['results']
        # print(len(results))

        for i in range(len(results)):
            name = results[i]['name']
            try:
                rating = results[i]['rating']
            except KeyError:
                rating = ''

            try:
                business_status = results[i]['business_status']
            except KeyError:
                business_status = ''

            try:
                types = ', '.join(results[i]['types'])
            except KeyError:
                types = ''

            try:
                user_ratings_total = results[i]['user_ratings_total']
            except KeyError:
                user_ratings_total = ''

            try:
                if n == '1':
                    address = results[i]['vicinity']
                elif n == '2':
                    address = results[i]['formatted_address']
            except KeyError:
                address = ''

            output.append([name, address, types, business_status, rating, user_ratings_total])

        try:
            next_page_token = res['next_page_token']
            # print(next_page_token)
            if n == '1':
                url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'.format(
                    next_page_token, API_KEY)
            elif n=='2':
                url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={}&key={}'.format(next_page_token,API_KEY)
            # print(url)
            time.sleep(5)
            response = requests.get(url)
            res = json.loads(response.text)
            # print([*res])
            page_available = True
        except:
            page_available = False

    df = pd.DataFrame(
        columns=['name', 'address', 'types', 'business_status', 'rating', 'user_ratings_total'])
    df = df.append(pd.DataFrame(output, columns=['name', 'address', 'types', 'business_status', 'rating',
                                                 'user_ratings_total']))

    df.to_csv('output/{}'.format(file), index_label='No.')

    print("DONE!\n")
