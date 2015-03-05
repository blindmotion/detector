#!/usr/bin/python
# Runs in parallel several training processes. After the training
# the result is exported as events json file and compared with CV
__author__ = 'lamerman'

import subprocess
import tempfile
from os import path
from optparse import OptionParser

def get_options():
    parser = OptionParser()
    parser.add_option("-t", "--train-data", dest="train_data",
                    help="Training data file")
    parser.add_option("-c", "--cv-data", dest="cv_data",
                    help="Cross validation data file")
    parser.add_option("-n", "--numproc", dest="numproc", type="int",
                    help="Number of parallel processes")
    parser.add_option("-e", "--events-json", dest="events_json",
                    help="Events json file to which the result will be compaired")

    (options, args) = parser.parse_args()

    if not options.train_data or not options.numproc or not options.cv_data\
            or not options.events_json:
        raise KeyError('Not all required options specified')

    return options


def main():
    options = get_options()
    script_path = path.dirname(path.realpath(__file__))
    octave_cwd = path.join(script_path, '../core')

    processes = []
    for i in xrange(options.numproc):
        tfile = tempfile.mktemp()
        proc = subprocess.Popen(['octave', '-q', 'main.m', options.train_data,
            tfile], cwd=octave_cwd)
        processes.append((proc, tfile))

    for proc, _ in processes:
        return_code = proc.wait()
        if return_code != 0:
            exit(1)

    for _, tfile in processes:
        events_file = tempfile.mktemp()

        print script_path
        proc = subprocess.Popen(['./predict_events.sh', tfile, events_file], cwd=script_path)
        return_code = proc.wait()
        if return_code != 0:
            exit(1)

        proc = subprocess.Popen(['./compaire_events.py', '-a', options.events_json,
                                '-p', events_file], cwd=script_path)
        return_code = proc.wait()
        if return_code != 0:
            exit(1)

        print '\n\n'

if __name__ == '__main__':
    main()
