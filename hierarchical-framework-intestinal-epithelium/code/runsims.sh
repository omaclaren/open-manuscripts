#!/bin/bash
now=$(date +"%m_%d_%Y_%H%M_%S")
jupyter nbconvert --ExecutePreprocessor.timeout=None --to html --execute sampling_simulations.ipynb
mv sampling_simulations.html sampling_simulations_$1_$now.html