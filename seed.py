#!/usr/bin/env python3

import sqlite3


connection = sqlite3.connect('master.db', check_same_thread=False)
cursor     = connection.cursor()

cursor.execute(
    """INSERT INTO users(
        username,
        password,
        balance
    ) VALUES(
        'gannon',
        'swordfish',
        1000.00
    );"""
)

cursor.execute(
    """INSERT INTO positions(
        ticker_symbol,
        number_of_shares,
        volume_weighted_adjusted_price
    ) VALUES(
        'tsla',
        1,
        350.99
    );"""
)

cursor.execute(
    """INSERT INTO transactions(
        unix_time,
        transaction_type,
        last_price,
        trade_volume
    ) VALUES(
        1519853474.5758197,
        1,
        350.99,
        1
    );"""
)

connection.commit()
cursor.close()
connection.close()
