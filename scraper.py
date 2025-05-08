import requests 
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

class NinersNewsScraper:
    def __init__(self):
        # Load API key from .env file
        load_dotenv()
        self.api_key = os.getenv('NEWS_API_KEY')
        if not self.api_key:
            raise ValueError("Please set NEWS_API_KEY in your .env file")
        
        self.base_url = "https://newsapi.org/v2/everything"
        self.articles = []

    def fetch_articles(self):
        # Calculate date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Parameters for the API request
        params = {
            'q': '("San Francisco 49ers" OR "49ers") AND (NFL OR football)',
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            
            if data['status'] == 'ok':
                for article in data['articles']:
                    self.articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': article['source']['name'],
                        'published': article['publishedAt'],
                        'description': article['description'],
                        'timestamp': datetime.now().isoformat()
                    })
                print(f"Successfully fetched {len(self.articles)} articles")
            else:
                print(f"API returned error: {data.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {str(e)}")

    def save_to_cache(self):
        # Sort articles by published date (most recent first)
        self.articles.sort(key=lambda x: x['published'], reverse=True)
        
        # Take top 10 articles
        top_articles = self.articles[:10]
        
        # Save to JSON file
        with open('news_cache.json', 'w') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'articles': top_articles
            }, f, indent=2)

    def run(self):
        print("Starting to fetch 49ers news...")
        self.fetch_articles()
        self.save_to_cache()
        print("Fetching complete! Results saved to news_cache.json")

if __name__ == "__main__":
    scraper = NinersNewsScraper()
    scraper.run() 