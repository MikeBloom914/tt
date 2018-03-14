#!/usr/bin/env python3

import json
import sqlite3
import time
import requests
import os


def buy(ticker_symbol, trade_volume):

    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
    response = json.loads(requests.get(deep_link).text)

    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    last_price = response['LastPrice']

    cursor.execute('SELECT balance FROM users;')
    balance = cursor.fetchall()[0][0]

    friction = 12.00 # Amount of money it costs to make a trade per trade

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
            cursor.execute('INSERT INTO positions(ticker_symbol, number_of_shares, vwap) VALUES("{ticker_symbol}", {number_of_shares}, {vwap});'.format(ticker_symbol=ticker_symbol, number_of_shares=int(trade_volume), vwap = last_price))
            connection.commit()

        else:
            cursor.execute('SELECT number_of_shares FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
            current_holdings = cursor.fetchall()[0][0]
            new_holdings = int(current_holdings) + int(trade_volume)

            cursor.execute('UPDATE positions SET number_of_shares = {number_of_shares} WHERE ticker_symbol = "{ticker_symbol}";'.format(number_of_shares=new_holdings, ticker_symbol=ticker_symbol))
            connection.commit()

            cursor.execute('SELECT vwap FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
            old_vwap = cursor.fetchall()[0][0]
            
            new_vwap = ((int(trade_volume) * last_price)+(current_holdings * old_vwap)) / new_holdings 

            cursor.execute('UPDATE positions SET vwap = {vwap} WHERE ticker_symbol = "{ticker_symbol}";'.format(vwap=new_vwap, ticker_symbol=ticker_symbol))
            connection.commit()

            cursor.close()
            connection.close()
        return 'Trade is complete. You paid' , last_price,'on',trade_volume, ticker_symbol.upper()

def sell(ticker_symbol, trade_volume):

    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
    response = json.loads(requests.get(deep_link).text)

    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    last_price = response['LastPrice']

    cursor.execute('SELECT balance FROM users;')
    balance = cursor.fetchall()[0][0]

    friction = 12.00 # Amount of money it costs to make a trade per trade

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
        #new_holdings and current_holdings are correct

        cursor.execute('INSERT INTO transactions(unix_time, ticker_symbol, transaction_type, last_price, trade_volume) VALUES({0}, "{1}", {2}, {3}, {4});'.format(unix_time, ticker_symbol, transaction_type, last_price, int(trade_volume)))
        connection.commit()

        cursor.execute('SELECT ticker_symbol FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
        position_exists = cursor.fetchone()

        if position_exists is None or int(trade_volume) > current_holdings:
            return 'You don\'t have any shares to sell'

        else:
                            
            cursor.execute('UPDATE positions SET number_of_shares = {number_of_shares} WHERE ticker_symbol = "{ticker_symbol}";'.format(number_of_shares=new_holdings, ticker_symbol=ticker_symbol))
            connection.commit()

            cursor.execute('SELECT vwap FROM positions WHERE ticker_symbol = "{ticker_symbol}";'.format(ticker_symbol=ticker_symbol))
            old_vwap = cursor.fetchall()[0][0]


            if new_holdings == 0:
                new_vwap = 0.0
            else:
                new_vwap = ((int(trade_volume) * last_price)+(current_holdings * old_vwap)) / new_holdings
            print(new_vwap)    
        #TODO ERROR IS HERE---!!!!
            #return new_vwap    
            cursor.execute('UPDATE positions SET vwap = {vwap} WHERE ticker_symbol = "{ticker_symbol}";'.format(vwap=new_vwap, ticker_symbol=ticker_symbol))
            connection.commit()

            cursor.execute('UPDATE users SET balance = {new_balance};'.format(new_balance=new_balance,))
            connection.commit()

            cursor.close()
            connection.close()

        return 'Trade is complete, You sold',trade_volume,'shares of',ticker_symbol.upper(),'at',last_price

def lookup(company_name):
    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input={company_name}'.format(company_name=company_name)
    response = json.loads(requests.get(deep_link).text)
    ticker_symbol = response[0]['Symbol']
    return ticker_symbol


def quote(ticker_symbol):
    deep_link = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol={ticker_symbol}'.format(ticker_symbol=ticker_symbol)
    response = json.loads(requests.get(deep_link).text)
    last_price = response['LastPrice']
    
    return ticker_symbol.upper(), last_price

def portfolio():
    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    cursor.execute('SELECT balance FROM users;')
    balance = cursor.fetchall()[0][0]

    cursor.execute('SELECT ticker_symbol,number_of_shares,vwap FROM positions;')
    trades = cursor.fetchall()

    cursor.close()
    connection.close()

    return 'Current balance is' ,round(balance, 2), 'and your current positions are:', trades

    

def pl1():

    connection = sqlite3.connect('master.db', check_same_thread=False)
    cursor     = connection.cursor()

    friction = 12.00

    cursor.execute('SELECT SUM(vwap) FROM positions;')
    avpr = cursor.fetchall()[0][0]
    

    cursor.execute('SELECT SUM(last_price) FROM transactions WHERE transaction_type = 0;')
    prbuy = cursor.fetchall()[0][0]

    cursor.execute('SELECT SUM(last_price) FROM transactions WHERE transaction_type = 1;')
    prsell = cursor.fetchall()[0][0]
    
    cursor.execute('SELECT SUM(trade_volume) FROM transactions;')
    totvol = cursor.fetchall()[0][0]

    cursor.execute('SELECT count(*) FROM transactions;')
    trans = cursor.fetchall()[0][0]
    brocost = trans * friction

    #return cost
    #return sale

    #return 'Current gain or loss is',(cost - sale) 

    cursor.close()
    connection.close()

   
   

    #return 'Current P&L is', round((price * shares), 2)


    



