# 🗄️ 8. Database Design

The system uses **SQLite3** as its relational database with **7 tables** to store all application data. The database file (`travel.db`) is auto-created and initialized on first run.

---

## 📊 Database Overview

| Property | Value |
|----------|-------|
| **Engine** | SQLite3 (serverless, file-based) |
| **File** | `travel.db` (auto-generated) |
| **Tables** | 7 |
| **Relationships** | Foreign keys linking users → destinations |
| **Initialization** | `database.py` → `init_db()` |
| **Seed Data** | `seed_data.py` → 20 destinations + 1 admin user |

---

## 🔗 Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐
│    users     │       │   destinations   │
│──────────────│       │──────────────────│
│ PK id        │       │ PK id            │
│    username  │       │    name          │
│    email     │       │    country       │
│    password  │       │    state         │
│    full_name │       │    description   │
│    phone     │       │    image_url     │
│    is_admin  │       │    budget_cat.   │
│    profile_pic│      │    travel_type   │
│    created_at│       │    best_season   │
└──────┬───────┘       │    duration_days │
       │               │    cost_estimate │
       │               │    rating        │
       │               │    latitude      │
       │               │    longitude     │
       │               │    attractions   │
       │               │    highlights    │
       │               │    how_to_reach  │
       │               │    best_time     │
       │               │    created_at    │
       │               └────────┬─────────┘
       │                        │
       │    ┌───────────────┐   │
       ├───▶│   reviews     │◀──┤
       │    │───────────────│   │
       │    │ PK id         │   │
       │    │ FK user_id    │   │
       │    │ FK dest_id    │   │
       │    │    rating     │   │
       │    │    comment    │   │
       │    │    created_at │   │
       │    └───────────────┘   │
       │                        │
       │    ┌───────────────┐   │
       ├───▶│   wishlist    │◀──┤
       │    │───────────────│   │
       │    │ PK id         │   │
       │    │ FK user_id    │   │
       │    │ FK dest_id    │   │
       │    │    created_at │   │
       │    │ UNIQUE(u,d)   │   │
       │    └───────────────┘   │
       │                        │
       │    ┌───────────────┐   │
       ├───▶│  itineraries  │◀──┘
       │    │───────────────│
       │    │ PK id         │
       │    │ FK user_id    │
       │    │ FK dest_id    │
       │    │    title      │
       │    │    start_date │
       │    │    end_date   │
       │    │    notes      │
       │    │    status     │
       │    │    created_at │
       │    └───────────────┘
       │
       │    ┌───────────────┐
       ├───▶│  preferences  │
       │    │───────────────│
       │    │ PK id         │
       │    │ FK user_id(UQ)│
       │    │    pref_type  │
       │    │    pref_budget│
       │    │    pref_season│
       │    │    pref_dur.  │
       │    └───────────────┘
       │
       │    ┌──────────────────┐
       └───▶│ contact_messages │ (no FK)
            │──────────────────│
            │ PK id            │
            │    name          │
            │    email         │
            │    subject       │
            │    message       │
            │    is_read       │
            │    created_at    │
            └──────────────────┘
