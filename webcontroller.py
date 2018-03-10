#!/usr/bin/env python3

import time

from flask import Flask, redirect, render_template, request, url_for

import model


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return render_template('login.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            username = request.form['username']
            password = request.form['password']

            if username != 'bloom' or password != 'swordfish':
                return render_template('login.html', message = 'error: bad credentials...Please try again')
            else:
                return redirect(url_for('menu'))


@app.route('/menu', methods = ['GET', 'POST'])
def menu():
    if request.method == 'GET':
        return render_template('menu.html')
    else:
        pass


@app.route('/buy', methods = ['GET', 'POST'])
def buy():
    if request.method == 'GET':
        return render_template('buy.html')
    else:
        ticker_symbol = request.form['thingone']
        trade_volume  = request.form['thingtwo']
        x = model.buy(ticker_symbol, trade_volume)
        return render_template('buy.html', message = x)


@app.route('/sell', methods = ['GET', 'POST'])
def sell():
    if request.method == 'GET':
        return render_template('sell.html')
    else:
        ticker_symbol = request.form['sellone']
        trade_volume  = request.form['selltwo']
        x = model.sell(ticker_symbol, trade_volume)
        return render_template('sell.html', message = x)


@app.route('/lookup', methods = ['GET', 'POST'])
def lookup():
    if request.method == 'GET':
        return render_template('lookup.html')
    else:
        company_name = request.form['coname']
        x = model.lookup(company_name)
        return render_template('lookup.html', message = x)


@app.route('/quote', methods = ['GET', 'POST'])
def quote():
    if request.method == 'GET':
        return render_template('quote.html')
    else:
        ticker_symbol = request.form['copsymb']
        x = model.quote(ticker_symbol)
        return render_template('quote.html', message = x)


@app.route('/portfolio', methods = ['GET'])
def portfolio():
        x = model.portfolio()
        return render_template('portfolio.html', message = x)


@app.route('/pl', methods = ['GET'])
def pl():
        x = model.pl1()
        return render_template('pl.html',message = x)
  


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
