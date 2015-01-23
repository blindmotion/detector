#!/bin/sh

BM=/home/lamerman/work/ml/BlindMotionProject

cd $BM/code/detector/core
octave -q predict_events.m result.mat $BM/workspace/events_gen/data.mat $BM/workspace/events_gen/time.csv $BM/workspace/events_gen/out_y.csv $BM/workspace/events_gen/out_time.csv
cd $BM/code/detector/data_prepaire
./post_process_events.py -d $BM/workspace/events_gen/out_y.csv -t $BM/workspace/events_gen/out_time.csv -o $BM/workspace/events_gen/events.json
