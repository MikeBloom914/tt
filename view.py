#!/usr/bin/env python3

import os


def header():
    return ' ------------------------------------'


def main_menu():
    os.system('clear')
    print(header())
    print('\n Terminal Trader\n\n\n\n')
    print(' [B] Buy\n [S] Sell\n\n [L] Look-up\n [Q] Quote\n\n\n [E] Exit\n\n')
    user_input = input(' What do you want to do? ')
    return user_input


def buy_menu():
    os.system('clear')
    print(header())
    print('\n Terminal Trader\n\n')
    ticker_symbol = input(' What do you want to buy? ')
    trade_volume = input(' How much {ticker_symbol} do you want to buy? '.format(ticker_symbol=ticker_symbol))
    return ticker_symbol, trade_volume


def sell_menu():
    os.system('clear')
    print(header())
    print('\n Terminal Trader\n\n')
    ticker_symbol = input(' What do you want to sell? ')
    trade_volume = input(' How much {ticker_symbol} do you want to buy? '.format(ticker_symbol=ticker_symbol))
    return ticker_symbol, trade_volume

def lookup_menu():
    os.system('clear')
    print(header())
    print('\n Terminal Trader\n\n')
    company_name = input(' What company do you want to look-up? ')
    return company_name

def quote_menu():
    os.system('clear')
    print(header())
    print('\n Terminal Trader\n\n')
    ticker_symbol = input(' What symbol do you want a price for? ')
    return ticker_symbol

