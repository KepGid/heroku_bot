# -*- coding: utf-8 -*-

from time import time
from datetime import datetime
import requests
import matplotlib.pyplot as plt


def create_chart(name_currency):

    url = "https://fxmarketapi.com/apitimeseries"

    # check what day it was
    if datetime.today().weekday() >= 5:
        workday_time = time()
        while datetime.fromtimestamp(workday_time).weekday() >= 5:
            workday_time = workday_time - 3600
        # since currencies are not traded on a weekend, we get the previous working day
        start_date = str(datetime.fromtimestamp(workday_time - 604800).strftime("%Y-%m-%d"))
        end_date = str(datetime.fromtimestamp(workday_time).strftime("%Y-%m-%d"))

    else:
        # we form the date in the required format for the request
        start_date = str(datetime.fromtimestamp(time() - 604800).strftime("%Y-%m-%d"))  # date 7 days ago
        end_date = str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d"))  # The current date

    querystring = {"api_key": "gMEf0GH5_3_dEHnsCW2I", "currency": name_currency, "start_date": start_date,
                   "end_date": end_date, "format": "ohlc"}

    response = requests.get(url, params=querystring)

    try:
        dict_time_series = response.json().pop('price')

    except KeyError:
        return -1

    # we form data for building a graph
    date = []
    price = []

    for i in dict_time_series:
        date.append(i)  # get data
        price.append(dict_time_series.get(i).get(name_currency).get('close'))  # get price

    plt.plot(date, price)  # building a graph

    plt.xlabel('Data', fontsize=15)
    plt.ylabel('Price', fontsize=15)
    plt.title(name_currency+' chart price ', fontsize=17)
    plt.savefig('chart.png')
    plt.close()

    return 0
