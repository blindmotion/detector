#!/bin/sh

while true; do
    octave -q main.m ~/work/ml/BlindMotionProject/workspace/results/full-trIdle-30-2/out.mat >> out.log;
    octave -q predict.m result.mat ~/work/ml/BlindMotionProject/workspace/results/cv-trIdle-30-2/out.mat >> log.txt;
    /home/lamerman/work/ml/BlindMotionProject/code/detector/data_prepaire/predict_events.sh >> log.txt;
    ~/work/ml/BlindMotionProject/code/detector/data_prepaire/compaire_events.py -a ~/work/ml/BlindMotionProject/Events/20141126/all.json -p ~/work/ml/BlindMotionProject/workspace/events_gen/events.json >> log.txt;

    echo "\n\n ***KHRU*** \n\n" >> log.txt
done
