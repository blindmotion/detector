#!/usr/bin/env python
__author__ = 'lamerman'

import pickle
import numpy as np
from optparse import OptionParser
from sklearn.ensemble import RandomForestClassifier


def get_options():
    parser = OptionParser()
    parser.add_option("--data-file", dest="datafile",
                    help="The file with cross validation/test set")
    parser.add_option("--model", dest="model",
                    help="The file with pretrained model")

    (options, args) = parser.parse_args()

    if not options.datafile or not options.model:
        raise KeyError('Not all required options specified')

    return options


def main():
    options = get_options()

    dataset = np.load(options.datafile)

    X = dataset['X']
    y = dataset['y']

    clf = None
    with open(options.model, 'r') as f:
        clf = pickle.load(f)

    score = clf.score(X, y)
    print score


if __name__ == '__main__':
    main()
