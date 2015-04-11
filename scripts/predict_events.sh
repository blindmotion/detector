#!/bin/sh

BM=/home/lamerman/work/ml/BlindMotionProject

TEMP_FILE_Y=$(eval mktemp -u)
TEMP_FILE_TIME=$(eval mktemp -u)

echo TEMP_FILE_Y $TEMP_FILE_Y
echo TEMP_FILE_TIME $TEMP_FILE_TIME

cd $BM/code/detector/core
octave -q predict_events.m $1 $BM/workspace/events_gen/results/2014-09-18/data.mat $BM/workspace/events_gen/results/2014-09-18/time.csv $TEMP_FILE_Y $TEMP_FILE_TIME
cd $BM/code/detector/scripts
./post_process_events.py -d $TEMP_FILE_Y -t $TEMP_FILE_TIME -o $2 --epsilon 1 --min-samples 7
