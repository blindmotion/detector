#!/usr/bin/python
__author__ = 'lamerman'

import datetime
import json
from optparse import OptionParser

START = 'start'
END = 'end'
TYPE = 'type'
DIRECTION = 'direction'


def get_options():
    parser = OptionParser()
    parser.add_option("-a", "--actual", dest="actual",
                    help="File with actual events")
    parser.add_option("-p", "--predicted", dest="predicted",
                    help="File with predicted events")

    (options, args) = parser.parse_args()

    if not options.actual or not options.predicted:
        raise KeyError('Not all required options specified')

    return options


def load_events(eventsfile):
    with open(eventsfile, 'rb') as file:
        events = json.load(file)
        for event in events:
            event[START] = datetime.datetime.strptime(event[START], '%H:%M:%S')
            event[END] = datetime.datetime.strptime(event[END], '%H:%M:%S')

        return events


def get_diff(actual, predicted):
    correct_type = {}
    wrong_type = {}
    false_positive = {}
    false_negative = {}

    for p_event in predicted:
        for a_event in actual:
            if (a_event[START] <= p_event[START] <= a_event[END]) or \
                    (a_event[START] <= p_event[END] <= a_event[END]):

                if a_event[TYPE] == p_event[TYPE] and \
                    a_event[DIRECTION] == p_event[DIRECTION]:

                    if a_event[TYPE] in correct_type:
                        correct_type[a_event[TYPE]] += 1
                    else:
                        correct_type[a_event[TYPE]] = 1
                else:
                    if a_event[TYPE] in wrong_type:
                        wrong_type[a_event[TYPE]] += 1
                    else:
                        wrong_type[a_event[TYPE]] = 1

    for p_event in predicted:
        one_of_actual = False
        for a_event in actual:
            if (a_event[START] <= p_event[START] <= a_event[END]) or \
                    (a_event[START] <= p_event[END] <= a_event[END]):
                one_of_actual = True

        if not one_of_actual:
            if p_event[TYPE] in false_positive:
                false_positive[p_event[TYPE]] += 1
            else:
                false_positive[p_event[TYPE]] = 1

    for a_event in actual:
        one_of_predicted = False
        for p_event in predicted:
            if (a_event[START] <= p_event[START] <= a_event[END]) or \
                    (a_event[START] <= p_event[END] <= a_event[END]):
                one_of_predicted = True

        if not one_of_predicted:
            if p_event[TYPE] in false_negative:
                false_negative[p_event[TYPE]] += 1
            else:
                false_negative[p_event[TYPE]] = 1

    correct_percent = float(sum(correct_type.values()))/(sum(correct_type.values()) +
                sum(wrong_type.values()) + sum(false_positive.values()) +
                sum(false_negative.values()))

    correct_percent_no_fn = float(sum(correct_type.values()))/(sum(correct_type.values()) +
                sum(wrong_type.values()) + sum(false_positive.values()))

    result = {
        'correct' : {
            'sum' : sum(correct_type.values()),
            'values' : correct_type
        },
        'wrong' : {
            'sum' : sum(wrong_type.values()),
            'values' : wrong_type
        },
        'false-positive' : {
            'sum' : sum(false_positive.values()),
            'values' : false_positive
        },
        'false-negative' : {
            'sum' : sum(false_negative.values()),
            'values' : false_negative
        },
        'correct-percent' : correct_percent,
        'correct-percent-no-fn' : correct_percent_no_fn
    }

    print json.dumps(result, indent=2)


def main():
    options = get_options()
    actual = load_events(options.actual)
    predicted = load_events(options.predicted)
    get_diff(actual, predicted)

if __name__ == '__main__':
    main()
