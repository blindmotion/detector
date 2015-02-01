#!/bin/sh

while true; do
    octave -q main.m ~/work/ml/BlindMotionProject/workspace/results/full-trIdle-30-2/out.mat >> out.log; octave -q predict.m result.mat ~/work/ml/BlindMotionProject/workspace/results/cv-trIdle-30-2/out.mat >> log.txt
    echo "\n\n ***KHRU*** \n\n" >> log.txt
done
