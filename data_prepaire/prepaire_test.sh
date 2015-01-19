#!/bin/sh
BASE_PATH=/home/lamerman/work/ml/BlindMotionProject
WORK_PATH=/home/lamerman/work/ml/BlindMotionProject/workspace
NUM_EL_GYR_ACC=20
NUM_EL_SPEED=5

TEST_DATE_1=2014-11-26
TEST_DATE_2=20141126

rm $WORK_PATH/out-${TEST_DATE_1}.csv

/usr/bin/python -u $BASE_PATH/code/detector/data_prepaire/prepaire.py -i $BASE_PATH/Sensors/${TEST_DATE_1}_SensorDatafile_smooth.csv -o $WORK_PATH/out-${TEST_DATE_1}.csv --time-delta-events-msec 10 --num-el-gyr-acc $NUM_EL_GYR_ACC --num-el-speed $NUM_EL_SPEED -e $BASE_PATH/Events/${TEST_DATE_2}/all.json

cat $WORK_PATH/out-${TEST_DATE_1}.csv > $WORK_PATH/out.csv
octave -q $BASE_PATH/code/detector/core/prepaire.m $WORK_PATH/out.csv $WORK_PATH/out.mat
