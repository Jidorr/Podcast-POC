import requests
import json
from config.config import API_KEY

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'sortBy=popularity&'
       f'apiKey={API_KEY}')

response = requests.get(url)

print(response.json())