#!/usr/bin/python
# Runs in parallel several training processes. After the training
# the result is exported as events json file and compared with CV
__author__ = 'lamerman'

import subprocess
import tempfile
from os import path
from optparse import OptionParser
from compaire_events import compaire_events
from post_process_events import post_process

script_path = path.dirname(path.realpath(__file__))
octave_cwd = path.join(script_path, '../core')

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
    parser.add_option("-g", "--events-gen-dir", dest="events_gen_dir",
                    help="Directory with generated intervals for one day")

    (options, args) = parser.parse_args()

    if not options.train_data or not options.numproc or not options.cv_data\
            or not options.events_json or not options.events_gen_dir:
        raise KeyError('Not all required options specified')

    return options


def predict_events(options, tfile_mat):
    tfile_y = tempfile.mktemp()
    tfile_time = tempfile.mktemp()

    raw_data_mat = path.join(options.events_gen_dir, 'data.mat')
    raw_data_time = path.join(options.events_gen_dir, 'time.csv')

    proc = subprocess.Popen(['octave', '-q', 'predict_events.m', tfile_mat,
                             raw_data_mat, raw_data_time, tfile_y, tfile_time],
                             cwd=octave_cwd)
    return_code = proc.wait()
    if return_code != 0:
        exit(1)

    tfile_events_json = tempfile.mktemp()

    post_process(tfile_y, tfile_time, tfile_events_json)

    return tfile_events_json

def main():
    options = get_options()

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
        try:
            events_file = predict_events(options, tfile)
            diff = compaire_events(options.events_json, events_file)
            print diff
        except Exception as e:
            pass

        print '\n\n'

if __name__ == '__main__':
    main()
