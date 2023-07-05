"""_Sentiment Analysis Algorithm API_
@author:
    Jakob Balkovec

@date:
    July 5th, 2023

@version:
    2.0

@license:
    This code is licensed under the MIT License.

@file:
    main.py

@description:
    This script implements a sentiment analysis algorithm API that determines the sentiment 
    polarity (positive, negative, or neutral) of textual data. 
    It utilizes the TextBlob library for sentiment analysis.
    
@usage:

    Run this script with the necessary dependencies installed and provide the text data to be analyzed. 
    The algorithm will output the sentiment polarity score for each input.
@example:
    $ python main.py
    from textblob import TextBlob
"""
import json
import json
from flask import Flask, render_template, redirect, render_template
from extremes import get_max, get_min

from main import establish_nltk, read_data, handle_data, write_data_to_file
from main import IN_FILE_, OUT_FILE_, PAUSE_

app = Flask(__name__, template_folder='template')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #no caching
    
"""__summary__
:desc: Analyzes data and renders the 'intro.html' template.

:param: None

:return: None
"""
@app.route('/', methods=['GET'])
def analyze_data():
    establish_nltk()
    return render_template('intro.html')

"""__summary__
:desc: A function that loads more data.

:return: str: The rendered template.
"""
@app.route('/load_more_data', methods=['POST'])
def load_more_data():
    data = read_data(IN_FILE_)
    handle_data(data, print_data=False)
    write_data_to_file(data, OUT_FILE_)
    return render_template('analyze.html', data=data[5:])

"""__summary__
:desc: Retrieves the maximum polarity from the given input data and returns it in a formatted JSON string.

:param: None

:return: str: A JSON string containing the maximum polarity value.
"""
@app.route('/get_max_polarity', methods=['POST'])
def get_max_polarity():
    data = read_data(IN_FILE_)
    handle_data(data, print_data=False)
    write_data_to_file(data, OUT_FILE_)
    data_out = get_max()
    pretty_data = json.dumps(data_out, indent=4)
    return render_template('max.html', data=pretty_data)

"""__summary__
:desc: Redirects the user to the GitHub page of j-balkovec.

:param: None

:return: None
"""
@app.route('/go_to_github', methods=['POST'])
def go_to_github():
    return redirect(location="https://github.com/j-balkovec", code=302)

"""__summary__
:desc: A route to get the minimum polarity.

:param: None

:return: A rendered template with the minimum polarity data.
"""
@app.route('/get_min_polarity', methods=['POST'])
def get_min_polarity():
    data = read_data(IN_FILE_)
    handle_data(data, print_data=False)
    write_data_to_file(data, OUT_FILE_)
    data_out = get_min()
    pretty_data = json.dumps(data_out, indent=4)
    return render_template('max.html', data=pretty_data)

"""__summary__
:desc: Acquires a data set by redirecting the user to the specified URL.

:param: None

:return: None
"""
@app.route('/acquire_data_set', methods=['POST'])
def acquire_data_set():
    return redirect(location="https://brightdata.com/products/datasets/Twitter", code=302)

"""__summary__ 
:desc: View data from the specified route using the POST method.

:return: The rendered analyze.html template with the data.
"""
@app.route('/view_data', methods=['POST'])
def view_data():
    establish_nltk()
    data = read_data(IN_FILE_)
    handle_data(data, print_data=False)

    return render_template('analyze.html', data=data)

if __name__ == '__main__':
    app.run(debug=False)
