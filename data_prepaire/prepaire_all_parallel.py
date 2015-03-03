#!/usr/bin/python

import os

BASE_PATH='/home/lamerman/work/ml/BlindMotionProject'
WORK_PATH='/home/lamerman/work/ml/BlindMotionProject/workspace'
NUM_EL_GYR_ACC=20
NUM_EL_SPEED=5

os.system('rm $WORK_PATH/out-201*.csv')

dates = [
    ('2014-09-17', '20140917'),
    ('2014-09-18', '20140918'),
    ('2014-10-14', '20141014'),
    ('2014-10-15', '20141015'),
    ('2014-10-16', '20141016'),
    ('2014-10-17', '20141017'),
    ('2014-10-18', '20141018'),
    ('2014-10-23', '20141023'),
    ('2014-10-24', '20141024'),
    ('2014-10-25', '20141025'),
    ('2014-11-25', '20141125'),
    ('2014-11-26', '20141126'),
    ('2014-11-29', '20141129'),
    ('2014-11-30', '20141130'),
    ('2014-12-16', '20141216'),
    ('2015-01-25', '20150125'),
    ]
template = 'nohup /usr/bin/python \
    -u {BASE_PATH}/code/detector/data_prepaire/prepaire.py \
    -i {BASE_PATH}/Sensors/{date_u}_SensorDatafile_smooth.csv \
    -o {WORK_PATH}/out-{date_u}.csv --time-delta-events-msec 500 \
    --num-el-gyr-acc {NUM_EL_GYR_ACC} --num-el-speed {NUM_EL_SPEED} \
    -e {BASE_PATH}/Events/{date}/all.json&'

for dat in dates:
    cmd = template.format(date_u=dat[0], date=dat[1], BASE_PATH=BASE_PATH,
            WORK_PATH=WORK_PATH, NUM_EL_GYR_ACC=NUM_EL_GYR_ACC,
            NUM_EL_SPEED=NUM_EL_SPEED)
    os.system(cmd)
