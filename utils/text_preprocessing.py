import re
import nltk
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


def process_urls(tweet, tokenizer=tokenizer):
    
    """Filter out all text except urls and parse them

    Parameters:
    tweet (str): tweet itself
    lemmatizer (obj): nltk object for lemmatization
    tokenizer (obj): nltk object for tokenization
    stop_word_list (list): list with stop words

    Returns:
    list: list of tokens, which represent input tweet 

   """
    
    pass