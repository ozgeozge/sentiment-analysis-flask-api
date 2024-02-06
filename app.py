import json
import pickle
import re
from string import punctuation
import sys

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
# Replace these values with your own bucket and file information
S3_BUCKET_NAME = 'YOUR_BUCKET_NAME_HERE'
S3_FILE_NAME = 'YOUR_FILE_NAME_HERE'

# Download your model from S3 and use pickle to load it
# model = <COMPLETE_THIS>
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

def lambda_handler(event, context):
    # Your main Lambda function here
    # Check https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
    # for more information on how to process the event input and
    # how to return the response
    
    bdy = event['body']
    rev_dict = json.loads(bdy)
    review = rev_dict['review']
    result = get_sentiment(review)
    return { "body": json.dumps({
            "result": str(result),
        }),
    }


""" if __name__ == '__main__':
     get_sentiment(sys.argv[1]) """
