# 🧰 7. Technologies Used

A professional-grade technology stack chosen for reliability, performance, and ease of deployment.

---

## 📊 Technology Stack Overview

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | HTML5 | 5 | Page structure & semantic elements |
| **Frontend** | CSS3 | 3 | Glassmorphism styling, animations, responsive design |
| **Frontend** | JavaScript (ES6+) | ES6 | DOM manipulation, AJAX, interactivity |
| **Frontend** | Jinja2 | 3.1.2 | Server-side template rendering |
| **Backend** | Python | 3.9+ | Core application language |
| **Backend** | Flask | 3.0.0 | Lightweight web framework (routing, sessions, requests) |
| **Backend** | Werkzeug | 3.0.1 | WSGI utilities, password hashing (PBKDF2-SHA256) |
| **Database** | SQLite3 | Built-in | Lightweight, serverless relational database |
| **Font** | Google Fonts (Inter) | — | Modern, clean typography |

---

## 🖥️ Frontend Technologies

### HTML5
- Semantic elements (`<nav>`, `<main>`, `<section>`, `<footer>`)
- Accessible form inputs with labels
- SEO-friendly meta tags and heading structure

### CSS3
- **Glassmorphism design** with `backdrop-filter: blur(20px)`
- **CSS Custom Properties** (variables) for consistent theming
- **CSS Grid & Flexbox** for responsive layouts
- **Keyframe animations** — fade-up, slide-in, hover transforms
- **Media queries** — breakpoints at 768px and 480px
- **Gradient backgrounds** — radial gradients for depth

### JavaScript (Vanilla ES6+)
- **Navbar scroll effects** — sticky with background change on scroll
- **Flash message auto-dismiss** — timed fade-out animations
- **Star rating input** — interactive click-to-rate system
- **AJAX wishlist toggle** — add/remove without page reload
- **Live search API** — real-time destination search suggestions
- **Intersection Observer** — scroll-triggered animations

### Jinja2 Templating
- **Template inheritance** — `base.html` → child templates
- **Component includes** — `navbar.html`, `footer.html`
- **Dynamic rendering** — loops, conditionals, filters
- **Context processors** — user data injected into all templates

---

## ⚙️ Backend Technologies

### Python 3.9+
- Clean, readable syntax for rapid development
- Built-in `sqlite3` module for database operations
- `functools.wraps` for custom decorators
- Strong standard library support

### Flask 3.0.0
- **Routing** — 20+ URL routes with variable rules
- **Request handling** — GET/POST form data and query parameters
- **Session management** — secure server-side user sessions
- **Flash messages** — categorized user notifications
- **Error handlers** — custom 404 and 500 error pages
- **Context processors** — inject user data into templates
- **Blueprint-ready** — modular route organization

### Werkzeug 3.0.1
- **Password hashing** — PBKDF2-SHA256 algorithm
- **Password verification** — `check_password_hash()`
- **Security utilities** — safe string comparison, URL handling

---

## 🗄️ Database Technology

### SQLite3
- **Serverless** — no separate database server needed
- **Zero configuration** — database file auto-created on first run
- **Portable** — single `travel.db` file contains all data
- **Built-in Python support** — `sqlite3` module included in standard library
- **Row factory** — dictionary-like access to query results
- **Foreign keys** — relational integrity between tables

### Schema: 7 Tables

```
users ─────────┬── reviews ──── destinations
               ├── wishlist ─── destinations
               ├── itineraries ── destinations
               └── preferences

contact_messages (standalone)
```

---

## 🛠️ Development Tools

| Tool | Purpose |
|------|---------|
| **VS Code** | Primary code editor with Python & HTML extensions |
| **Git** | Version control and source code management |
| **GitHub** | Remote repository hosting and collaboration |
| **Chrome DevTools** | Frontend debugging, responsive design testing |
| **Python pip** | Package manager for installing dependencies |
| **SQLite Browser** | Database inspection and debugging (optional) |
| **Terminal (zsh)** | Command-line development and server management |

---

## 🔌 APIs & Endpoints

### Built-in REST APIs

| Endpoint | Method | Response | Purpose |
|----------|--------|----------|---------|
| `/api/destinations` | GET | JSON | List all destinations with key fields |
| `/api/search?q=` | GET | JSON | Search destinations by name or state |

### Optional API Integrations (Future Scope)

| API | Purpose | Status |
|-----|---------|--------|
| **Google Maps API** | Interactive maps with destination markers | 🔮 Planned |
| **OpenWeatherMap API** | Real-time weather data for destinations | 🔮 Planned |
| **Unsplash API** | High-quality destination images | 🔮 Planned |
| **Google Places API** | Reviews and ratings from Google | 🔮 Planned |

---

## 📦 Dependencies

### `requirements.txt`

```
Flask==3.0.0
Werkzeug==3.0.1
Jinja2==3.1.2
```

> **Note:** SQLite3 and Python standard libraries require no additional installation.

---

## 🔄 Why This Stack?

| Decision | Reasoning |
|----------|-----------|
| **Flask over Django** | Lightweight, minimal boilerplate, ideal for focused applications |
| **SQLite over MySQL** | Zero-config, portable, sufficient for project scale, no server needed |
| **Vanilla JS over React** | No build tools required, simpler deployment, faster page loads |
| **Jinja2 Templates** | Server-side rendering, tight Flask integration, SEO-friendly |
| **PBKDF2-SHA256** | Industry-standard password hashing, built into Werkzeug |
| **CSS Custom Properties** | Maintainable theming, easy color/style updates |
