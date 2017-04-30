# -*- coding: ascii -*-
"""
Load that date formatted text
"""

from sqlite3 import connect
from csv import reader
from datetime import date, time

SQL_INSERT = 'INSERT INTO SITE_DATA VALUES (?, ?, ?, ?, ?, ? , ?, ?)'

raw_csv = ''
ws = ''
with connect(ws) as conn:

    cursor = conn.cursor()
    with open(raw_csv) as csv_file:
        x = 0
        for lab, timestamp in reader(csv_file):
            if 'Visit' in timestamp:
                continue
            try:
                rec_date, rec_time = timestamp.split(' ')
            except ValueError:
                continue
            month, day, year = [int(e) for e in rec_date.split('-')]


            entry_date = date(2000 + year, month, day)
            weekday = entry_date.weekday()
            hour, minute = [int(i) for i in rec_time.split(':')]
            x +=1
            entry = (x, lab, 2000 + year, month, day, hour, minute, weekday)
            cursor.execute(SQL_INSERT, entry)
            if not x % 10000:
                print(x)
        conn.commit()




