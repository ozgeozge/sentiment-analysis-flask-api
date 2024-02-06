import json
import pickle
import re
from string import punctuation
import sys
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import nltk
from nltk.corpus import stopwords
from nltk.util import everygrams
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize


# You need to specify the download dir because not
# all paths are available in Lambda
nltk.data.path.append("/tmp")
nltk.download('stopwords', download_dir = "/tmp")
nltk.download('omw-1.4', download_dir = "/tmp")
nltk.download("punkt", download_dir = "/tmp")
nltk.download('wordnet', download_dir = "/tmp")


with open('sa_classifier.pickle', 'rb') as f_in:
     model = pickle.load(f_in)

stopwords_eng = stopwords.words('english')
lemmatizer = WordNetLemmatizer()


def bag_of_words(words):                                                                                                                                                                                       
    bag = {}                                                                                                                                                                                                   
    for w in words:                                                                                                                                                                                            
        bag[w] = bag.get(w,0)+1                                                                                                                                                                                
    return bag


def is_useful_word(word):
    return (word not in stopwords_eng) and (word not in punctuation) 

def extract_features(document):
    words = word_tokenize(document)
    lemmas = [str(lemmatizer.lemmatize(w)) for w in words if is_useful_word(w)]
    document = " ".join(lemmas)
    document = document.lower()
    document = re.sub(r'[^a-zA-Z0-9\s]', ' ', document)
    words = [w for w in document.split(" ") if w != "" and is_useful_word(w)]
    return [str('_'.join(ngram)) for ngram in list(everygrams(words, max_len=3))]

def get_sentiment(review):
    words = extract_features(review)
    words = bag_of_words(words)
    result =model.classify(words) 
    print(result)
    return result





app = Flask('predictflask')
CORS(app)
@app.route('/predict', methods=['POST'])
def predict():
    rev_dict = request.get_json()
    review = rev_dict['review']
    pred = get_sentiment(review)

    result = {
        'result': str(pred)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)


#This is a development server. install and use "gunicorn" for deployment server.
#pip install gunicorn
#gunicorn --bind 0.0.0.0:9696 predict:app