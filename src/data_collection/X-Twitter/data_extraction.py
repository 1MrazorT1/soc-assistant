import os
import requests
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
print(f"Bearer Token: {BEARER_TOKEN}")


def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

def search_tweets(query, max_results=20):
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,text,author_id"
    }
    response = requests.get(url, headers=create_headers(), params=params)
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code} {response.text}")
    return response.json()

query = '("compromised" OR "ransomware" OR "IOC" OR "breach") has:links -is:retweet lang:en'
tweets = search_tweets(query)

for tweet in tweets.get("data", []):
    print(f"{tweet['created_at']} - {tweet['text']}\n")
