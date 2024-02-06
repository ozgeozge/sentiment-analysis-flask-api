FROM python:3.11.7-slim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ["predict.py", "sa_classifier.pickle", "/app"]

# Port information will be set via env variables from Heroku
# Also, port information can be passed to the container via -e flag while running the docker container

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app", "--timeout 5"]