# -*- coding: ascii -*-
"""
<<DESCRIPTION OF SCRIPT>>
"""
from sqlite3 import connect
from os.path import join, dirname

ws = ''

script = join(dirname(__file__), 'create.sql')
conn = connect(ws)
cursor = conn.cursor()
with open(join(script), 'rU') as sql:
    cursor.executescript(sql.read().strip())
