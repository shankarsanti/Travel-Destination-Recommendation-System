# 🌍 Travel Destination — Travel Destination Recommendation System

> **Discover amazing destinations tailored to your preferences.** An AI-Powered Travel Recommendation System built with Python Flask, SQLite, and modern web technologies. Features collaborative filtering, real-time weather integration, Google Maps, an AI chatbot, auto-generated itineraries, and a stunning glassmorphic UI.

---

## 🚀 Features (15 Industry-Level Modules)

### 🤖 AI & Intelligence
| # | Feature | Description |
|---|---------|-------------|
| 1 | **AI-Based Recommendation** | Collaborative filtering using cosine similarity + user behavior tracking |
| 2 | **Chatbot Assistant** | NLP-powered floating chatbot — understands budget, type, season queries |
| 3 | **Smart Search** | AJAX-powered live search with autocomplete |

### 📊 User Experience
| # | Feature | Description |
|---|---------|-------------|
| 4 | **Personalized Dashboard** | Stats, saved destinations, AI recommendations, search history, notifications |
| 5 | **Real-Time Weather** | Live weather data via Open-Meteo API with 5-day forecast |
| 6 | **Google Maps Integration** | Embedded maps, nearby attractions, route directions |
| 7 | **Budget Planner** | Detailed breakdown + interactive custom calculator (travelers × days) |
| 8 | **Itinerary Generator** | Auto-generated day-by-day travel plans based on destination data |
| 9 | **Image Gallery** | Multi-image gallery with thumbnail navigation |

### 👥 Social & Community
| # | Feature | Description |
|---|---------|-------------|
| 10 | **Reviews & Ratings** | Star ratings with comments on every destination |
| 11 | **Wishlist/Favorites** | Save destinations with AJAX toggle |
| 12 | **Notification System** | Weather alerts, deals, new destination alerts |

### 🛠️ Administration
| # | Feature | Description |
|---|---------|-------------|
| 13 | **Admin Dashboard** | Analytics, user management, destination CRUD |
| 14 | **Trending Destinations** | Dynamic trending section based on ratings |
| 15 | **Search History Tracking** | Logged searches for personalization |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, Flask |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Styling** | Custom CSS with Glassmorphism design |
| **APIs** | Open-Meteo (Weather), Google Maps Embed |
| **AI Engine** | Cosine Similarity, Collaborative Filtering |
| **Authentication** | Session-based with password hashing |

---

## 📁 Project Structure

```
TRAVEL DESTINATION RECOMMENDATION SYSTEM/
├── app.py                      # Main Flask application (routes, controllers)
├── database.py                 # Database schema & initialization
├── recommendation_engine.py    # AI recommendation + chatbot + itinerary engine
├── seed_data.py                # Sample data seeder
├── config.py                   # App configuration
├── requirements.txt            # Python dependencies
├── travel.db                   # SQLite database (auto-created)
├── templates/
│   ├── base.html               # Base template with chatbot widget
│   ├── index.html              # Home page (hero + trending)
│   ├── explore.html            # Explore destinations (filter/sort)
│   ├── destination.html        # Detail page (weather, maps, itinerary, reviews)
│   ├── recommend.html          # Smart recommendation form
│   ├── dashboard.html          # Personalized user dashboard
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── profile.html            # User profile & preferences
│   ├── wishlist.html           # Saved destinations
│   ├── itinerary.html          # Trip planning
│   ├── components/
│   │   ├── navbar.html         # Navigation bar
│   │   └── footer.html         # Footer
│   └── admin/
│       ├── dashboard.html      # Admin analytics
│       ├── destinations.html   # Manage destinations
│       ├── add_destination.html
│       ├── edit_destination.html
│       ├── users.html          # Manage users
│       └── messages.html       # Contact messages
└── static/
    ├── css/style.css           # All styles (glassmorphism + components)
    └── js/main.js              # Client-side JS (chatbot, gallery, search)
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install flask werkzeug requests
```

### 2. Run the Application
```bash
python3 app.py
```

### 3. Open in Browser
```
http://127.0.0.1:5000
```

### 4. Demo Credentials
| Role | Username | Password |
|------|----------|----------|
| 🛠️ Admin | `admin` | `admin123` |
| 👤 User | `testuser2` | `test1234` |

---

## 📸 Key Pages

### 🏠 Home Page
- Hero section with gradient typography
- Trending destinations carousel
- Stats counters (20+ destinations, 8 types, 4 seasons)
- Floating chatbot widget

### 📍 Destination Detail Page
- **Image Gallery** with clickable thumbnails
- **Weather Widget** — live temperature, humidity, wind, 5-day forecast
- **Google Maps** — embedded map with directions link
- **Budget Breakdown** — bar chart visualization
- **Custom Calculator** — travelers × days cost estimator
- **Auto Itinerary** — day-by-day timeline with activities & tips
- **Reviews** — star rating + comments
- **Similar Destinations** — AI-powered recommendations

### 📊 User Dashboard
- Stats cards (Saved, Reviews, Trips, Views)
- Travel Profile (auto-detected preferences)
- AI Recommendations ("Users like you visited...")
- Notifications (weather, deals, new destinations)
- Search History
- Quick Actions

### 🤖 Chatbot
- Understands: budget, destination type, season, price range
- Example queries: "beach under ₹15,000", "adventure destinations", "luxury winter trip"
- Returns destination cards with images and links

---

## 🧠 AI Recommendation Algorithm

```
1. Track user interactions (views, wishlists, reviews)
2. Build user-destination interaction matrix
3. Calculate cosine similarity between users
4. Find top-K similar users
5. Recommend destinations visited by similar users
6. Weighted scoring: type(35%) + budget(25%) + season(20%) + duration(10%) + rating(10%)
```

---

## 📌 Database Schema

| Table | Purpose |
|-------|---------|
| `users` | User accounts with profiles |
| `destinations` | All destination data (20+ entries) |
| `reviews` | User ratings & comments |
| `wishlist` | Saved destinations |
| `itineraries` | Trip planning |
| `preferences` | User preference profiles |
| `user_activity` | View/interaction tracking for AI |
| `search_history` | Search query logging |
| `notifications` | Alert system |
| `contact_messages` | Contact form submissions |

---

## 👤 Authors

- **Student**: College Project — Travel Destination Recommendation System
- **Built with**: Python Flask, SQLite, HTML/CSS/JS

---

## 📄 License

This project is for educational purposes. Built as a college project demonstrating full-stack web development with AI-based recommendation systems.
