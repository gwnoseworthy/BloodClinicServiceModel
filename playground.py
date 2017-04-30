# -*- coding: ascii -*-
"""
<<DESCRIPTION OF SCRIPT>>
"""
from collections import defaultdict
from math import log
from os.path import join
from pandas import DataFrame

SQL_ORDERED_DATA = """SELECT  WEEKDAY, HOUR + MINUTE/60 FROM SITE_DATA WHERE YEAR==2013"""

MONTH_ORDERED_DATA = """SELECT SITE, MONTH, HOUR, COUNT(SITE) FROM SITE_DATA GROUP BY SITE, WEEKDAY, HOUR
ORDER BY  MONTH, HOUR ASC"""

MONTH_ORDERED_DATA = """SELECT SITE, HOUR, COUNT(SITE) FROM SITE_DATA GROUP BY SITE, HOUR
ORDER BY HOUR ASC"""


BINNER = """SELECT WEEKDAY, HOUR, MINUTE, ROUND(AVG(FREQ)) FROM SITE_BINS WHERE  WEEKDAY < 5 AND HOUR >=7 AND HOUR <=16 GROUP BY WEEKDAY, HOUR, MINUTE
ORDER BY  WEEKDAY, HOUR ASC;"""

from sqlite3 import connect
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def fetch_data(database, sql):
    """
    fetch data from cursor
    """
    with connect(database) as db:
        cur = db.cursor()
        cur.execute(sql)
        return cur.fetchall()
# End fetch_data function


def graph_from_database(ws, out_path):
    """
    make a few graphs
    """
    count_pots = dict()
    data = fetch_data(ws, BINNER)
    for day, hour, minute, count in data:
        count_pots[day, hour, minute] = count

    days, hours, minutes = zip(*count_pots.keys())
    # z_values = []
    # y_values = []
    #
    # for hour in sorted(list(set(hours))):
    #     for minute in sorted(list(set(minutes))):
    #         y_row = []
    #         for day in sorted(list(set(days))):
    #             y_row.append(count_pots.get((day, hour, minute), 0))
    #         y_values.append(hour + (minute/60))
    #         z_values.append(y_row)

    df = pd.DataFrame(data)
    df.columns = ['day', 'hour', 'minute', 'freq']
    df['time_series'] = df['hour'] + (df['minute'] / 60)
    pivot = df.pivot('time_series', 'day')['freq']

    cmap = sns.diverging_palette(50, 10, as_cmap=True)
    plot = sns.heatmap(pivot, cmap="Reds")
    # sns.plt.xticks('MON', 'TUE', 'WED', 'THU', 'FRI')
    # for i, label in enumerate(plot.get_yticklabels(), start=1):
    #     if not i % 6:
    #         label.set_visible(True)
    #     else:
    #         label.set_visible(False)
    sns.plt.yticks([i for i in range(6, 66, 6)], df.hour.unique()[::-1],
                   rotation='horizontal')
    sns.plt.xticks([i + 0.5 for i in range(5)],
                   ['MON', 'TUE', 'WED', 'THU', 'FRI'])
    sns.plt.xlabel("Weekday")
    sns.plt.ylabel("Hour")
    # sns.plt.show()

    # for site, weekday, hour, minute, count in data:
    #     # if not 9 <= hour <= 17:
    #     #     continue
    #     # if count < 100:
    #     #     continue
    #     times = defaultdict()
    #     time = hour + (minute/60.)
    #     stores[site].append((weekday, time, count))
    #     # if not 'major' in site.lower():
    #     #     continue
    #     # time[]
    #
    #
    # for site, records in stores.items():
    #     w, h, c = zip(*records)
    #
    #     sizer = [20 * e for e  in c]
    #     # plt.bar(h, c)
    #     plt.scatter(w, h, c=c, s=sizer, label=c)
    #     plt.title(site)
    #     plt.colorbar()
    #     sns.heatmap([w,h,c])
    sns.plt.savefig(out_path)
    #     plt.show()
# End graph_from_database function


if __name__ == '__main__':
    pass

