# -*- coding: utf-8 -*-

import sqlite3 as sql


def create_and_update(list_currency):
    con = sql.connect('currencies.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS currency (currency TEXT PRIMARY KEY, price REAL, time INTEGER);""")

    for i in list_currency:
        try:
            cur.execute(f"INSERT INTO currency VALUES (?,?,?)", i)
        except sql.IntegrityError:
            cur.execute('UPDATE currency SET price == ?, time == ? WHERE currency == ?', (i[1], i[2], i[0]))

    con.commit()
    cur.close()



