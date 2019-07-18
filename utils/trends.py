import operator
from datetime import datetime
from pyspark.sql import Row


wrong_date = datetime.strptime("Mon Jun 03 00:00:00 +0000 2000", '%a %b %d %H:%M:%S %z %Y')

def validate(date_text):
    """
    Validate date in str

    Parameters:
    date_text (str):  datetimne in str format 

    Returns:
    (boolean): boolean status about validation 
    """
    
    try:
        if date_text != datetime.strptime(date_text, '%a %b %d %H:%M:%S %z %Y').strftime('%a %b %d %H:%M:%S %z %Y'):
            raise ValueError
        return True
    except ValueError:
        return False

    
def str_tweet_to_datetime(frame_datetime):
    
    """
    Convert tweet date to datetime

    Parameters:
    frame_datetime (str):  tweet frame date in str 

    Returns:
    datetime (datetimne): converted datetime format 
    """


    if (validate(frame_datetime) == True):
        return datetime.strptime(frame_datetime,'%a %b %d %H:%M:%S %z %Y')
    else:
        return wrong_date

def datetime_to_tweet_str(frame_datetime):
    
    """
    Convert datetime to str

    Parameters:
    frame_datetime (str):  datetime 

    Returns:
    ts (str): datetime in str format
    """

    ts = datetime.strftime(frame_datetime, '%a %b %d %H:%M:%S %z %Y')
    return ts

    
def get_geo_name(geo):
    
    """
    get geo information

    Parameters:
    geo (str):  geo US or US-NY 

    Returns:
    (str): get extended geo information
    """
                
    if geo == "US-NY":
        return "New York"
    elif geo == "US":
        return "United States"
    return ""

def print_google_trend_title(start_date, finish_date, name, geo):
    
    """
    print google trends in suitable way

    Parameters:
    start_date (datetime):  start date 
    
    finish_date (datetime): end date
    
    geo (str) geo info
    
    """
    start_date_str = start_date.strftime("%Y-%m-%d")
    
    if start_date == finish_date:
        print(f"\nGoogle trends {name} in {get_geo_name(geo)} during {start_date_str}")
    else:
        finish_date_str = finish_date.strftime("%Y-%m-%d")
        print(f"\nGoogle trends {name} in {get_geo_name(geo)} during {start_date_str} - {finish_date_str}")
        
