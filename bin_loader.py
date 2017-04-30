# -*- coding: ascii -*-
"""
Load Time Deatils from bin tables
"""

from os.path import join
from csv import reader
from datetime import datetime

CSV_FOLDER = r''

HSC_FILE = ''
MP_FILE = ''
WF_FILE = ''
SC_FILE = ''


CLINIC_LOOKUP = {'HS': join(CSV_FOLDER, HSC_FILE),
                 'MP': join(CSV_FOLDER, MP_FILE),
                 'WF': join(CSV_FOLDER, WF_FILE),
                 'SC': join(CSV_FOLDER, SC_FILE)}

def parse_file_as_dict(file):
    """
    
    """
    with open(file) as csv_file:
        time_stamps = dict()
        for day, time, r_queue, s_queue, wait_time in reader(csv_file):
            time_stamps[(day, time)] = r_queue, s_queue, wait_time
        return time_stamps
# End parse_file function


def pull_now_time(hospital_code, now_time):
    """
    
    """
    weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI']
    lookup_file = CLINIC_LOOKUP.get(hospital_code)
    try:
        day = weekdays[now_time.weekday()-2]
        mins = round(now_time.minute, -1)
        hour = now_time.hour
        if mins >= 55:
            hour += 1
        q_time = datetime(100, 1, 1, now_time.hour, mins % 60, 00)

    except IndexError:
        return None
    time_stamps = parse_file_as_dict(lookup_file)
    return time_stamps.get((day, str(q_time.time())))


def pull_request_time(hospital_code, request_time):
    """

    """
    weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI']
    lookup_file = CLINIC_LOOKUP.get(hospital_code)
    try:
        day = weekdays[request_time.weekday()]
        mins = round(request_time.minute, -1)
        hour = request_time.hour
        if mins >= 55:
            hour += 1
        q_time = datetime(100, 1, 1, hour, mins % 60, 00)
        print(str(q_time.time()))

    except IndexError:
        return None
    time_stamps = parse_file_as_dict(lookup_file)
    return time_stamps.get((day, str(q_time.time())))

# End pull_wait_time function

if __name__ == '__main__':
    print(pull_now_time('MP', datetime.now()))
    print(pull_request_time('MP', datetime(2017, 4, 28, 10, 28)))
    print(pull_request_time('MP', datetime(2017, 4, 28, 10, 59)))
