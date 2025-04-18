import requests
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_news_api_key():
    """Get News API key from environment variables"""
    return os.getenv("NEWSAPI_API_KEY")

def fetch_news(query, days=7, api_key=None, page=1, max_results=100):
    """Fetch news articles matching the query from the last N days
    
    Args:
        query (str): Search query
        days (int): Number of days to look back
        api_key (str): NewsAPI key (defaults to environment variable)
        page (int): Page number for pagination
        max_results (int): Maximum number of results to return (max 100 per page)
    
    Returns:
        tuple: (articles, total_results) - list of articles and total number of results available
    """
    if api_key is None:
        api_key = get_news_api_key()
    
    base_url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": query,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "from": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
        "page": page,
        "pageSize": min(max_results, 100)  # NewsAPI limits to 100 per page
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["articles"], data.get("totalResults", 0)
        else:
            print(f"Error fetching news: {response.status_code}")
            return [], 0
    except Exception as e:
        print(f"Error fetching news: {e}")
        return [], 0

def generate_mock_data(num_articles=10, city=None):
    """Generate mock articles for testing"""
    mock_events = [
        {"type": "concert", "location": city or "San Francisco", "date": "next Saturday"},
        {"type": "road closure", "location": f"{city or ''} Downtown".strip(), "date": "tomorrow"},
        {"type": "construction", "location": f"Highway near {city}" if city else "Highway 101", "date": "next week"},
        {"type": "festival", "location": f"{city} Park" if city else "Golden Gate Park", "date": "this weekend"},
        {"type": "marathon", "location": f"Main Street in {city}" if city else "Market Street", "date": "Sunday morning"}
    ]
    
    articles = []
    for i in range(num_articles):
        event = random.choice(mock_events)
        articles.append({
            "title": f"{event['type'].title()} in {event['location']}",
            "description": f"A {event['type']} is scheduled in {event['location']} {event['date']}.",
            "content": f"A {event['type']} is scheduled in {event['location']} {event['date']}. This event is expected to draw large crowds and may affect traffic in the surrounding areas.",
            "publishedAt": datetime.now().isoformat(),
            "source": {"name": "Mock News"}
        })
    return articles

def generate_mock_data_for_city(city, num_articles=10):
    """Generate mock data customized for the given city"""
    return generate_mock_data(num_articles, city) 