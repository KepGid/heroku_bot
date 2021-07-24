# -*- coding: utf-8 -*-

import sqlite3 as sql


# getting a price for the specified currency
def get_price(currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM currency WHERE currency=?", (currency.upper(),))
    three_results = cur.fetchall()
    cur.close()

    if not three_results:  # check for a non-empty list
        return -1

    price = three_results[0][1]  # getting a price

    return price


#  getting the time of the last update
def get_time():

    con = sql.connect('currencies.db')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM currency WHERE currency=?", ('CAD',))
        three_results = cur.fetchall()
        cur.close()

        if not three_results:  # check for a non-empty list
            return -1

        time = three_results[0][2]   # getting the time

        return time

    except sql.OperationalError:
        return 0