```

---

## 📋 Table Definitions

### Table 1: `users`

Stores registered user accounts and admin accounts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| `username` | TEXT | UNIQUE, NOT NULL | Login username |
| `email` | TEXT | UNIQUE, NOT NULL | User email address |
| `password_hash` | TEXT | NOT NULL | PBKDF2-SHA256 hashed password |
| `full_name` | TEXT | — | User's display name |
| `phone` | TEXT | — | Contact phone number |
| `is_admin` | INTEGER | DEFAULT 0 | Admin flag (0 = user, 1 = admin) |
| `profile_pic` | TEXT | DEFAULT 'default.png' | Profile picture filename |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration date |

---

### Table 2: `destinations`

Stores all travel destination information with 18 fields.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique destination identifier |
| `name` | TEXT | NOT NULL | Destination name (e.g., "Goa") |
| `country` | TEXT | NOT NULL | Country (default: "India") |
| `state` | TEXT | — | State/region |
| `description` | TEXT | NOT NULL | Detailed description |
| `image_url` | TEXT | DEFAULT 'default_dest.jpg' | Image filename |
| `budget_category` | TEXT | NOT NULL | `budget` / `moderate` / `luxury` |
| `travel_type` | TEXT | NOT NULL | `beach` / `adventure` / `historical` / `nature` / `cultural` / `wildlife` / `pilgrimage` / `hill_station` |
| `best_season` | TEXT | NOT NULL | `summer` / `winter` / `monsoon` / `spring` / `all` |
| `duration_days` | INTEGER | NOT NULL | Recommended trip duration |
| `cost_estimate` | INTEGER | NOT NULL | Estimated cost per person (₹) |
| `rating` | REAL | DEFAULT 0.0 | Average user rating (0-5) |
| `latitude` | REAL | — | GPS latitude coordinate |
| `longitude` | REAL | — | GPS longitude coordinate |
| `attractions` | TEXT | — | Comma-separated top attractions |
| `highlights` | TEXT | — | Comma-separated activity highlights |
| `how_to_reach` | TEXT | — | Transportation information |
| `best_time_detail` | TEXT | — | Detailed timing recommendation |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date added |

---

### Table 3: `reviews`

Stores user ratings and comments for destinations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique review identifier |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY → users(id) | Reviewer |
| `destination_id` | INTEGER | NOT NULL, FOREIGN KEY → destinations(id) | Reviewed destination |
| `rating` | INTEGER | NOT NULL | Star rating (1-5) |
| `comment` | TEXT | — | Review text |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Review date |

---

### Table 4: `wishlist`

Stores user's saved/favorite destinations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique entry identifier |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY → users(id) | User who saved |
| `destination_id` | INTEGER | NOT NULL, FOREIGN KEY → destinations(id) | Saved destination |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date saved |

> **Constraint:** `UNIQUE(user_id, destination_id)` — prevents duplicate saves.

---

### Table 5: `itineraries`

Stores user's travel plans and trip details.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique trip identifier |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY → users(id) | Trip owner |
| `title` | TEXT | NOT NULL | Trip title (e.g., "Weekend in Goa") |
| `destination_id` | INTEGER | FOREIGN KEY → destinations(id) | Linked destination (optional) |
| `start_date` | TEXT | — | Trip start date |
| `end_date` | TEXT | — | Trip end date |
| `notes` | TEXT | — | User notes and plans |
| `status` | TEXT | DEFAULT 'planned' | `planned` / `completed` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date created |

---

### Table 6: `preferences`

Stores user's travel preferences for personalized recommendations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique preference identifier |
| `user_id` | INTEGER | UNIQUE, NOT NULL, FK → users(id) | One preference set per user |
| `preferred_type` | TEXT | — | Preferred travel type |
| `preferred_budget` | TEXT | — | Preferred budget category |
| `preferred_season` | TEXT | — | Preferred travel season |
| `preferred_duration` | INTEGER | — | Preferred trip duration (days) |

---

### Table 7: `contact_messages`

Stores contact form submissions from website visitors.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique message identifier |
| `name` | TEXT | NOT NULL | Sender's name |
| `email` | TEXT | NOT NULL | Sender's email |
| `subject` | TEXT | — | Message subject |
| `message` | TEXT | NOT NULL | Message content |
| `is_read` | INTEGER | DEFAULT 0 | Read status (0 = unread, 1 = read) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date received |

---

## 📈 Table Relationships Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| users → reviews | One-to-Many | A user can write many reviews |
| users → wishlist | One-to-Many | A user can save many destinations |
| users → itineraries | One-to-Many | A user can plan many trips |
| users → preferences | One-to-One | Each user has one preference set |
| destinations → reviews | One-to-Many | A destination can have many reviews |
| destinations → wishlist | One-to-Many | A destination can be saved by many users |
| destinations → itineraries | One-to-Many | A destination can be in many itineraries |

---

## 🌱 Pre-loaded Data

### Destinations (20 records)

| # | Name | Type | Budget | Season |
|---|------|------|--------|--------|
| 1 | Goa | Beach | Moderate | Winter |
| 2 | Manali | Hill Station | Moderate | Summer |
| 3 | Jaipur | Historical | Moderate | Winter |
| 4 | Kerala Backwaters | Nature | Moderate | Winter |
| 5 | Ladakh | Adventure | Luxury | Summer |
| 6 | Varanasi | Pilgrimage | Budget | Winter |
| 7 | Andaman Islands | Beach | Luxury | Winter |
| 8 | Jim Corbett | Wildlife | Moderate | Winter |
| 9 | Hampi | Historical | Budget | Winter |
| 10 | Rishikesh | Adventure | Budget | All |
| 11 | Darjeeling | Hill Station | Moderate | Spring |
| 12 | Udaipur | Cultural | Moderate | Winter |
| 13 | Ooty | Hill Station | Budget | Summer |
| 14 | Rann of Kutch | Cultural | Moderate | Winter |
| 15 | Coorg | Nature | Moderate | Winter |
| 16 | Lakshadweep | Beach | Luxury | Winter |
| 17 | Mysore | Cultural | Budget | Winter |
| 18 | Shimla | Hill Station | Moderate | Summer |
| 19 | Kaziranga | Wildlife | Moderate | Winter |
| 20 | Amritsar | Pilgrimage | Budget | Winter |

### Admin Account (1 record)

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@travel.com | admin123 | Administrator |

---

## 🔧 Database Operations

| Operation | Function | File |
|-----------|----------|------|
| **Initialize** | `init_db()` — Creates all 7 tables | `database.py` |
| **Connect** | `get_db()` — Returns connection with Row factory | `database.py` |
| **Close** | `close_db(db)` — Safely closes connection | `database.py` |
| **Seed** | `seed_database()` — Inserts 20 destinations + admin | `seed_data.py` |
