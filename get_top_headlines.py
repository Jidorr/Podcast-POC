from newsapi import NewsApiClient
from config.config import API_KEY

# Init
newsapi = NewsApiClient(api_key=API_KEY)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(category='business',
                                          language='en',
                                          country='us',
                                          )

with open('top_headlines.txt', 'w') as file:
    for article in top_headlines.get('articles', []):
        file.write(f"Title: {article.get('title', 'N/A')}\n")
        file.write(f"Description: {article.get('description', 'N/A')}\n")
        file.write(f"Content: {article.get('content', 'N/A')}\n")
        file.write(f"URL: {article.get('url', 'N/A')}\n")
        file.write("\n")