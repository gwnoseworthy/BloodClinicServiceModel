# -*- coding: ascii -*-
"""
Metadata process montitor engine
"""

from sqlite3 import connect
from collections import defaultdict
from csv import writer
from datetime import datetime, timedelta

SQL_PULL = """SELECT SITE, WEEKDAY, HOUR, MINUTE, ROUND(AVG(FREQ + 0.5)) FROM SITE_BINS WHERE HOUR >=7 AND WEEKDAY <5 AND SITE='SC' GROUP BY SITE, WEEKDAY, HOUR, MINUTE
ORDER BY SITE, WEEKDAY, HOUR, MINUTE ASC;"""


def fetch_data(database, sql):
    """
    fetch data from cursor
    """
    with connect(database) as db:
        cur = db.cursor()
        cur.execute(SQL_PULL)
        return cur.fetchall()
# End fetch_data function


class WaitTimer(object):
    """
    Wait time determination
    """
    def __init__(self, data, service_staff, registration_staff, out_csv):
        """
        Initialize the WaitTimer class
        """
        super(WaitTimer, self).__init__()
        self.data = data
        self.service_staff = service_staff
        self.registration_staff = registration_staff
        self.registration_tick = 1
        self.service_tick = 1
        self.out_csv = out_csv
    # End init built-in

    def __call__(self):
        """
        Make Class Callable
        """
        weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        data = fetch_data(self.data, SQL_PULL)
        stores = defaultdict(lambda: defaultdict(list))
        with open(self.out_csv, 'w') as csv_out:
            _writer = writer(csv_out)
            _writer.writerow(['DAY', 'TIME', 'REGISTRATION_QUEUE', 'SERVICE_QUEUE', 'WAIT_TIME'])

            for site, weekday, hour, minute, count in data:
                # if not 9 <= hour <= 17:
                #     continue
                # if count < 100:
                #     continue

                stores[site][weekday].append(int(count))
            for site, days in sorted(stores.items()):
                print(site)
                print('=============+=============')
                for day, clients in days.items():
                    print(weekdays[day])
                    self.process_people(clients, weekdays[day], _writer)
                print('==========================')

        # with open(self.data) as csv_file:
        #     for time, count in reader(csv_file):
        #         try:
        #             int(count)
        #         except ValueError:
        #             continue
        #         bins.append(int(count))
        # self.process_people(bins)
    # End call built-in
    # End  property

    def process_people(self, time_bins, day, _writer):
        """
        
        """
        service_line = 0
        registration_line = 0
        _time = -1
        start_time = datetime(100,1,1,7,00,00)
        str_time = start_time
        while time_bins or registration_line or service_line:
            # if time and not time % 6:
            if _time >= 0:
                str_time = start_time + timedelta(minutes=_time*10)
                _writer.writerow((day, str(str_time.time()), registration_line,
                                  service_line, self.wait_time(
                     registration_line, service_line)))
                print((day, str(str_time.time()), registration_line,
                       service_line, self.wait_time(
                    registration_line, service_line)))

            if not _time % self.registration_tick:
                if registration_line < self.registration_staff * 2:
                    registration_line = 0
                    service_line += registration_line
                else:
                    registration_line -= self.registration_staff * 2
                    service_line += self.registration_staff * 2
            if not _time % self.service_tick:
                if service_line <= self.service_staff:
                    service_line = 0
                else:
                    service_line -= self.service_staff
            if time_bins:
                registration_line += time_bins.pop(0)
            _time += 1
            if str_time >= datetime(100,1,1,15,00,00):
                break

    # End process_people method

    def wait_time(self, registration, service):
        """
        remaining wait
        """
        register_wait = round((registration/self.registration_staff) +.5)
        served = register_wait/self.service_tick * self.service_staff
        to_serve = registration - served + service

        service_wait = round(self.service_tick * to_serve / self.service_staff)
        return (register_wait + service_wait) * 10
    # End wait_time method
# End WaitTimer class
if __name__ == '__main__':
    pass

