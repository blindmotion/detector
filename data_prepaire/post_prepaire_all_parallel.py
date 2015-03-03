#!/usr/bin/python

import os

BASE_PATH='/home/lamerman/work/ml/BlindMotionProject'
WORK_PATH='/home/lamerman/work/ml/BlindMotionProject/workspace'
NUM_EL_GYR_ACC=20
NUM_EL_SPEED=5

datesTrain = [
    ('2014-09-17', '20140917'),
    ('2014-10-15', '20141015'),
    ('2014-10-16', '20141016'),
    ('2014-10-17', '20141017'),
    # ('2014-10-18', '20141018'),
    # ('2014-10-23', '20141023'),
    # ('2014-10-24', '20141024'),
    # ('2014-10-25', '20141025'),
    # ('2014-11-29', '20141129'),
    # ('2014-11-30', '20141130'),
    # ('2014-12-16', '20141216'),
    # ('2015-01-25', '20150125'),
]

datesCV = [
    ('2014-09-18', '20140918'),
    ('2014-11-25', '20141125'),
]

datesTest = [
    ('2014-11-26', '20141126'),
    ('2014-10-14', '20141014'),
]

# cleanup

os.system('rm {WORK_PATH}/outTrain.csv'.format(WORK_PATH=WORK_PATH))
os.system('rm {WORK_PATH}/outCV.csv'.format(WORK_PATH=WORK_PATH))

# train

for dat in datesTrain:
    os.system('cat {WORK_PATH}/out-{date}.csv >> {WORK_PATH}/outTrain.csv'.
        format(WORK_PATH=WORK_PATH, date=dat[0]))

os.system('octave -q {BASE_PATH}/code/detector/core/prepaire.m \
    {WORK_PATH}/outTrain.csv {WORK_PATH}/outTrain.mat'
    .format(BASE_PATH=BASE_PATH, WORK_PATH=WORK_PATH))

# cv

for dat in datesCV:
    os.system('cat {WORK_PATH}/out-{date}.csv >> {WORK_PATH}/outCV.csv'.
        format(WORK_PATH=WORK_PATH, date=dat[0]))

os.system('octave -q {BASE_PATH}/code/detector/core/prepaire.m \
    {WORK_PATH}/outCV.csv {WORK_PATH}/outCV.mat'
    .format(BASE_PATH=BASE_PATH, WORK_PATH=WORK_PATH))

# cleanup

os.system('rm {WORK_PATH}/outTrain.csv'.format(WORK_PATH=WORK_PATH))
os.system('rm {WORK_PATH}/outCV.csv'.format(WORK_PATH=WORK_PATH))
