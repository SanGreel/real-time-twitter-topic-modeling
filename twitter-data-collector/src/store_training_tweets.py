import tweepy
import json
from pymongo import MongoClient
import sys

# $1 - db name
g_db_name = sys.argv[1]

print ("DB name: ", g_db_name)

class StreamListener(tweepy.StreamListener):
    """tweepy.StreamListener is a class provided by tweepy used to access
    the Twitter Streaming API to collect tweets in real-time.
    """

    def on_connect(self):
        """Called when the connection is made"""
        print("You're connected to the streaming server.")

    def on_error(self, status_code):
        """This is called when an error occurs"""
        print('Error: ' + repr(status_code))
        return False

    def on_data(self, data):
        """This will be called each time we receive stream data"""
        client = MongoClient()

        # I stored the tweet data in a database called 'training_tweets' in MongoDB, if 
        # 'training_tweets' does not exist it will be created for you.
        # db = client.g_db_name
        db = client[g_db_name]

        # Decode JSON
        datajson = json.loads(data)

        # I'm only storing tweets in English. I stored the data for these tweets in a collection 
        # called 'training_tweets_collection' of the 'training_tweets' database. If 
        # 'training_tweets_collection' does not exist it will be created for you. 
        if "lang" in datajson and datajson["lang"] == "en":
            db.training_tweets_collection.insert_one(datajson)


if __name__ == "__main__":

    # These are provided to you through the Twitter API after you create a account
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth1.set_access_token(access_token, access_token_secret)

    # LOCATIONS are the longitude, latitude coordinate corners for a box that restricts the 
    # geographic area from which you will stream tweets. The first two define the southwest
    # # corner of the box and the second two define the northeast corner of the box. 
    LOCATIONS = [-124.7771694, 24.520833, -66.947028, 49.384472,        # Contiguous US
                 -164.639405, 58.806859, -144.152365, 71.76871,         # Alaska
                 -160.161542, 18.776344, -154.641396, 22.878623]        # Hawaii

    # LOCATIONS = [-74.272749, 40.579724, -73.678206, 40.976252]          # New York

    stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    stream = tweepy.Stream(auth=auth1, listener=stream_listener)
    stream.filter(locations=LOCATIONS)
