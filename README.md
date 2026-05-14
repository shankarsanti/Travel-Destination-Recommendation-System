# 🌍 Travel Destination Recommendation System

An AI-powered travel recommendation platform built with Python Flask, SQLite, and modern web technologies. Features intelligent recommendations, real-time weather data, Google Maps integration, an AI chatbot, and auto-generated itineraries.

---

## ✨ Features

- **AI-Based Recommendations** — Collaborative filtering using cosine similarity and user behavior tracking
- **Chatbot Assistant** — NLP-powered chatbot for budget, destination type, and season queries
- **Real-Time Weather** — Live weather data with 5-day forecasts via Open-Meteo API
- **Google Maps Integration** — Embedded maps with nearby attractions and directions
- **Budget Planner** — Interactive cost calculator with detailed breakdowns
- **Itinerary Generator** — Auto-generated day-by-day travel plans
- **Reviews & Ratings** — User reviews with star ratings
- **Wishlist System** — Save favorite destinations
- **Admin Dashboard** — Complete analytics and content management
- **Smart Search** — AJAX-powered live search with autocomplete

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **APIs:** Open-Meteo (Weather), Google Maps Embed
- **AI Engine:** Cosine Similarity, Collaborative Filtering

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install flask werkzeug requests
```

### 2. Run the Application
```bash
python3 app.py
```

### 3. Access the App
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 4. Demo Credentials
| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `testuser2` | `test1234` |

---

## 📁 Project Structure

```
├── app.py                      # Main Flask application
├── database.py                 # Database schema & initialization
├── recommendation_engine.py    # AI recommendation engine
├── seed_data.py                # Sample data seeder
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── templates/                  # HTML templates
│   ├── index.html
│   ├── explore.html
│   ├── destination.html
│   ├── dashboard.html
│   └── admin/                  # Admin templates
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## 🧠 AI Recommendation Algorithm

The system uses collaborative filtering to provide personalized recommendations:

1. Track user interactions (views, wishlists, reviews)
2. Build user-destination interaction matrix
3. Calculate cosine similarity between users
4. Find similar users and recommend their preferred destinations
5. Weighted scoring: type (35%) + budget (25%) + season (20%) + duration (10%) + rating (10%)

---

## 📄 License

This project is for educational purposes. Built as a college project demonstrating full-stack web development with AI-based recommendation systems.
