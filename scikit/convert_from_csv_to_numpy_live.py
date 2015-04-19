#!/usr/bin/env python
__author__ = 'lamerman'

import numpy as np
from optparse import OptionParser


def get_options():
    parser = OptionParser()
    parser.add_option("--input-file", dest="inputfile",
                    help="Csv file with events data")
    parser.add_option("--output-file", dest="outputfile",
                    help="The name of output numpy file")

    (options, args) = parser.parse_args()

    if not options.inputfile or not options.outputfile:
        raise KeyError('Not all required options specified')

    return options


def main():
    options = get_options()

    dataset = np.loadtxt(options.inputfile, delimiter=",")

    X = dataset[:, :]

    np.savez(options.outputfile, X=X)


if __name__ == '__main__':
    main()
