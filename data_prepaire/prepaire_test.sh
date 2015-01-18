#!/bin/sh
BASE_PATH=/home/lamerman/work/ml/BlindMotionProject
WORK_PATH=/home/lamerman/work/ml/BlindMotionProject/workspace
NUM_EL_GYR_ACC=20
NUM_EL_SPEED=5

rm $WORK_PATH/out-2014-11-30.csv

/usr/bin/python -u $BASE_PATH/code/detector/data_prepaire/prepaire.py -i $BASE_PATH/Sensors/2014-11-30_SensorDatafile_smooth.csv -o $WORK_PATH/out-2014-11-30.csv --time-delta-events-msec 10 --num-el-gyr-acc $NUM_EL_GYR_ACC --num-el-speed $NUM_EL_SPEED -e $BASE_PATH/Events/20141130/all.json

cat $WORK_PATH/out-2014-11-30.csv > $WORK_PATH/out.csv
octave -q $BASE_PATH/code/detector/core/prepaire.m $WORK_PATH/out.csv $WORK_PATH/out.mat
