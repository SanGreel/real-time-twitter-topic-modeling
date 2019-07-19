import re
import nltk
import urllib
from nltk.stem import WordNetLemmatizer 
from utils.channels_to_filter import channels_not_to_consider

nltk.download('stopwords')
nltk.download('wordnet')

tokenizer = nltk.WordPunctTokenizer()
lemmatizer = WordNetLemmatizer()
stop_word_list = nltk.corpus.stopwords.words('english')

def filter_tweet(tweet):
    
    """Filter out tweets based on their length.

    Parameters:
    tweet (str): tweet itself

    Returns:
    bool: indicator if to filter tweet

   """
    
    if not isinstance(tweet, str):
        is_filtered = True
    elif len(tweet.split(' ')) < 3:
        is_filtered = True
    else: 
        is_filtered = False
        
    return not is_filtered
         
def process_text(tweet, lemmatizer=lemmatizer, tokenizer=tokenizer, stop_word_list=stop_word_list):
    
    """Classic text processing.

    Parameters:
    tweet (str): tweet itself
    lemmatizer (obj): nltk object for lemmatization
    tokenizer (obj): nltk object for tokenization
    stop_word_list (list): list with stop words

    Returns:
    list: list of tokens, which represent input tweet 

   """
   
    tweet = tweet.lower() # get lowercase
    tweet = re.sub(r'@\w+', '', tweet) # filter words with non-letters at the beginning (mainly for mentions)
    tweet = re.sub(r'http://\S{,280}', '', tweet) # filter http
    tweet = re.sub(r'https://\S{,280}', '', tweet) # filter https
    tweet = re.sub(r'[^A-Za-z]', ' ', tweet) # filter all non-letters
    tweet = re.sub(r'\s{2,}', ' ', tweet) # remove multiply whitespaces
    tweet = re.sub(r'(.)\1{2,}', r'\1', tweet) # remove repeated chars (e.g. "greeeeat" -> "great")
    tweet = tweet.strip() # remove possible whitespaces from both sides of the tweet

    # lemmatize, tokenize and conquer
    processed_tweet = [lemmatizer.lemmatize(token) for token in tokenizer.tokenize(tweet)
                       if token not in stop_word_list]
    
    return processed_tweet


def process_hashtags(tweet, lemmatizer=lemmatizer, stop_word_list=stop_word_list):
    
    """Filter out all text except hashtags

    Parameters:
    tweet (str): tweet itself
    lemmatizer (obj): nltk object for lemmatization
    stop_word_list (list): list with stop words

    Returns:
    list: list of tokens, which represent input tweet 

   """
   
    tweet = tweet.lower() # get lowercase
    hashtags = re.findall(r"#(\w+)", tweet)
    hashtags = [lemmatizer.lemmatize(hashtag) for hashtag in hashtags if hashtag not in stop_word_list]

    return hashtags


def get_response(url):
    
    """Get response by url.

    Parameters:
    url (str): url to query

    Returns:
    str: string which represents html response from url or None if url doesn't respond

   """
    
    try:
        response = urllib.request.urlopen(url).read().decode()
        return response
    except:
        return None
    

def get_keywords(html):
    
    """Parse keywords from html

    Parameters:
    html (str): html to parse

    Returns:
    str: keywords

   """
    
    # use regex to find meta
    keywords = re.findall('<meta name="keywords" content="(.+)"', html)
    
    if len(keywords) > 0:
        keywords = keywords[0]
    
        # filter keywrods
        keywords = keywords.lower() # get lowercase
        keywords = re.sub(r'[^A-Za-z]', ' ', keywords) # filter all non-letters
        keywords = re.sub(r'\s{2,}', ' ', keywords) # remove multiply whitespaces
        keywords = re.sub(r'(.)\1{2,}', r'\1', keywords) # remove repeated chars (e.g. "greeeeat" -> "great")
        keywords = keywords.strip() # remove possible whitespaces from both sides of the tweet
    else:
        keywords = ''
    
    return keywords


def get_description(html):
    
    """Parse description from html

    Parameters:
    html (str): html to parse

    Returns:
    str: description

   """
    
    # use regex to find meta
    description = re.findall('<meta name="description" content="(.+)"', html)
    
    if len(description) > 0:
        description = description[0]
    
        # filter description
        description = description.lower() # get lowercase
        description = re.sub(r'[^A-Za-z]', ' ', description) # filter all non-letters
        description = re.sub(r'\s{2,}', ' ', description) # remove multiply whitespaces
        description = re.sub(r'(.)\1{2,}', r'\1', description) # remove repeated chars (e.g. "greeeeat" -> "great")
        description = description.strip() # remove possible whitespaces from both sides of the tweet
    else:
        description = ''
    
    return description
   
    
def process_urls(tweet, tokenizer=tokenizer):
    
    """Filter out all text except urls and parse them

    Parameters:
    tweet (str): tweet itself
    lemmatizer (obj): nltk object for lemmatization
    tokenizer (obj): nltk object for tokenization
    stop_word_list (list): list with stop words

    Returns:
    list: list of tokens from keywords from url
    list: list of tokens from url's description

   """
    
    # find urls in tweet
    urls = re.findall(r"https(.+)", tweet)
                                  
    if len(urls) > 0:                              
        urls = ['https' + url for url in urls]

        # query urls
        responses = [get_response(url) for url in urls]

        # parse urls for keywords and description
        keywords = [[_ for _ in tokenizer.tokenize(get_keywords(response))] for response in responses if response is not None]
        descriptions = [[_ for _ in tokenizer.tokenize(get_description(response))] for response in responses if response is not None]
    
        # flatten lists
        flatten = lambda l: [item for sublist in l for item in sublist]
        keywords = flatten(keywords)
        descriptions = flatten(descriptions)
    
        # merging keywords with descriptions
        keywords.extend(descriptions)
        
        return keywords
    
    else:
        return []
