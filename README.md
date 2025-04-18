# 🔍 Multi-Site Product Scraper & Alert System

Search and monitor electronics components from **Amazon.in**, **Robu.in**, and **RoboCraze**, with intelligent ranking and email alerts for restocks.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Features

- 🔎 **Unified Search** across Amazon, Robu, RoboCraze
- ⚖️ **Smart Product Ranking** using sentence-transformers
- 📬 **Email Alerts** for out-of-stock products
- ⏱️ **Caching** with MongoDB to reduce scraping load
- 🤖 **Headless Selenium Scraping** for real-time data
- 📊 Ranking based on **relevance + price + availability**

---

## 📦 Requirements

- Python 3.8+
- Google Chrome + ChromeDriver
- MongoDB (local or Atlas)
- Gmail account (for alert emails)

---

## 🛠️ Installation

```bash
git clone https://github.com/PSP21-ux/MultiSiteProductFinder.git
cd MultiSiteProductFinder
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ⚙️ Usage

1. Start MongoDB server locally
2. Run the Flask app:

```bash
python app.py
```

3. Visit `http://localhost:5000` in your browser.

---

## ✉️ Email Alert Setup

Update these in `app.py`:
```python
EMAIL_USERNAME = "youremail@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use Gmail App Passwords
```

---

## 📂 Project Structure

```
.
├── app.py                # Flask backend
├── amazon_scraper.py
├── robu_scraper.py
├── robocraze_scraper.py
├── alertscraping.py
├── ml_ranker.py
├── requirements.txt
├── templates/
│   └── index.html
```

---

## 📄 License

MIT License. Use freely, credit appreciated 😊
