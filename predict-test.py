import requests


url = 'http://localhost:9696/predict'

review = {"review": "amazing unforgettable movie"}

response = requests.post(url, json=review).json()
print(response)
