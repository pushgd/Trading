import sqlite3
import datetime


def inertIntoTick(open, high, close, low, volume, symbol, date):
    s = 'Insert INTO Tick (OPEN,HIGH,CLOSE,LOW,VOLUME,SYMBOL,DATE) Values('+str(open)+','+str(high)+','+str(close)+','+str(low) +\
        ','+str(volume)+',\''+symbol+'\',\''+str(date)+'\')'
    cursor.execute(s)
    conn.commit()


def init():
    global conn
    conn = sqlite3.connect('marketData.db')
    global cursor
    cursor = conn.cursor()
    s = 'Create TABLE IF NOT EXISTS Tick (ID INTEGER PRIMARY KEY AUTOINCREMENT,OPEN REAL NOT NULL,HIGH REAL NOT NULL,CLOSE REAL NOT NULL,LOW REAL NOT NULL,VOLUME REAL NOT NULL,SYMBOL TEXT NOT NULL,DATE TEXT NOT NULL)'
    cursor.execute(s)
