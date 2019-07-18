from datetime import datetime
from utils.trends import str_tweet_to_datetime

wrong_date = datetime.strptime("Mon Jun 03 00:00:00 +0000 2000", '%a %b %d %H:%M:%S %z %Y')

# This function extracts data from *.csv with collected tweets 
# params:
# - historical_start_time: initial date for data extraction
# - historical_finish_time: final date for data extraction
# example of format for historical_start_time and historical_finish_time: 'Fri Jul 05 00:00:00 +0000 2019'.

def get_historical_df(historical_tweets_data, historical_start_time, historical_finish_time, spark):
    print("Range for collected data (history): ", historical_start_time, historical_finish_time)
    
    df = spark.read.csv(historical_tweets_data, inferSchema=True, header=True)
    # remove records with no date
    df = df.na.drop(subset=["created_at"])
    
    # convert string to desired date format
    from datetime import datetime
    from pyspark.sql.functions import col, udf
    from pyspark.sql.types import DateType, TimestampType

    func =  udf (lambda x: str_tweet_to_datetime(x), TimestampType())

    df = df.withColumn('created_at', func(col('created_at')))

    selected_history = df.filter((df.created_at > historical_start_time) & (df.created_at < historical_finish_time))

    return selected_history

