import sqlite3

db = sqlite3.connect('./trade_ticks.db')

cur = db.cursor()

cur.execute("SELECT name from sqlite_master where type = 'table'")
cur.fetchall()

cur.execute("PRAGMA table_info(AAPL)")
cur.fetchall()

cur.execute("SELECT * FROM AAPL")
cur.fetchall()