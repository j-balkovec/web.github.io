"""_Sentiment Analysis Algorithm_
@author:
    Jakob Balkovec

@date:
    June 26, 2023

@version:
    1.0

@license:
    This code is licensed under the MIT License.

@file:
    main.py

@description:
    This script implements a sentiment analysis algorithm that determines the sentiment 
    polarity (positive, negative, or neutral) of textual data. 
    It utilizes the TextBlob library for sentiment analysis.
    
@usage:

    Run this script with the necessary dependencies installed and provide the text data to be analyzed. 
    The algorithm will output the sentiment polarity score for each input.
@example:
    $ python main.py
    from textblob import TextBlob
"""

"""_note_
Sentiment Analysis Algorithm
Go into "myenv" in the conda environment where all the dependencies are installed
"""

"""__plan__"""
'''
Make a separate file that finds the extremes to see if the algo is working properly
Data visualization
Testing
Bug Checking & Optimization
'''

"""__imports__"""
import csv
import json
import time
from typing import List, Any
import re
from enum import Enum
import nltk
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
import multiprocessing as mp
from extremes import find_extremes #extremes.py

"""__constants__"""
IN_FILE_: str = "mock_data/mock_m.csv"

OUT_FILE_: str = "out/output.json"
HEADER_: str = "\n\n[sentiment analysis algorithm]\n\n"
PAUSE_: Any = 0.5

"""__summary__
:desc: (function) Establishes the necessary setup for NLTK by checking if 
the 'vader_lexicon' dataset is already downloaded. 
If it is not found, it downloads the dataset.

:return: None
"""
def establish_nltk() -> None:
    if 'vader_lexicon.zip' in nltk.data.path:
        print("['vader_lexicon' dataset is already downloaded]\n")
    else:
        print("['vader_lexicon' dataset not found, downloading now]...\n")
        nltk.download('vader_lexicon')
        print("['vader_lexicon' dataset downloaded]\n")
        
"""_summary_
:desc: (function) Cleans the text by removing URLs, special characters, and excess whitespace.

:param: text (str): The text to be cleaned.

:return: str: The cleaned text.
"""
def clean_tweet(text: str) -> str:
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'[^\w\s.]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('.', '') #removes full stops
    
    return text.strip()

"""__summary__
:desc: (function) Reads data from a CSV file and returns a list of dictionaries.

:param filename: str -> The name of the CSV file to read data from.
:param debug: bool -> A flag indicating whether to enable debug mode.

:return: List[dict] -> A list of dictionaries containing the data from the CSV file.

:raises FileNotFoundError: If the specified file could not be found.
"""
def read_data(filename: str) -> List[dict]:
    try:
        data = []
        with open(filename, 'r', encoding='latin-1') as file:
            csv_reader = csv.reader(file)
            total_items = sum(1 for _ in csv_reader) - 1
            file.seek(0) 
            next(csv_reader)
            with tqdm(total=total_items, desc="[reading data...]    ") as pbar:
                for row in csv_reader:
                    polarity, id, date, _, user, text = row
                    clean_text = clean_tweet(text)
                    data.append({'polarity': polarity, 'id': id, 'date': date, 'user': user, 'text': clean_text})
                    pbar.update(1)
            print("\n")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"[the file '{filename}' could not be found]")
    
"""_summary_
:desc: (function) Convert the given list of dictionaries to a JSON string.

:param: data (List[dict]): A list of dictionaries to be converted.

:return: str: The JSON string representation of the input data.
""" 
def convert_to_json(data: List[dict]) -> str:
    return json.dumps(data, indent=4)

"""__summary__
:desc: (function) Adds polarity to a given tweet dictionary.

:param: tweet (dict): A dictionary representing a tweet.

:return: dict: The modified tweet dictionary with the added 'polarity' field.
"""
def get_tweet_polarity(tweet: dict, sentiment_analyzer: SentimentIntensityAnalyzer) -> float:
    polarity = sentiment_analyzer.polarity_scores(tweet['text'])['compound']
    return polarity

"""__summary__
{ (enum class): Polarity
    :desc: Polarity of a tweet.
}

{ (function): classify_tweet
    :desc: Classifies a tweet based on its polarity.

    :param: polarity (float): The polarity of the tweet.

    :return: str: The classification of the tweet ("Positive", "Negative", or "Neutral").
}
"""
class Polarity(Enum):
    POSITIVE = "[positive]"
    NEGATIVE = "[negative]"
    NEUTRAL = "[neutral]"
    
def classify_tweet(polarity: float) -> str:
    return Polarity.POSITIVE.value if polarity > 0.05 else Polarity.NEGATIVE.value if polarity < -0.05 else Polarity.NEUTRAL.value

"""__summary__
:desc: (function) Process a tweet's information and update the information dictionary with the tweet's 
       polarity and classification.

:param: info (dict): A dictionary containing the tweet's information.
:param: print_data (bool): A boolean indicating whether to print the converted JSON data.
    
:return: None
"""
def process_tweet(info: dict, print_data: bool, sentiment_analyzer: SentimentIntensityAnalyzer) -> None:
    info['polarity'] = get_tweet_polarity(info, sentiment_analyzer)
    info['classification'] = classify_tweet(info['polarity'])
    json_data = convert_to_json(info)
    
    if print_data:
        print(json_data + "\n\n")
        time.sleep(PAUSE_)
        
"""__summary__
:desc: (function) Handle data by iterating through a list of dictionaries and performing certain operations on each dictionary.

:param: data (List[dict]): A list of dictionaries containing data to be processed.
:param: print_data (bool): A boolean flag indicating whether to print the processed data.
:param: debug (bool): A boolean flag indicating whether to enable debug mode.
    
:return: None

:raise: Exception: If any error occurs during data handling.
"""
def handle_data(data: List[dict], print_data: bool) -> None:
    sentiment_analyzer = SentimentIntensityAnalyzer()
    with tqdm(total=len(data), desc="[processing data...] ") as pbar:
        for info in data:
            process_tweet(info, print_data, sentiment_analyzer)
            pbar.update(1)
    print("\n")
    
"""__summary__
:desc: (function) Write the given data to a file.

:param: data (List[dict]): The data to be written to the file.
:param: filename (str): The name of the file to write the data to.

:return: None
"""
def write_data_to_file(data: List[dict], filename: str) -> None:    
    total_items = len(data)
    with tqdm(total=total_items, desc="[writing data...]    ") as pbar:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        pbar.update(total_items)
    print(f"[data written to file]:\t {filename}\n\n")

"""_summary_
:desc: (function) The main function reads data from a CSV file named 'twitter_data.csv' and converts it to a JSON format. 
It then iterates over each tweet in the data list, prints the tweet in a formatted JSON format, 
adds a formatting line break, and pauses for 1 second before printing the next tweet. Finally, 
it prints the entire JSON data and returns an integer value of 0.

:param: None

:return: int: The function returns 0.
"""  
def main() -> None:
    establish_nltk()
    print(HEADER_)
    data = read_data(IN_FILE_)
    handle_data(data, print_data=False)
    write_data_to_file(data, OUT_FILE_)
    find_extremes()

if __name__ == '__main__':
    main()


