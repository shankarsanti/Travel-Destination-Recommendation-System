# 🏗️ 5. System Architecture

## 3-Tier Architecture

The system follows a **3-tier architecture** for clear separation of concerns:

```
┌──────────────────────────────────────────────────────────┐
│                    3-TIER ARCHITECTURE                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌──────────────────────────────────────────────────┐   │
│   │           🖥️  FRONTEND (UI Layer)                │   │
│   │                                                  │   │
│   │   • User interaction & presentation              │   │
│   │   • HTML5, CSS3 (Glassmorphism), JavaScript      │   │
│   │   • Jinja2 Templates (server-side rendering)     │   │
│   │   • Responsive design (Mobile + Desktop)         │   │
│   │                                                  │   │
│   │   Pages: Home, Explore, Recommend, Login,        │   │
│   │          Profile, Wishlist, Itinerary, Admin      │   │
│   └──────────────────────┬───────────────────────────┘   │
│                          │ HTTP Requests                  │
│                          ▼                               │
│   ┌──────────────────────────────────────────────────┐   │
│   │          ⚙️  BACKEND (Logic Layer)               │   │
│   │                                                  │   │
│   │   • Request processing & business logic          │   │
│   │   • Python 3.9+ with Flask 3.0 framework        │   │
│   │   • Recommendation Engine (weighted scoring)     │   │
│   │   • Authentication (Werkzeug PBKDF2-SHA256)      │   │
│   │   • Session management & access control          │   │
│   │                                                  │   │
│   │   Modules: app.py, recommendation_engine.py,     │   │
│   │            config.py, seed_data.py               │   │
│   └──────────────────────┬───────────────────────────┘   │
│                          │ SQL Queries                    │
│                          ▼                               │
│   ┌──────────────────────────────────────────────────┐   │
│   │          🗄️  DATABASE (Data Layer)               │   │
│   │                                                  │   │
│   │   • Stores destinations, users & preferences     │   │
│   │   • SQLite3 (lightweight, serverless)            │   │
│   │   • 7 Tables with foreign key relationships      │   │
│   │   • Auto-initialized with schema on first run    │   │
│   │                                                  │   │
│   │   Tables: users, destinations, reviews,          │   │
│   │           wishlist, itineraries, preferences,    │   │
│   │           contact_messages                       │   │
│   └──────────────────────────────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Layer Details

### 🖥️ Layer 1: Frontend (UI Layer)

**Purpose:** User interaction and visual presentation

| Component | Technology | Role |
|-----------|-----------|------|
| Structure | HTML5 | Page layout and semantic elements |
| Styling | CSS3 (Glassmorphism) | Dark theme, animations, responsive design |
| Interactivity | JavaScript (Vanilla) | Navbar, flash messages, AJAX wishlist, live search |
| Templating | Jinja2 | Server-side rendering with template inheritance |
| Font | Inter (Google Fonts) | Modern, clean typography |

**Key Design Decisions:**
- Glassmorphism with `backdrop-filter: blur(20px)` for premium feel
- Dark mode reduces eye strain and looks professional
- Responsive breakpoints at 768px (tablet) and 480px (mobile)

---

### ⚙️ Layer 2: Backend (Logic Layer)

**Purpose:** Business logic, request processing, and recommendation engine

| Component | Technology | Role |
|-----------|-----------|------|
| Framework | Flask 3.0 | HTTP routing, request handling, session management |
| Language | Python 3.9+ | Core application logic |
| Auth | Werkzeug | Password hashing (PBKDF2-SHA256), session cookies |
| Engine | Custom Algorithm | Weighted multi-criteria scoring for recommendations |

**Route Categories:**
- **Public Routes** — Home, Explore, Destination Detail, Recommend, Contact
- **Auth Routes** — Login, Register, Logout
- **User Routes** — Profile, Wishlist, Reviews, Itinerary
- **Admin Routes** — Dashboard, Manage Destinations/Users/Messages
- **API Routes** — JSON endpoints for destinations and search

---

### 🗄️ Layer 3: Database (Data Layer)

**Purpose:** Persistent storage for all application data

| Component | Technology | Role |
|-----------|-----------|------|
| Engine | SQLite3 | Lightweight, serverless, file-based database |
| File | `travel.db` | Auto-generated on first application run |
| Schema | 7 Tables | Users, destinations, reviews, wishlist, itineraries, preferences, contact_messages |

**Database Schema:**

```
users ──────────┐
  │              │
  ├── reviews ───┤── destinations
  │              │        │
  ├── wishlist ──┘        │
  │                       │
  ├── itineraries ────────┘
  │
  ├── preferences
  │
  └── (contact_messages - standalone)
```

---

## Data Flow

```
User Input ──▶ Flask Route ──▶ Database Query ──▶ Recommendation Engine
                                                          │
User Screen ◀── Jinja2 Template ◀── Scored Results ◀──────┘
```

### Example Flow: Getting Recommendations

1. **User** fills preference form (type, budget, season, duration)
2. **Flask** receives POST request at `/recommend`
3. **Database** returns all destinations
4. **Recommendation Engine** scores each destination using weighted algorithm
5. **Results** sorted by match score and converted to match percentage
6. **Jinja2** renders the results page with ranked destination cards
7. **Browser** displays results with match % bars and details

---

## Security Architecture

| Feature | Implementation |
|---------|---------------|
| Password Hashing | PBKDF2-SHA256 via Werkzeug |
| Session Management | Flask secure sessions with secret key |
| Access Control | `@login_required` and `@admin_required` decorators |
| Input Validation | Server-side validation on all forms |
| CSRF Protection | Flask session-based protection |
