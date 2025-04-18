# 🔍 Multi-Site Product Scraper & Availability Alert System

Search and monitor electronics components from Amazon.in, Robu.in, and RoboCraze. Get notified by email when out-of-stock products become available.

## Features
- Unified search across 3 stores
- ML-based product ranking (relevance, price, availability)
- Email alerts for restocks
- Background availability checker
- Cached results via MongoDB

## Setup Instructions

```bash
git clone https://github.com/your-username/multi-site-product-scraper.git
cd multi-site-product-scraper
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then visit: http://127.0.0.1:5000/

## Technologies
- Flask
- Selenium
- MongoDB
- SentenceTransformers
