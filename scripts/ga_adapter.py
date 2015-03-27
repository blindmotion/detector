#!/usr/bin/python
__author__ = 'lamerman'

import json
import sys
from optparse import OptionParser

def get_options():
    parser = OptionParser()
    parser.add_option("--type", dest="type",
                    help="Type of output to transform")

    (options, args) = parser.parse_args()

    if not options.type:
        raise KeyError('Not all required options specified')

    return options


def adapt_compaire_events():
    s = sys.stdin.read()
    output = json.loads(s)
    print output['correct-percent']


def adapt_run_train_parallel():
    max_percent = 0

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        if line == 'next_line_is_result\n':
            try:
                result_json = sys.stdin.readline()
                result = json.loads(result_json)
                max_percent = max(max_percent, result['correct-percent'])
            except:
                pass

    print max_percent

def main():
    opts = get_options()

    if opts.type == 'compaire_events':
        adapt_compaire_events()
    elif opts.type == 'run_train_parallel':
        adapt_run_train_parallel()
    else:
        raise KeyError('Unsupported type ' + opts.type)

if __name__ == '__main__':
    main()