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
from time import sleep

ACC_KEY = '1'
GYR_KEY = '4'
ACC_KEY_INT = 1
GYR_KEY_INT = 4
GEO_KEY = 'geo'
TYPE_INDX = 0
TIME_INDX = 1
X_INDX = 3
Y_INDX = 4
Z_INDX = 5
SPD_INDX = 9
SpeedCoefficient = 3.6

TIME_DELTA_SECONDS = 10
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

    if row[TYPE_INDX] == GEO_KEY:
        row[SPD_INDX] = float(row[SPD_INDX]) * SpeedCoefficient

    row[TIME_INDX] = datetime.datetime.strptime(row[TIME_INDX], '%H:%M:%S.%f')

    return row


def load_events(eventsfile):
    with open(eventsfile, 'rb') as file:
        events = json.load(file)
        for event in events:
            event['start'] = datetime.datetime.strptime(event['start'], '%H:%M:%S')
            event['end'] = datetime.datetime.strptime(event['end'], '%H:%M:%S')

        return events


def load_data(inputfile):
    with open(inputfile, 'rb') as input:
        csvreader = csv.reader(input, delimiter=';')

        data = []
        num_errors = 0

        for row in csvreader:
            try:
                data.append(parse_row(row))
            except ValueError:
                num_errors += 1

        if num_errors > 0:
            print 'Errors occured while parsing is ' + str(num_errors)

        return data


def sort_data_by_time(data):
    return sorted(data, key=lambda row: row[TIME_INDX])


def get_data_for_interval(data, start_indx, end_indx):
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
        }
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

    intrpl = interp1d(x, y)
    result = [intrpl(i * one_el_len)[()] for i in xrange(num_el)]

    return result


def write_one_row(data, file):
    row = data[ACC_KEY]['x'] + data[ACC_KEY]['y'] + data[ACC_KEY]['z'] + \
        data[GYR_KEY]['x'] + data[GYR_KEY]['y'] + data[GYR_KEY]['z'] + \
        data[GEO_KEY]['spd']

    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
    writer.writerow(['{0:.3f}'.format(x) for x in row])


def write_idle_data(data, file):
    for start_indx in xrange(0, len(data)):
        start_date = data[start_indx][TIME_INDX]
        end_date = start_date + timedelta(seconds=TIME_DELTA_SECONDS)
        end_indx = bsearch(data, end_date, 0, len(data) - 1,
                            lambda row: row[TIME_INDX])

        if end_date > data[len(data)-1][TIME_INDX]:
            break

        data_for_interval = get_data_for_interval(data, start_indx, end_indx)
        write_one_row(data_for_interval, file)

        sys.stdout.write("\r%d" % start_indx)
        sys.stdout.flush()

    print ''


def main():
    options = get_options()
    data = load_data(options.inputfile)
    events = load_events(options.eventsfile)
    data = sort_data_by_time(data)

    with open(options.outputfile, 'wb') as output:
        write_idle_data(data, output)


if __name__ == '__main__':
    main()