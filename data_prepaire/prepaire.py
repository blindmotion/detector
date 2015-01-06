#!/usr/bin/python
# Copyright (c) 2014, Blind Motion Project
# All rights reserved.

import csv
import json
import sys
import datetime
from optparse import OptionParser
from datetime import timedelta
from scipy.interpolate import interp1d

ACC_KEY = '1'
GYR_KEY = '4'
ACC_KEY_INT = 1
GYR_KEY_INT = 4
GEO_KEY = 'geo'
TYPE_KEY = 'type'
DIRECTION_KEY = 'direction'
TYPE_INDX = 0
TIME_INDX = 1
X_INDX = 3
Y_INDX = 4
Z_INDX = 5
SPD_INDX = 9
SpeedCoefficient = 3.6
EVENT_START = 'start'
EVENT_END = 'end'

EVENT_TYPE_IDLE = -1
EVENT_DIR_LEFT = 0

TIME_DELTA_IDLE_START_END = timedelta(seconds=10)
TIME_DELTA_EVENTS = timedelta(milliseconds=500)
NUM_ELEMENTS_GYR_ACC = 100
NUM_ELEMENTS_SPEED = 10


def bsearch(arr, searchValue, left, right, extr=lambda v: v):
    if searchValue < extr(arr[0]):
        raise ValueError('search value is less than left value')

    if right < left:
        return right

    mid = (left + right) / 2
    if searchValue > extr(arr[mid]):
        return bsearch(arr, searchValue, mid + 1, right, extr)
    elif searchValue < extr(arr[mid]):
        return bsearch(arr, searchValue, left, mid - 1, extr)
    else:
        return mid


def get_options():
    parser = OptionParser()
    parser.add_option("-i", "--inputfile", dest="inputfile",
                    help="Input csv file")
    parser.add_option("-e", "--eventsfile", dest="eventsfile",
                    help="Json file with events")
    parser.add_option("-o", "--outputfile", dest="outputfile",
                    help="The name of output file")
    parser.add_option("-s", "--shift", dest="shift",
                    help="Additional shift for data window in seconds")
    parser.add_option("-t", "--shift-step", dest="shift_step",
                    help="Length of one shift step in seconds")

    (options, args) = parser.parse_args()

    if not options.inputfile or not options.outputfile \
            or not options.shift or not options.shift_step \
            or not options.eventsfile:

        raise KeyError('Not all required options specified')

    return options


def parse_row(row):
    if row[TYPE_INDX] == ACC_KEY or row[TYPE_INDX] == GYR_KEY:
        row[TYPE_INDX] = int(row[TYPE_INDX])
        row[X_INDX] = float(row[X_INDX])
        row[Y_INDX] = float(row[Y_INDX])
        row[Z_INDX] = float(row[Z_INDX])
        row[TIME_INDX] = datetime.datetime.strptime(row[TIME_INDX], '%H:%M:%S.%f')
        return row

    if row[TYPE_INDX] == GEO_KEY:
        row[SPD_INDX] = float(row[SPD_INDX]) * SpeedCoefficient
        row[TIME_INDX] = datetime.datetime.strptime(row[TIME_INDX], '%H:%M:%S.%f')
        return row

    return None


def load_events(eventsfile):
    with open(eventsfile, 'rb') as file:
        events = json.load(file)
        for event in events:
            event[EVENT_START] = datetime.datetime.strptime(event[EVENT_START], '%H:%M:%S')
            event[EVENT_END] = datetime.datetime.strptime(event[EVENT_END], '%H:%M:%S')

        return events


def load_data(inputfile):
    with open(inputfile, 'rb') as input:
        csvreader = csv.reader(input, delimiter=';')

        data = []
        num_errors = 0

        for row in csvreader:
            try:
                parsed = parse_row(row)
                if parsed is not None:
                    data.append(parsed)
            except ValueError:
                num_errors += 1

        if num_errors > 0:
            print 'Errors occured while parsing is ' + str(num_errors)

        return data


def sort_data_by_time(data):
    return sorted(data, key=lambda row: row[TIME_INDX])


def get_data_for_interval(data, start_indx, end_indx, event_type, event_dir):
    if start_indx < 0 or end_indx >= len(data):
        raise IndexError('index out of range')

    result = {
        ACC_KEY: {
            'x': [],
            'y': [],
            'z': []
        },
        GYR_KEY: {
            'x': [],
            'y': [],
            'z': []
        },
        GEO_KEY: {
            'spd': []
        },
        TYPE_KEY: event_type,
        DIRECTION_KEY: event_dir
    }

    for i in xrange(start_indx, end_indx + 1):
        row = data[i]
        if row[TYPE_INDX] == ACC_KEY_INT:
            result[ACC_KEY]['x'].append(row[X_INDX])
            result[ACC_KEY]['y'].append(row[Y_INDX])
            result[ACC_KEY]['z'].append(row[Z_INDX])
        if row[TYPE_INDX] == GYR_KEY_INT:
            result[GYR_KEY]['x'].append(row[X_INDX])
            result[GYR_KEY]['y'].append(row[Y_INDX])
            result[GYR_KEY]['z'].append(row[Z_INDX])
        if row[TYPE_INDX] == GEO_KEY:
            result[GEO_KEY]['spd'].append(row[SPD_INDX])

    result[ACC_KEY]['x'] = interpolate_array(result[ACC_KEY]['x'], NUM_ELEMENTS_GYR_ACC)
    result[ACC_KEY]['y'] = interpolate_array(result[ACC_KEY]['y'], NUM_ELEMENTS_GYR_ACC)
    result[ACC_KEY]['z'] = interpolate_array(result[ACC_KEY]['z'], NUM_ELEMENTS_GYR_ACC)

    result[GYR_KEY]['x'] = interpolate_array(result[GYR_KEY]['x'], NUM_ELEMENTS_GYR_ACC)
    result[GYR_KEY]['y'] = interpolate_array(result[GYR_KEY]['y'], NUM_ELEMENTS_GYR_ACC)
    result[GYR_KEY]['z'] = interpolate_array(result[GYR_KEY]['z'], NUM_ELEMENTS_GYR_ACC)

    result[GEO_KEY]['spd'] = interpolate_array(result[GEO_KEY]['spd'], NUM_ELEMENTS_SPEED)

    return result


