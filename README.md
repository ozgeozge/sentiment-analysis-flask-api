# Problem description

Automatizing the process of classifying customer reviews as negative or positive is crucial for e-commerce companies.  This project provides a solution to this problem. The project includes the following steps: 

- Train a machine learning model to score product reviews, recognizing how positive or negative they are.
- Expose this model as an API so that a website can display automatic product rankings.
- Build a small sample webpage to demonstrate this functionality.


# Getting Started

You can find all the information to run/build the application on your local or Docker in this document.

## Prerequisites

- Python 3.11
- Jupyter Notebook
- Docker

## Preparation

In order to train the model, movie reviews dataset in Python NLTK library is used.


## Model Training
- The jupyter notebook file `train_sentiment_analysis.ipynb` contains text processing and training steps. 
- The trained model is saved as `sa_classifier.pickle` file which will be used in sentiment classification.

## Build and run locally

- Run `pipenv shell` to create and activate a virtual environment
- `requirements.txt` will be automatically converted to `Pipfile`.
- Run `pipenv install` to install dependencies. It will also create `Pipfile.lock` file.
- Run `python predict.py` command to spin up a Flask API endpoint to return the prediction of the given request.
- To test the endpoint, you can run below cURL command:

```shell
curl  -X POST \
  'http://localhost:9696/predict' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "review": "amazing unforgettable movie"
}'
```

- You will get the result below after running the previous command:

```json
{
  "result": "pos"
}
```

## Build and run via Docker

- Run `docker build -t sentiment-prediction .` command in the root directory of the project to create a docker image.
- Run `docker run -it -p 9696:9696 sentiment-prediction:latest` to run a container which serves an API endpoint which exposes container default port `9696` to local `9696` port. Now, the app which is running inside the docker container is accessible with the address `http://localhost:9696`.
- To test the endpoint, you can run below cURL command:

```shell
curl  -X POST \
  'http://localhost:9696/predict' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "review": "amazing unforgettable movie"
}'
```

- You will get the result below after running the previous command:

```json
{
  "result": "pos"
}
```
## Test the endpoint from the web page

Open `sentiment.html` file on a web browser, write the review into the text box and click the button to display the score.