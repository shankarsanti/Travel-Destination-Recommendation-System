# 🧩 6. Modules

The Travel Destination Recommendation System is organized into **three core modules**, each responsible for a distinct area of functionality. Each module includes **core features** (required) and **extra features** (beyond requirements).

---

## 👤 Module 1: User Module

Handles all user-facing operations from registration to destination interaction.

### Core Features

| Feature | Description | Route |
|---------|-------------|-------|
| **Registration** | New users create accounts with username, email, password | `/register` |
| **Login / Logout** | Secure authentication with PBKDF2-SHA256 hashing | `/login`, `/logout` |
| **Enter Travel Preferences** | Select budget, travel type, season, and duration | `/recommend` |
| **View Recommended Destinations** | See ranked results with match percentage scores | `/recommend` (POST) |
| **View Details & Attractions** | Full destination page with highlights, how-to-reach, budget breakdown | `/destination/<id>` |

### ⭐ Extra Features

| Feature | Description | Route |
|---------|-------------|-------|
| **⭐ Star Rating & Reviews** | Submit 1-5 star ratings with comments for visited destinations | `/review/<id>` |
| **❤️ Wishlist / Favorites** | Save/remove favorite destinations with one click (AJAX support) | `/wishlist` |
| **📋 Trip Itinerary Planner** | Create travel plans with title, dates, notes, and linked destinations | `/itinerary` |
| **👤 Profile Management** | Update full name, email, phone, and view activity history | `/profile` |
| **📊 Preference Memory** | System remembers user preferences for future recommendations | Auto-saved |
| **💰 Budget Calculator** | Automated cost breakdown (accommodation, food, transport, activities) | `/destination/<id>` |
| **🔍 Live Search** | Real-time destination search with instant suggestions via API | `/api/search` |
| **📱 Responsive Design** | Full mobile + tablet + desktop support | All pages |

### Implementation Files

| File | Role |
|------|------|
| `app.py` (lines 180–400) | Auth routes, user routes (profile, wishlist, reviews, itinerary) |
| `templates/login.html` | Login form with glassmorphism card |
| `templates/register.html` | Registration form with validation |
| `templates/profile.html` | User profile, reviews, preferences display |
| `templates/wishlist.html` | Saved destinations grid with remove option |
| `templates/itinerary.html` | Trip planner with add/delete forms |
| `templates/destination.html` | Detail page with reviews, budget breakdown, similar places |

### User Flow

```
Register ──▶ Login ──▶ Set Preferences ──▶ View Recommendations
                              │
                              ├──▶ View Destination Details
                              │         │
                              │         ├──▶ Add to Wishlist ❤️
                              │         ├──▶ Write Review ⭐
                              │         └──▶ View Budget Breakdown 💰
                              │
                              ├──▶ Plan Itinerary 📋
                              │
                              └──▶ Update Profile 👤
```

---

## 🛠️ Module 2: Admin Module

Provides administrative control over the system's content and users.

### Core Features

| Feature | Description | Route |
|---------|-------------|-------|
| **Add Destination** | Form to create new destinations with all fields (type, budget, season, etc.) | `/admin/destinations/add` |
| **Update Destination** | Edit existing destination details | `/admin/destinations/edit/<id>` |
| **Delete Destination** | Remove destination and its associated reviews/wishlists | `/admin/destinations/delete/<id>` |
| **Manage Users** | View all registered users, delete users | `/admin/users` |
| **Maintain Database** | System auto-initializes and seeds data on first run | Auto |

### ⭐ Extra Features

| Feature | Description | Route |
|---------|-------------|-------|
| **📊 Analytics Dashboard** | Overview with total destinations, users, reviews, wishlists, unread messages | `/admin` |
| **📈 Type Distribution Chart** | Visual bar breakdown of destinations by travel type | `/admin` |
| **🕐 Recent Activity Feed** | Latest reviews and newly registered users at a glance | `/admin` |
| **👥 User Activity Stats** | Per-user review count and wishlist count in user table | `/admin/users` |
| **📧 Contact Message Center** | Read/manage contact form submissions from users | `/admin/messages` |
| **📬 Unread Message Counter** | Badge showing number of unread messages in navbar | `/admin` |
| **🔒 Role-Based Access** | `@admin_required` decorator protects all admin routes | All admin routes |
| **🗑️ Cascade Delete** | Deleting a destination removes its reviews and wishlist entries | Auto |

### Implementation Files

| File | Role |
|------|------|
| `app.py` (lines 403–555) | Admin routes with `@admin_required` decorator |
| `templates/admin/dashboard.html` | Analytics dashboard with 5 stat cards |
| `templates/admin/destinations.html` | Destination management table (CRUD) |
| `templates/admin/add_destination.html` | Add/Edit destination form (15 fields) |
| `templates/admin/users.html` | User management table with stats |
| `templates/admin/messages.html` | Contact messages viewer with read status |

### Admin Flow

```
Login (Admin) ──▶ Dashboard ──┬──▶ Manage Destinations (Add/Edit/Delete)
                   │          ├──▶ Manage Users (View/Delete)
                   │          └──▶ View Contact Messages
                   │
                   └──▶ View Analytics
                          ├── Total Stats (5 cards)
                          ├── Type Distribution (bar chart)
                          ├── Recent Reviews
                          └── Recent Users
```

### Access Control

- Protected by `@admin_required` decorator
- Only users with `is_admin = 1` in the database can access
- Default admin account: `admin` / `admin123`

---

## 🤖 Module 3: Recommendation Module

The core intelligence of the system — analyzes user input and generates personalized destination suggestions.

