import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Replace 'YOUR 3BG0ZSUWOYFNO49P  with your actual NewsAPI key
NEWSAPI_KEY = 'YOUR_NEWSAPI_KEY'
URL = f'https://newsapi.org/v2/everything?q=gold&apiKey={NEWSAPI_KEY}'

def fetch_news():
    response = requests.get(URL)
    articles = response.json().get('articles', [])
    return articles

def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment

def main():
    articles = fetch_news()
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        content = title + ' ' + description
        sentiment = analyze_sentiment(content)
        
        print(f"Title: {title}")
        print(f"Sentiment: {sentiment}")
        print('-' * 40)

if __name__ == "__main__":
    main()
