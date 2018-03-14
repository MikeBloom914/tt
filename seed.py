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
        'mikebloom914@gmail.com',
        'swordfish',
        10000.00
    );"""
)


connection.commit()
cursor.close()
connection.close()
