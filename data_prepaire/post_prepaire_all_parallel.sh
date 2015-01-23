#!/bin/sh
BASE_PATH=/home/lamerman/work/ml/BlindMotionProject
WORK_PATH=/home/lamerman/work/ml/BlindMotionProject/workspace
NUM_EL_GYR_ACC=20
NUM_EL_SPEED=5

cat $WORK_PATH/out-2014-* > $WORK_PATH/out.csv
octave -q $BASE_PATH/code/detector/core/prepaire.m $WORK_PATH/out.csv $WORK_PATH/out.mat
