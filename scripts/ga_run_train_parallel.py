#!/usr/bin/python
__author__ = 'lamerman'

import tempfile
import csv
import subprocess
from optparse import OptionParser

def get_options():
    parser = OptionParser()
    parser.add_option("--train-data", dest="train_data",
                    help="Training data file")
    parser.add_option("--cv-data", dest="cv_data",
                    help="Cross validation data file")
    parser.add_option("--numproc", dest="numproc", type="int",
                    help="Number of parallel processes")
    parser.add_option("--events-json", dest="events_json",
                    help="Events json file to which the result will be compaired")
    parser.add_option("--events-gen-dir", dest="events_gen_dir",
                    help="Directory with generated intervals for one day")
    parser.add_option("--nn-lambda", dest="nn_lambda", type="int",
                    help="Neural network param lambda")
    parser.add_option("--nn-layer1-size", dest="nn_layer1_size", type="int",
                    help="Neural network param layer 1 size")
    parser.add_option("--nn-layer2-size", dest="nn_layer2_size", type="int",
                    help="Neural network param layer 2 size")
    parser.add_option("--nn-layer3-size", dest="nn_layer3_size", type="int",
                    help="Neural network param layer 3 size")

    (options, args) = parser.parse_args()

    if not options.train_data or not options.numproc or not options.cv_data\
            or not options.events_json or not options.events_gen_dir\
            or not options.nn_lambda or not options.nn_layer1_size or not options.nn_layer2_size\
            or not options.nn_layer3_size:
        raise KeyError('Not all required options specified')

    return options


def generate_program_file(options):
    tfile = tempfile.mktemp()
    with open(tfile, 'wb') as programfile:
        writer = csv.writer(programfile, delimiter=',')
        row = [options.nn_lambda, '1e-3', options.nn_layer1_size, options.nn_layer2_size, options.nn_layer3_size]
        writer.writerow(row)

    return tfile


def main():
    options = get_options()
    programfile = generate_program_file(options)

    proc = subprocess.Popen(['./run_train_parallel.py', '--train-data', options.train_data, '--cv-data',
                             options.cv_data, '--numproc', str(options.numproc), '--events-json', options.events_json,
                             '--events-gen-dir', options.events_gen_dir, '--program', programfile])
    return_code = proc.wait()


if __name__ == '__main__':
    main()