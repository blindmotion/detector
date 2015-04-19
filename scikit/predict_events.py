#!/usr/bin/python
__author__ = 'lamerman'

import sys
sys.path.append('..')

import subprocess
import tempfile
import csv
import pickle
import json
import numpy as np
from os import path
from optparse import OptionParser
from scripts.compaire_events import compaire_events
from scripts.post_process_events import post_process

script_path = path.dirname(path.realpath(__file__))

def vararg_callback(option, opt_str, value, parser):
    assert value is None
    value = []

    for arg in parser.rargs:

        if arg[:2] == "--" and len(arg) > 2:
            break

        if arg[:1] == "-" and len(arg) > 1:
            break

        value.append(arg)

    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)


def get_options():
    parser = OptionParser()
    parser.add_option("--models", dest="models",
                    help="Models that will be used to predict events")
    parser.add_option("--events-dates", dest="events_dates",
                    help="Dates of events to be predicted",
                    action="callback", callback=vararg_callback)
    parser.add_option("--events-gen-dir", dest="events_gen_dir",
                    help="Directory with generated events for all days")
    parser.add_option("--events-dir", dest="events_dir",
                    help="Directory with hand made events")
    parser.add_option("--epsilon", dest="epsilon", type="int",
                    help="DBScan epsilon")
    parser.add_option("--min-samples", dest="min_samples", type="int",
                    help="DBScan min samples")
    parser.add_option("--threshold", dest="threshold", type="float",
                    help="How confident the classifer should be "
                         "before marking an event")

    (options, args) = parser.parse_args()

    if not options.models or not options.events_dates\
            or not options.events_gen_dir or not options.events_dir\
            or not options.epsilon or not options.min_samples\
            or not options.threshold:
        raise KeyError('Not all required options specified')

    return options


def predict_events(options, event_date, tfile_mat):
    tfile_y = tempfile.mktemp()
    tfile_time = tempfile.mktemp()

    raw_data_mat = path.join(options.events_gen_dir, event_date, 'data.npz')
    raw_data_time = path.join(options.events_gen_dir, event_date, 'time.csv')

    dataset = np.load(raw_data_mat)
    time = np.loadtxt(raw_data_time, dtype=np.str_)

    X = dataset['X']

    clf = None
    with open(options.models, 'r') as f:
        clf = pickle.load(f)

    prob = clf.predict_proba(X)
    y = clf.predict(X)

    indx = np.max(prob, axis=1) > options.threshold
    y = y[indx]
    time = time[indx]

    indx = y != 1
    y = y[indx]
    time = time[indx]

    with open(tfile_y, 'wb') as f:
        np.savetxt(f, y, delimiter=',', fmt='%d')

    with open(tfile_time, 'wb') as f:
        np.savetxt(f, time, fmt='%s')

    tfile_events_json = tempfile.mktemp()

    post_process(tfile_y, tfile_time, tfile_events_json,
                 options.epsilon, options.min_samples)

    return tfile_events_json


def merge_diffs(all_diffs):
    result = {
        'false-negative': {'sum': 0},
        'correct': {'sum': 0},
        'wrong': {'sum': 0},
        'false-positive': {'sum': 0}
    }

    for diff in all_diffs:
        result['false-negative']['sum'] += diff['false-negative']['sum']
        result['correct']['sum'] += diff['correct']['sum']
        result['wrong']['sum'] += diff['wrong']['sum']
        result['false-positive']['sum'] += diff['false-positive']['sum']

    result['correct-percent'] = float(result['correct']['sum'])/(result['correct']['sum'] +
                result['wrong']['sum'] + result['false-positive']['sum'] +
                result['false-negative']['sum'])

    result['correct-percent-no-fn'] = float(result['correct']['sum'])/(result['correct']['sum'] +
                result['wrong']['sum'] + result['false-negative']['sum'])

    return result


def main():
    options = get_options()

    print ''

    all_diffs = []

    for event_date in options.events_dates:
        events_file = predict_events(options, event_date, options.models)
        hand_made_event_file = path.join(options.events_dir, event_date, 'all.json')
        diff = compaire_events(hand_made_event_file, events_file)
        all_diffs.append(diff)

        print event_date
        print json.dumps(diff)
        print ''

    print 'all'
    print json.dumps(merge_diffs(all_diffs))

if __name__ == '__main__':
    main()
