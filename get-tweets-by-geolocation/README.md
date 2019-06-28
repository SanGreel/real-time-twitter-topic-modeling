## Get tweets by geolocation

## Create virtual environment and activate it
```virtualenv venv && source venv/bin/activate```

## Install libs from requirements.txt
```pip install -r requirements.txt```

## Make sure that you run in the separate screen:
## mac
```mongod```
## ubuntu
```sudo systemctl start mongodb```

## Check that mongo is running
```mongo```

## Start storing tweets to mongo db (be sure that ```mongo``` started)
```python src/store_training_tweets.py usa_training_tweets_dd_mm```

## Pull the data from MongoDB as a json file
```mongoexport --db usa_training_tweets_dd_mm --collection training_tweets_collection --out usa_training_tweets.json```
## Convert json to csv
```python src/tweets_json_to_csv.py ./usa_training_tweets.json ./usa_training_tweets.csv```
## or
```./src/mongo_to_csv.sh dd_mm```


