#!/bin/sh
BASE_PATH=/home/lamerman/work/ml/BlindMotionProject
NUM_EL_GYR_ACC=20
NUM_EL_SPEED=5

/usr/bin/python -u $BASE_PATH/code/detector/data_prepaire/prepaire.py -i $BASE_PATH/Sensors/2014-09-18_SensorDatafile_smooth.csv -o /mnt/ramfs/out-2014-09-18.csv --time-delta-events-msec 500 --num-el-gyr-acc $NUM_EL_GYR_ACC --num-el-speed $NUM_EL_SPEED -e $BASE_PATH/Events/20140918/all.json
/usr/bin/python -u $BASE_PATH/code/detector/data_prepaire/prepaire.py -i $BASE_PATH/Sensors/2014-09-17_SensorDatafile_smooth.csv -o /mnt/ramfs/out-2014-09-17.csv --time-delta-events-msec 500 --num-el-gyr-acc $NUM_EL_GYR_ACC --num-el-speed $NUM_EL_SPEED -e $BASE_PATH/Events/20140917/all.json
/usr/bin/python -u $BASE_PATH/code/detector/data_prepaire/prepaire.py -i $BASE_PATH/Sensors/2014-12-16_SensorDatafile_smooth.csv -o /mnt/ramfs/out-2014-12-16.csv --time-delta-events-msec 500 --num-el-gyr-acc $NUM_EL_GYR_ACC --num-el-speed $NUM_EL_SPEED -e $BASE_PATH/Events/20141216/all.json

cat /mnt/ramfs/out-2014-*.csv > /mnt/ramfs/out.csv
octave -q ~/work/ml/BlindMotionProject/code/detector/core/prepaire.m /mnt/ramfs/out.csv /mnt/ramfs/out.mat