### Core Features

| Feature | Description |
|---------|-------------|
| **Analyze User Input** | Receives preferences: travel type, budget, season, duration, max cost |
| **Apply Filtering Logic** | Weighted scoring algorithm with 5 criteria |
| **Generate Personalized Suggestions** | Ranked list of destinations with match percentage |

### ⭐ Extra Features

| Feature | Description |
|---------|-------------|
| **🔗 Related Type Matching** | Understands semantic links (adventure ↔ nature ↔ wildlife) |
| **📊 Match Percentage Display** | Visual progress bars showing how well each destination matches |
| **🔍 Similar Destinations** | Auto-suggests related places on each destination detail page |
| **💰 Budget Breakdown Engine** | Splits cost into accommodation (35%), food (20%), transport (25%), activities (12%), misc (8%) |
| **🔥 Trending Destinations** | Top-rated destinations shown on homepage |
| **📅 Duration Proximity Scoring** | Flexible matching — close durations still score well |
| **💵 Max Cost Filter** | Hard budget cap in addition to category-based budget matching |
| **💾 Preference Persistence** | Saves user preferences for logged-in users |

### Weighted Scoring Algorithm

```
Score = (Type Match × 3.0) + (Budget Match × 2.5) + (Season Match × 2.0)
      + (Duration Match × 1.5) + (Rating Score × 1.0)
```

| Criteria | Weight | Scoring Logic |
|----------|--------|---------------|
| **Travel Type** | 3.0 | Exact = 100%, Partial = 50%, Related type = 30% |
| **Budget** | 2.5 | Exact = 100%, Adjacent category = 40-60% |
| **Season** | 2.0 | Exact = 100%, "All season" = 100%, Partial = 70% |
| **Duration** | 1.5 | Exact = 100%, ±2 days = 70%, ±4 days = 40% |
| **Rating** | 1.0 | Proportional to 5-star scale |

### Related Type Mapping

The engine understands semantic relationships between travel types:

```
Adventure  ←→  Nature, Wildlife, Hill Station
Beach      ←→  Nature
Historical ←→  Cultural, Pilgrimage
Nature     ←→  Adventure, Wildlife, Hill Station, Beach
Cultural   ←→  Historical, Pilgrimage
Wildlife   ←→  Nature, Adventure
Pilgrimage ←→  Cultural, Historical
Hill Station ←→ Nature, Adventure
```

### Implementation Files

| File | Role |
|------|------|
| `recommendation_engine.py` | Core algorithm (5 functions, 118 lines) |
| `app.py` (lines 148–176) | `/recommend` route that calls the engine |
| `templates/recommend.html` | Preference form + results display with match bars |

### Recommendation Flow

```
User Preferences ──▶ Fetch All Destinations ──▶ Score Each Destination
        │                                              │
        │                                              ▼
        │                                    Sort by Score (DESC)
        │                                              │
        └─── Save Preferences (if logged in)           ▼
                                              Render Ranked Results
                                              with Match Percentage
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `get_recommendations()` | Main entry — scores all destinations against preferences |
| `calculate_score()` | Calculates weighted relevance score for one destination |
| `get_similar_destinations()` | Finds similar places based on a destination's attributes |
| `get_budget_breakdown()` | Splits total cost into accommodation, food, transport, etc. |
| `get_trending_destinations()` | Returns top-rated destinations for homepage |

---

## 📋 Feature Summary — All Modules

### Core Features (Required)

| # | Feature | Module |
|---|---------|--------|
| 1 | User Registration & Login | User |
| 2 | Travel Preference Input | User |
| 3 | Destination Recommendation | Recommendation |
| 4 | Destination Details View | User |
| 5 | Add / Edit / Delete Destinations | Admin |
| 6 | Manage Users | Admin |
| 7 | Maintain Database | Admin |
| 8 | Filtering Logic | Recommendation |
| 9 | Personalized Suggestions | Recommendation |

### ⭐ Extra Features (Beyond Requirements)

| # | Feature | Module | Benefit |
|---|---------|--------|---------|
| 1 | ⭐ Star Ratings & Reviews | User | Social proof and community feedback |
| 2 | ❤️ Wishlist / Favorites | User | Save destinations for future trips |
| 3 | 📋 Travel Itinerary Planner | User | Complete trip planning with dates |
| 4 | 💰 Budget Calculator | Recommendation | Detailed cost breakdown per trip |
| 5 | 🔗 Similar Destinations | Recommendation | Discover related places easily |
| 6 | 🔥 Trending Destinations | Recommendation | Quick access to top-rated places |
| 7 | 📊 Admin Analytics Dashboard | Admin | Visual stats and activity monitoring |
| 8 | 📈 Type Distribution Chart | Admin | Understand destination variety |
| 9 | 📧 Contact Message System | Admin | User-to-admin communication |
| 10 | 🤖 Related Type Matching | Recommendation | Smarter, fuzzy recommendations |
| 11 | 🔍 Live Search API | User | Instant search results |
| 12 | 📱 Fully Responsive Design | All | Works on mobile, tablet, desktop |
| 13 | 🎨 Glassmorphism UI | All | Premium dark theme with animations |
| 14 | 🌤️ Best Season Indicators | Recommendation | Timing recommendations per destination |
| 15 | 💵 Max Cost Filter | Recommendation | Hard budget cap for precise filtering |
| 16 | 💾 Preference Persistence | User | Remembers choices for logged-in users |
| 17 | 📬 Flash Notifications | All | Auto-dismiss success/error messages |
| 18 | 🔒 Role-Based Access Control | Admin | Secure admin-only routes |

