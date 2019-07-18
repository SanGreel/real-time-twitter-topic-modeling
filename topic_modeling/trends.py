from datetime import datetime

wrong_date = datetime.strptime("Mon Jun 03 00:00:00 +0000 2000", '%a %b %d %H:%M:%S %z %Y')

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, '%a %b %d %H:%M:%S %z %Y').strftime('%a %b %d %H:%M:%S %z %Y'):
            raise ValueError
        return True
    except ValueError:
        return False

def str_tweet_to_datetime(frame_datetime):
    if (validate(frame_datetime) == True):
        return datetime.strptime(frame_datetime,'%a %b %d %H:%M:%S %z %Y')
    else:
        return wrong_date

def datetime_to_tweet_str(frame_datetime):
    ts = datetime.strftime(frame_datetime, '%a %b %d %H:%M:%S %z %Y')
    return ts

def tweet2google_timeframe(frame_start_datetime, frame_finish_datetime):
    start_date = str_tweet_to_datetime(frame_start_datetime)
    end_date = str_tweet_to_datetime(frame_finish_datetime)
    tim
    
def get_google_trends_by_geo(geo):
    if geo == 'US':
        return google_trends_search_topics_us, google_trends_search_queries_us
    elif geo == 'US-NY':
        return google_trends_search_topics_us_ny, google_trends_search_queries_us_ny
    
    return None, None
    
def unique_google_trends_by_time_frame(df):
    data = df.collect()
    rising_dict = {}
    top_dict = {}
    
    geo = data[0]['geo']
    columns = df.columns

    for i in range(0, len(data)):
        rising_val = data[i][columns[1]]
        top_value = data[i][columns[2]]
        
        if rising_val in rising_dict:
            rising_dict[rising_val][0] += str_rising_to_float(data[i][columns[3]])
            rising_dict[rising_val][1] += 1
        else:
            rising_dict[rising_val] = [str_rising_to_float(data[i][columns[3]]), 1]
            
        if top_value in top_dict:
            top_dict[top_value][0] += float(data[i][columns[4]])
            top_dict[top_value][1] += 1
        else:
            top_dict[top_value] = [float(data[i][columns[4]]), 1]
    
    
    for key in top_dict:
        top_dict[key] = round(top_dict[key][0] / top_dict[key][1])
        
    for key in rising_dict:
        rising_dict[key] = round(rising_dict[key][0] / rising_dict[key][1])
    
    top_dict = sorted(top_dict.items(), key=operator.itemgetter(1), reverse=True)
    rising_dict = sorted(rising_dict.items(), key=operator.itemgetter(1), reverse=True)
    
    
    seq = []
    len_top = len(top_dict)
    len_rising = len(rising_dict)
    length = max(len_top, len_rising)
    
    row = Row(columns[1], columns[2], columns[3], columns[4], columns[5])
    
    for i in range(0, length):
        rising = rising_dict[i][0] if i < len_rising else ''
        rising_val = f"+{rising_dict[i][1]}%" if i < len_rising else None
        
        top = top_dict[i][0] if i < len_top else ''
        top_val = top_dict[i][1] if i < len_top else None
        
        seq.append(row(rising, top, rising_val, top_val, geo))
    
    dframe = spark.createDataFrame(seq)
    return dframe

def get_geo_name(geo):
    if geo == "US-NY":
        return "New York"
    elif geo == "US":
        return "United States"
    return ""

def print_google_trend_title(start_date, finish_date, name):
    start_date_str = start_date.strftime("%Y-%m-%d")
    if start_date == finish_date:
        print(f"\nGoogle trends {name} in {get_geo_name(geo)} during {start_date_str}")
    else:
        finish_date_str = finish_date.strftime("%Y-%m-%d")
        print(f"\nGoogle trends {name} in {get_geo_name(geo)} during {start_date_str} - {finish_date_str}")
        
def convert_datetime_in_interesting_google(df):
    columns = df.columns
    converted_df = df.rdd.map(lambda x : (
                                          x["Date"].strftime("%Y-%m-%d"), 
                                          x[columns[1]], 
                                          x[columns[2]], 
                                          x[columns[3]],
                                          x[columns[4]],
                                          x[columns[5]])).toDF([columns[0], columns[1], columns[2], columns[3], columns[4], columns[5]])
                                                
    return converted_df

def str_rising_to_float(str):
    if str is None:
        return 0.0
    if str == '':
        return 0.0
    if str == 'Breakout':
        return 0.0
    
    str_value = str.split('%')[0]
    if '+' in str_value:
        str_value = str_value.split('+')[1]
        
    if ',' in str_value:
        str_value = str_value.replace(',', '.')
        value = 1000* float(str_value)
        return value
    return float(str_value)