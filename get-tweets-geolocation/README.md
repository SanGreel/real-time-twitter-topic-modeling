## Get tweets by geolocation

## Start storing tweets to mongo db (be sure that ```mongo``` started)
```python src/store_training_tweets.py```

## Pull the data from MongoDB as a json file
```mongoexport --db training_tweets --collection training_tweets_collection --out training_tweets.json```

## Convert json to csv
```python src/tweets_json_to_csv.py ./training_tweets.json ./training_tweets.csv```
