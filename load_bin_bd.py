# -*- coding: ascii -*-
"""
<<DESCRIPTION OF SCRIPT>>
"""

from sqlite3 import connect
from csv import reader
from datetime import date, time

SQL_INSERT = 'INSERT INTO SITE_BINS VALUES (?, ?, ?, ?, ? , ?, ?, ?)'


from sqlite3 import connect
from os.path import join, dirname
# raw_csv = r'/Users/gwnoseworthy/Downloads/SCM10min.csv'
# raw_csv = r'/Users/gwnoseworthy/Hacking/HSC10min.csv'
# raw_csv = r'/Users/gwnoseworthy/Hacking/WAH10min.csv'
raw_csv = r''
ws = r''



script = join(dirname(__file__), 'bin_site.sql')
conn = connect(ws)
cursor = conn.cursor()
# with open(join(script), 'rU') as sql:
#     cursor.executescript(sql.read().strip())
lab = 'MP'
with connect(ws) as conn:

    cursor = conn.cursor()
    with open(raw_csv) as csv_file:
        x = 0
        for timestamp, freq in reader(csv_file):
            if 'Visit' in timestamp:
                continue
            try:
                rec_date, rec_time = timestamp.split(' ')
            except ValueError:
                continue
            year, month, day = [int(e) for e in rec_date.split('-')]
            entry_date = date(year, month, day)
            weekday = entry_date.weekday()
            hour, minute = [int(i) for i in rec_time.split(':')]
            x +=1
            entry = (lab, year, month, day, hour, minute, weekday, freq)
            cursor.execute(SQL_INSERT, entry)
            if not x % 10000:
                print(x)
        conn.commit()




