#!/bin/bash

# $1 - date and month if format dd_mm, e.g 23_06
dd_mm=$1

## Pull the data from MongoDB as a json file
mongoexport --db "usa_training_tweets_"${dd_mm} --collection training_tweets_collection --out "usa_training_tweets_"${dd_mm}".json"

## Convert json to csv
python src/tweets_json_to_csv.py "./usa_training_tweets_"${dd_mm}".json" "usa_training_tweets_"${dd_mm}".csv"