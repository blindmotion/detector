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

    print
    print 'Correct type:'
    print sum(correct_type.values())
    print correct_type
    print
    print 'Wrong type:'
    print sum(wrong_type.values())
    print wrong_type
    print
    print 'False positive:'
    print sum(false_positive.values())
    print false_positive
    print
    print 'False negative:'
    print sum(false_negative.values())
    print false_negative
    print
    print 'Correct percent'
    print float(sum(correct_type.values()))/(sum(correct_type.values()) +
                sum(wrong_type.values()) + sum(false_positive.values()) +
                sum(false_negative.values()))
    print float(sum(correct_type.values()))/(sum(correct_type.values()) +
                sum(wrong_type.values()) + sum(false_positive.values()))


def main():
    options = get_options()
    actual = load_events(options.actual)
    predicted = load_events(options.predicted)
    get_diff(actual, predicted)

if __name__ == '__main__':
    main()
