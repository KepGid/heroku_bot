# -*- coding: utf-8 -*-

import telebot
from requests import post
from time import time


import config
from command_list import command_list
from create_bd import create_and_update
from parsing_currencies import parsing_currencies
from get_price_and_time import get_price, get_time
from command_chart import create_chart


bot = telebot.TeleBot(config.token)

# default USD to USD ratio
price_base_currency = 1
price_second_currency = 1
command_base_currency = False
command_second_currency = False
name_base_currency = 'USD'
name_second_currency = 'USD'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello, i will help convert one currency to another currency.'
                                      '\nBase currency USD '
                                      '\nCommand list:'
                                      '\n/list - display a list of all currencies and their exchange rates;'
                                      '\n/basecurrency  - change base currency; '
                                      '\n/quotedcurrency - change the quoted currency;'
                                      '\n/chart - will show the price chart for the last 7 days;'
                                      '\n/help - detailed information about commands and how to use them;')
    create_and_update(parsing_currencies())


@bot.message_handler(commands=['list'])
def send_list_currencies(message):
    update_bd()  # if more than 10 minutes have passed then update the local database
    bot.send_message(message.chat.id, '\n'.join(command_list()))


@bot.message_handler(commands=['basecurrency'])
def command_base_currency(message):
    global command_base_currency
    command_base_currency = True
    bot.send_message(message.chat.id, 'Enter the name of the base currency')


@bot.message_handler(commands=['quotedcurrency'])
def command_quoted_currency(message):
    global command_second_currency
    command_second_currency = True
    bot.send_message(message.chat.id, 'Enter the name of the quoted currency')


@bot.message_handler(commands=['chart'])
def send_chart(message):
    global name_base_currency
    global name_second_currency

    update_bd()  # if more than 10 minutes have passed then update the local database

    name_chart = name_base_currency + name_second_currency

    if create_chart(name_chart) != -1:
        url = "https://api.telegram.org/bot" + config.token + "/sendPhoto"
        files = {'photo': open('chart.png', 'rb')}
        data = {'chat_id': message.chat.id}
        r = post(url, files=files, data=data)
    else:
        bot.send_message(message.chat.id, 'No exchange rate data is available for the selected currency')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, '\nCommand list:'
                                      '\n/list - display a list of all currencies and their exchange rates;'
                                      '\n/basecurrency   - to change the base currency; '
                                      '\n/quotedcurrency - to change the quoted currency; '
                                      '\n/chart - will show the price chart for the '
                                      'current currency pair for the last 7 days;')


@bot.message_handler(commands=['stop'])
def command_help(message):
    global price_base_currency
    global price_second_currency
    global command_second_currency
    global command_base_currency
    global name_base_currency
    global name_second_currency

    price_base_currency = 1
    price_second_currency = 1
    command_base_currency = False
    command_second_currency = False
    name_base_currency = 'USD'
    name_second_currency = 'USD'

    bot.send_message(message.chat.id, 'goodbye')


@bot.message_handler(content_types=['text'])
def convert(message):
    global price_base_currency
    global price_second_currency
    global command_second_currency
    global command_base_currency
    global name_base_currency
    global name_second_currency

    update_bd()  # if more than 10 minutes have passed then update the local database

    if command_base_currency:
        name_currency = message.text.replace(' ', '').upper()

        if name_currency.upper() == 'USD':
            price_base_currency = 1
        else:
            price_base_currency = get_price(name_currency)

        # checking if there is such a currency
        if price_base_currency != -1:
            name_base_currency = name_currency

            bot.send_message(message.chat.id, 'Currency pair '
                                              ''+name_base_currency+name_second_currency+'\nEnter the amount:')
            command_base_currency = False
        else:
            bot.send_message(message.chat.id, 'There is no such currency')

    elif command_second_currency:
        name_currency = message.text.replace(' ', '').upper()

        if name_currency == 'USD':
            price_second_currency = 1
        else:
            price_second_currency = get_price(name_currency)

        # checking if there is such a currency
        if price_second_currency != -1:
            name_second_currency = name_currency

            bot.send_message(message.chat.id, 'Currency pair '
                                              ''+name_base_currency+name_second_currency+'\nEnter the amount:')
            command_second_currency = False
        else:
            bot.send_message(message.chat.id, 'There is no such currency')

    else:
        if is_number(message.text):

            number = float(message.text)

            # obtaining the ratio of the first currency to the second
            coefficient = price_second_currency / price_base_currency
            # convert currencies
            amount = number * coefficient

            if amount > 1:
                text_message = name_base_currency+' : '+str('%.2f' % number) + \
                               '\n'+name_second_currency + ' : ' + str('%.2f' % float(amount))
            else:
                text_message = name_base_currency+' : '+str('%.2f' % number) + \
                               '\n'+name_second_currency + ' : ' + str('%.6f' % float(amount))
            bot.send_message(message.chat.id, text_message)

        else:
            text = 'incorrect number entered'
            bot.send_message(message.chat.id, text)


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


# function to check the last update of the exchange rate,
# if more than 10 minutes have passed since the last update, then update the database
def update_bd():
    timestamp = get_time()
    if (time() - timestamp) >= 600:
        create_and_update(parsing_currencies())


if __name__ == '__main__':
     bot.infinity_polling()
