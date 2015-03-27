#!/usr/bin/python
# Runs in parallel several training processes. After the training
# the result is exported as events json file and compared with CV
__author__ = 'lamerman'

import subprocess
import tempfile
import csv
import json
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
    parser.add_option("-p", "--program", dest="program",
                    help="[Optional] Program with csv net parameters to be executed")

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
        raise subprocess.CalledProcessError()

    tfile_events_json = tempfile.mktemp()

    post_process(tfile_y, tfile_time, tfile_events_json, 1, 7)

    return tfile_events_json


def get_program_from_file(path):
    program = []
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            tfile = tempfile.mktemp()
            with open(tfile, 'wb') as programfile:
                writer = csv.writer(programfile, delimiter=',')
                writer.writerow(row)

            program.append((row, tfile))

    return program


def main():
    options = get_options()

    program = [None]
    if options.program:
        program = get_program_from_file(options.program)

    for program_iter in program:

        if program_iter is not None:
            print "Running program " + str(program_iter[0])
            print 'Config: ' + program_iter[1]

        processes = []
        for i in xrange(options.numproc):
            tfile = tempfile.mktemp()
            if program_iter is None:
                proc = subprocess.Popen(['octave', '-q', 'main.m', options.train_data,
                    tfile], cwd=octave_cwd)
            else:
                proc = subprocess.Popen(['octave', '-q', 'main.m', options.train_data,
                    tfile, program_iter[1]], cwd=octave_cwd)
            processes.append((proc, tfile))

        for proc, _ in processes:
            return_code = proc.wait()
            if return_code != 0:
                raise subprocess.CalledProcessError()

        for _, tfile in processes:
            try:
                print 'Result file: ' + tfile
                events_file = predict_events(options, tfile)
                diff = compaire_events(options.events_json, events_file)
                print 'next_line_is_result'
                print json.dumps(diff)
            except Exception as e:
                pass

            print '\n\n'

if __name__ == '__main__':
    main()