def interpolate_array(arr, num_el):
    if num_el <= 0:
        raise ValueError('num_el cannot be 0 or less')

    if len(arr) == 0:
        arr = [0, 0]
    elif len(arr) == 1:
        arr = [arr[0], arr[0]]

    one_el_len = float(len(arr) - 1)/(num_el - 1)

    x = [i for i in xrange(len(arr))]
    y = arr

    # due to rounding issues we need to prolong array by one element
    x += [x[-1] + 1]
    y += [arr[-1]]

    intrpl = interp1d(x, y)
    try:
        result = [intrpl(i * one_el_len)[()] for i in xrange(num_el)]
    except ValueError:
        raise

    return result


def write_one_row(data, file):
    row = data[ACC_KEY]['x'] + data[ACC_KEY]['y'] + data[ACC_KEY]['z'] + \
        data[GYR_KEY]['x'] + data[GYR_KEY]['y'] + data[GYR_KEY]['z'] + \
        data[GEO_KEY]['spd']

    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
    writer.writerow([data[TYPE_KEY], data[DIRECTION_KEY]] + ['{0:.3f}'.format(x) for x in row])


def is_event_overlapped(events, start_date, end_date):
    for event in events:
        if event[EVENT_START] <= start_date <= event[EVENT_END]:
            return True
        if event[EVENT_START] <= end_date <= event[EVENT_END]:
            return True

    return False


def write_idle_data(data, events, file):
    for start_indx in xrange(0, len(data)):
        start_date = data[start_indx][TIME_INDX]
        end_date = start_date + TIME_DELTA_IDLE_START_END
        end_indx = bsearch(data, end_date, 0, len(data) - 1,
                            lambda row: row[TIME_INDX])

        if end_date > data[len(data)-1][TIME_INDX]:
            break

        if is_event_overlapped(events, start_date, end_date):
            continue

        data_for_interval = get_data_for_interval(data, start_indx, end_indx, EVENT_TYPE_IDLE, EVENT_DIR_LEFT)
        write_one_row(data_for_interval, file)

        sys.stdout.write("\r%d of %d" % (start_indx, len(data)) )
        sys.stdout.flush()

    print ''

def write_event_data(data, event, start_indx, end_indx, file):
    cur_indx = start_indx
    duration = event[EVENT_END] - event[EVENT_START]
    cur_end_time = data[cur_indx][TIME_INDX] + duration
    end_time = data[end_indx][TIME_INDX]

    while cur_end_time < end_time:
        cur_indx_plus_dur = bsearch(data, cur_end_time, 0, len(data) - 1,
                            lambda row: row[TIME_INDX])
        data_for_interval = get_data_for_interval(data, cur_indx, cur_indx_plus_dur, event[TYPE_KEY], event[DIRECTION_KEY])
        write_one_row(data_for_interval, file)

        cur_indx += 1
        cur_end_time = data[cur_indx][TIME_INDX] + duration

def write_events_data(data, events, file):
    for event_id in xrange(len(events)):
        event = events[event_id]
        sys.stdout.write("\rprocessing event %d of %d" % (event_id + 1, len(events)) )
        sys.stdout.flush()

        if data[0][TIME_INDX] <= event[EVENT_START] \
                and event[EVENT_END] <= data[len(data) - 1][TIME_INDX]:

            event_start_indx = bsearch(data, event[EVENT_START], 0, len(data) - 1,
                            lambda row: row[TIME_INDX])

            event_end_indx = bsearch(data, event[EVENT_END], 0, len(data) - 1,
                            lambda row: row[TIME_INDX])

            event_start_plus_dt = event[EVENT_START] - TIME_DELTA_EVENTS
            event_end_plus_dt = event[EVENT_END] + TIME_DELTA_EVENTS

            while event_start_indx > 0 and \
                    data[event_start_indx][TIME_INDX] > event_start_plus_dt:
                event_start_indx -= 1

            while event_end_indx < len(data) - 1 and \
                    data[event_end_indx][TIME_INDX] < event_end_plus_dt:
                event_end_indx += 1

            write_event_data(data, event, event_start_indx, event_end_indx, file)


def main():
    options = get_options()
    data = load_data(options.inputfile)
    events = load_events(options.eventsfile)
    data = sort_data_by_time(data)

    with open(options.outputfile, 'wb') as output:
        write_events_data(data, events, output)
        write_idle_data(data, events, output)


if __name__ == '__main__':
    main()