#!/usr/bin/env python3

import json
import sqlite3
import time

import requests


def buy(ticker_symbol, trade_volume):

    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
    response = json.loads(requests.get(deep_link).text)

    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    last_price = response['LastPrice']

    cursor.execute('SELECT balance FROM users;')
    balance = cursor.fetchall()[0][0]

    friction = 8.00 # Amount of money it costs to make a trade per trade

    transaction_cost = (int(trade_volume) * float(last_price)) + friction
    unix_time = time.time()
    transaction_type = 1

    if transaction_cost > balance:
        return 'You have insufficient funds'
    else:
        new_balance = balance - transaction_cost
        cursor.execute('UPDATE users SET balance = {new_balance};'.format(new_balance=new_balance))
        connection.commit()

        cursor.execute('INSERT INTO transactions(unix_time, ticker_symbol, transaction_type, last_price, trade_volume) VALUES({0}, "{1}", {2}, {3}, {4});'.format(unix_time, ticker_symbol, transaction_type, last_price, int(trade_volume)))
        connection.commit()

        cursor.execute('SELECT ticker_symbol FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
        position_exists = cursor.fetchone()

        if position_exists is None:
            cursor.execute('INSERT INTO positions(ticker_symbol, number_of_shares, volume_weighted_adjusted_price) VALUES("{ticker_symbol}", {number_of_shares}, {volume_weighted_adjusted_price});'.format(ticker_symbol=ticker_symbol, number_of_shares=int(trade_volume), volume_weighted_adjusted_price = last_price))
            connection.commit()

        else:
            cursor.execute('SELECT number_of_shares FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
            current_holdings = cursor.fetchall()[0][0]
            new_holdings = int(current_holdings) + int(trade_volume)

            cursor.execute('UPDATE positions SET number_of_shares = {number_of_shares};'.format(number_of_shares=new_holdings))
            connection.commit()

            cursor.execute('SELECT volume_weighted_adjusted_price FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))

            old_vwap = cursor.fetchall()[0][0]
            new_vwap = ((int(trade_volume) * last_price)+(current_holdings * old_vwap)) / new_holdings 

            cursor.execute('UPDATE positions SET volume_weighted_adjusted_price = {volume_weighted_adjusted_price};'.format(volume_weighted_adjusted_price=new_vwap))
            connection.commit()

            cursor.close()
            connection.close()
        return 'Trade is complete'

def sell(ticker_symbol, trade_volume):

    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
    response = json.loads(requests.get(deep_link).text)

    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    last_price = response['LastPrice']

    cursor.execute('SELECT balance FROM users;')
    balance = cursor.fetchall()[0][0]

    friction = 8.00 # Amount of money it costs to make a trade per trade

    transaction_cost = friction
    new_balance = balance + (last_price * int(trade_volume)) - transaction_cost

    unix_time = time.time()
    transaction_type = 0

    if transaction_cost > balance:
        return 'You have insufficient funds'
    else:
        cursor.execute('SELECT number_of_shares FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
        current_holdings = cursor.fetchall()

        if len(current_holdings) < 1:
            return 'You don\'t have any shares to sell'
        else:
            current_holdings = current_holdings[0][0]

        new_holdings = current_holdings - int(trade_volume)

        cursor.execute('INSERT INTO transactions(unix_time, ticker_symbol, transaction_type, last_price, trade_volume) VALUES({0}, "{1}", {2}, {3}, {4});'.format(unix_time, ticker_symbol, transaction_type, last_price, int(trade_volume)))
        connection.commit()

        cursor.execute('SELECT ticker_symbol FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
        position_exists = cursor.fetchone()

        if position_exists is None or int(trade_volume) > current_holdings:
            return 'You don\'t have any shares to sell'

        else:

            cursor.execute('UPDATE positions SET number_of_shares = {number_of_shares};'.format(number_of_shares=new_holdings))
            connection.commit()

            cursor.execute('SELECT volume_weighted_adjusted_price FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))

            old_vwap = cursor.fetchall()[0][0]

            if new_holdings == 0:
                new_vwap = 0.0
            else:
                new_vwap = ((int(trade_volume) * last_price)+(current_holdings * old_vwap)) / new_holdings

            cursor.execute('UPDATE positions SET volume_weighted_adjusted_price = {volume_weighted_adjusted_price};'.format(volume_weighted_adjusted_price=new_vwap))
            connection.commit()

            cursor.execute('UPDATE users SET balance = {new_balance};'.format(new_balance=new_balance))
            connection.commit()

            cursor.close()
            connection.close()
        return 'Trade is complete'

def lookup(company_name):
    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input={company_name}'.format(company_name=company_name)
    response = json.loads(requests.get(deep_link).text)
    ticker_symbol = response[0]['Symbol']
    return ticker_symbol


def quote(ticker_symbol):
    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
    response = json.loads(requests.get(deep_link).text)
    last_price = response['LastPrice']
    return last_price

def portfolio(balance):
    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    cursor.execute('SELECT balance FROM users;')
    balance = cursor.fetchall()[0][0]
    return 'Current balance is' ,balance

    cursor.close()
    connection.close()

def pl(p):

    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    friction = 12

    cursor.execute('SELECT balance FROM users;')
    bal= cursor.fetchall()[0][0]
    
    cursor.execute('SELECT count(*) from transactions;')
    vol= cursor.fetchall()[0][0]

    cursor.execute('SELECT number_of_shares FROM positions;')
    posvol = cursor.fetchall()[0][0]
    
    cursor.execute('SELECT volume_weighted_adjusted_price FROM positions JOIN transactions WHERE transaction_type == 0;')
    sale = cursor.fetchall()[0][0]
  
    cursor.execute('SELECT volume_weighted_adjusted_price FROM positions JOIN transactions WHERE transactions.transaction_type == 1;')
    buy = cursor.fetchall()[0][0]
        
    x = ((buy) - (sale)) - (friction * vol)
    
    if sale > buy:
        return 'You made a profit of', x
    else:
        return  'You have a loss of', x

    cursor.close()
    connection.close()
