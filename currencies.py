__author__ = 'ubuntu'

import requests
import operator
from tabulate import tabulate

def get_data():
    """gets data from REST Countries, returns json"""
    r = requests.get('https://restcountries.eu/rest/v1/all')
    return r.json()

def get_currencies_data(r):
    """returns a dictioniary, keys (str) are currencies, values (int) are number of people using these currencies"""
    currencies_data = {}
    for country in r:
        for currency in country['currencies']:
            if currency in currencies_data:
                currencies_data[currency] += int(country['population'])
            else:
                currencies_data[currency] = int(country['population'])
    return currencies_data

def sort_data(data):
    """sorts a dictionary by its values, returns a tuple with tuples"""
    sorted_data = sorted(data.items(), key=operator.itemgetter(1))
    return tuple(reversed(sorted_data))

def pack_data(data, number_to_print):
    """returns data in pretty table, user sets how many records are printed"""
    table = [["Place", "Currency", "Users [millions]"], ["-----", "--------", "----------------"]]
    for index, item in enumerate(data):
        if index < number_to_print:
            table.append([index+1, item[0], round(item[1]/1000000,2)])
        else:
            break
    return tabulate(table)

def save_data(data):
    """saves data to 'results.txt'"""
    try:
        with open('results.txt', 'w') as file:
            file.write(data)
    except IOError:
        print("IOError!")

print(pack_data(sort_data(get_currencies_data(get_data())), 100))
save_data(pack_data(sort_data(get_currencies_data(get_data())), 100))