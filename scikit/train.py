#!/usr/bin/env python
__author__ = 'lamerman'

import pickle
import numpy as np
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA


def get_options():
    parser = OptionParser()
    parser.add_option("--train-data", dest="traindata",
                    help="The file with train data")
    parser.add_option("--cv-data", dest="cvdata",
                    help="The file with cross validation data")
    parser.add_option("--output-file", dest="outputfile",
                    help="The file where the trained model will be written")

    (options, args) = parser.parse_args()

    if not options.traindata or not options.cvdata or not options.outputfile:
        raise KeyError('Not all required options specified')

    return options


def main():
    options = get_options()

    train_data = np.load(options.traindata)

    X_train = train_data['X']
    y_train = train_data['y']

    clf = RandomForestClassifier(max_depth=10, n_estimators=10)
    clf.fit(X_train, y_train)

    cv_data = np.load(options.cvdata)

    X_cv = cv_data['X']
    y_cv = cv_data['y']

    score = clf.score(X_cv, y_cv)
    print 'Cv score is {}'.format(score)

    with open(options.outputfile, 'wb') as f:
        pickle.dump(clf, f)


if __name__ == '__main__':
    main()
