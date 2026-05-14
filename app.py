"""
Travel Destination Recommendation System
Main Flask Application
"""
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, session, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_db, close_db, init_db
from recommendation_engine import (get_recommendations, get_similar_destinations,
                                    get_trending_destinations, get_budget_breakdown,
                                    track_user_activity, get_ai_recommendations,
                                    get_popular_with_similar_users, get_user_travel_profile,
                                    generate_day_plan, chatbot_response)
from seed_data import seed_database
from config import Config
import os
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database on first run
# Only initialize if not in a serverless cold start
if not os.environ.get('VERCEL') or not os.path.exists(Config.DATABASE):
    with app.app_context():
        init_db()
        seed_database()


# ==================== DECORATORS ====================

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


# ==================== CONTEXT PROCESSOR ====================

@app.context_processor
def inject_user():
    """Inject user info into all templates."""
    user = None
    if 'user_id' in session:
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        close_db(db)
    return dict(current_user=user)


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Home page with trending destinations and AI recommendations."""
    db = get_db()
    destinations = db.execute('SELECT * FROM destinations ORDER BY rating DESC').fetchall()
    trending = destinations[:6]
    total_destinations = len(destinations)

    # AI-based personalized recommendations for logged-in users
    ai_recommendations = []
    travel_profile = None
    if 'user_id' in session:
        ai_recommendations = get_ai_recommendations(db, session['user_id'], limit=6)
        travel_profile = get_user_travel_profile(db, session['user_id'])

    close_db(db)
    return render_template('index.html', trending=trending, total=total_destinations,
                           ai_recommendations=ai_recommendations, travel_profile=travel_profile)


@app.route('/explore')
def explore():
    """Browse all destinations with filters."""
    db = get_db()
    query = "SELECT * FROM destinations WHERE 1=1"
    params = []

    # Apply filters
    travel_type = request.args.get('type')
    budget = request.args.get('budget')
    season = request.args.get('season')
    search = request.args.get('search')
    sort_by = request.args.get('sort', 'rating')

    if travel_type and travel_type != 'all':
        query += " AND travel_type = ?"
        params.append(travel_type)
    if budget and budget != 'all':
        query += " AND budget_category = ?"
        params.append(budget)
    if season and season != 'all':
        query += " AND (best_season = ? OR best_season = 'all')"
        params.append(season)
    if search:
        query += " AND (name LIKE ? OR state LIKE ? OR description LIKE ?)"
        params.extend([f'%{search}%'] * 3)

    # Sorting
    sort_map = {'rating': 'rating DESC', 'cost_low': 'cost_estimate ASC',
                'cost_high': 'cost_estimate DESC', 'name': 'name ASC', 'duration': 'duration_days ASC'}
    query += f" ORDER BY {sort_map.get(sort_by, 'rating DESC')}"

    destinations = db.execute(query, params).fetchall()
    close_db(db)
    return render_template('explore.html', destinations=destinations,
                           filters={'type': travel_type, 'budget': budget, 'season': season,
                                    'search': search, 'sort': sort_by})


@app.route('/destination/<int:dest_id>')
def destination_detail(dest_id):
    """View destination details."""
    db = get_db()
    dest = db.execute('SELECT * FROM destinations WHERE id = ?', (dest_id,)).fetchone()
    if not dest:
        flash('Destination not found.', 'danger')
        close_db(db)
        return redirect(url_for('explore'))

    # Track user view for AI recommendations
    if 'user_id' in session:
        track_user_activity(db, session['user_id'], dest_id, 'view')

    reviews = db.execute('''
        SELECT r.*, u.username, u.full_name FROM reviews r 
        JOIN users u ON r.user_id = u.id 
        WHERE r.destination_id = ? ORDER BY r.created_at DESC
    ''', (dest_id,)).fetchall()

    all_dests = db.execute('SELECT * FROM destinations').fetchall()
    similar = get_similar_destinations(dest, all_dests)
    budget = get_budget_breakdown(dest['cost_estimate'], dest['duration_days'])
    day_plan = generate_day_plan(dest)

    # AI: "Users who viewed this also viewed..."
    also_viewed = []
    if 'user_id' in session:
        also_viewed = get_popular_with_similar_users(db, session['user_id'], dest_id, limit=4)

    in_wishlist = False
    if 'user_id' in session:
        wl = db.execute('SELECT id FROM wishlist WHERE user_id = ? AND destination_id = ?',
                        (session['user_id'], dest_id)).fetchone()
        in_wishlist = wl is not None

    close_db(db)
    return render_template('destination.html', dest=dest, reviews=reviews,
                           similar=similar, budget=budget, in_wishlist=in_wishlist,
                           also_viewed=also_viewed, day_plan=day_plan)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Recommendation page."""
    recommendations = None
    if request.method == 'POST':
        prefs = {
            'travel_type': request.form.get('travel_type'),
            'budget': request.form.get('budget'),
            'season': request.form.get('season'),
            'duration': request.form.get('duration'),
            'max_cost': request.form.get('max_cost')
        }
        db = get_db()
        all_dests = db.execute('SELECT * FROM destinations').fetchall()
        close_db(db)
        recommendations = get_recommendations(all_dests, prefs)

        # Save preferences if logged in
        if 'user_id' in session:
            db = get_db()
            db.execute('DELETE FROM preferences WHERE user_id = ?', (session['user_id'],))
            db.execute('''INSERT INTO preferences (user_id, preferred_type, preferred_budget, 
                         preferred_season, preferred_duration) VALUES (?, ?, ?, ?, ?)''',
                      (session['user_id'], prefs['travel_type'], prefs['budget'],
                       prefs['season'], prefs.get('duration', 0)))
            db.commit()
            close_db(db)

    return render_template('recommend.html', recommendations=recommendations)


# ==================== AUTH ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        close_db(db)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash(f'Welcome back, {user["username"]}!', 'success')
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')

        db = get_db()
        existing = db.execute('SELECT id FROM users WHERE username = ? OR email = ?',
                             (username, email)).fetchone()
        if existing:
            flash('Username or email already exists.', 'danger')
            close_db(db)
            return render_template('register.html')

        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        db.execute('INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)',
                  (username, email, password_hash, full_name))
        db.commit()
        close_db(db)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


# ==================== USER ROUTES ====================

@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    reviews = db.execute('''
        SELECT r.*, d.name as dest_name FROM reviews r 
        JOIN destinations d ON r.destination_id = d.id 
        WHERE r.user_id = ? ORDER BY r.created_at DESC
    ''', (session['user_id'],)).fetchall()
    wishlist_count = db.execute('SELECT COUNT(*) FROM wishlist WHERE user_id = ?',
                                (session['user_id'],)).fetchone()[0]
    prefs = db.execute('SELECT * FROM preferences WHERE user_id = ?',
                       (session['user_id'],)).fetchone()
    close_db(db)
    return render_template('profile.html', user=user, reviews=reviews,
                           wishlist_count=wishlist_count, prefs=prefs)


@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile."""
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    db = get_db()
    db.execute('UPDATE users SET full_name = ?, email = ?, phone = ? WHERE id = ?',
              (full_name, email, phone, session['user_id']))
    db.commit()
    close_db(db)
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/wishlist')
@login_required
def wishlist():
    """View user's wishlist."""
    db = get_db()
    items = db.execute('''
        SELECT d.*, w.created_at as added_at FROM wishlist w 
        JOIN destinations d ON w.destination_id = d.id 
        WHERE w.user_id = ? ORDER BY w.created_at DESC
    ''', (session['user_id'],)).fetchall()
    close_db(db)
    return render_template('wishlist.html', items=items)


@app.route('/wishlist/toggle/<int:dest_id>', methods=['POST'])
@login_required
def toggle_wishlist(dest_id):
    """Add/remove destination from wishlist."""
    db = get_db()
    existing = db.execute('SELECT id FROM wishlist WHERE user_id = ? AND destination_id = ?',
                          (session['user_id'], dest_id)).fetchone()
    if existing:
        db.execute('DELETE FROM wishlist WHERE id = ?', (existing['id'],))
        msg = 'Removed from wishlist.'
    else:
        db.execute('INSERT INTO wishlist (user_id, destination_id) VALUES (?, ?)',
                  (session['user_id'], dest_id))
        msg = 'Added to wishlist!'
    db.commit()
    close_db(db)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'message': msg, 'in_wishlist': not bool(existing)})
    flash(msg, 'success')
    return redirect(request.referrer or url_for('explore'))


@app.route('/review/<int:dest_id>', methods=['POST'])
@login_required
def add_review(dest_id):
    """Add a review for a destination."""
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    db = get_db()

    # Check if already reviewed
    existing = db.execute('SELECT id FROM reviews WHERE user_id = ? AND destination_id = ?',
                          (session['user_id'], dest_id)).fetchone()
    if existing:
        db.execute('UPDATE reviews SET rating = ?, comment = ? WHERE id = ?',
                  (rating, comment, existing['id']))
    else:
        db.execute('INSERT INTO reviews (user_id, destination_id, rating, comment) VALUES (?, ?, ?, ?)',
                  (session['user_id'], dest_id, rating, comment))

    # Update destination average rating
    avg = db.execute('SELECT AVG(rating) FROM reviews WHERE destination_id = ?', (dest_id,)).fetchone()[0]
    db.execute('UPDATE destinations SET rating = ? WHERE id = ?', (round(avg, 1), dest_id))

    db.commit()
    close_db(db)
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('destination_detail', dest_id=dest_id))


@app.route('/itinerary')
@login_required
def itinerary():
    """View user's travel itineraries."""
    db = get_db()
    trips = db.execute('''
        SELECT i.*, d.name as dest_name, d.image_url, d.state 
        FROM itineraries i LEFT JOIN destinations d ON i.destination_id = d.id 
        WHERE i.user_id = ? ORDER BY i.start_date DESC
    ''', (session['user_id'],)).fetchall()
    destinations = db.execute('SELECT id, name, state FROM destinations ORDER BY name').fetchall()
    close_db(db)
    return render_template('itinerary.html', trips=trips, destinations=destinations)


@app.route('/itinerary/add', methods=['POST'])
@login_required
def add_itinerary():
    """Add a new itinerary."""
    db = get_db()
    db.execute('''INSERT INTO itineraries (user_id, title, destination_id, start_date, end_date, notes) 
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (session['user_id'], request.form.get('title'),
               request.form.get('destination_id') or None,
               request.form.get('start_date'), request.form.get('end_date'),
               request.form.get('notes')))
    db.commit()
    close_db(db)
    flash('Trip added to your itinerary!', 'success')
    return redirect(url_for('itinerary'))


@app.route('/itinerary/delete/<int:trip_id>', methods=['POST'])
@login_required
def delete_itinerary(trip_id):
    """Delete an itinerary."""
    db = get_db()
    db.execute('DELETE FROM itineraries WHERE id = ? AND user_id = ?', (trip_id, session['user_id']))
    db.commit()
    close_db(db)
    flash('Trip removed from itinerary.', 'success')
    return redirect(url_for('itinerary'))


@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission."""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not name or not email or not message:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('index') + '#contact')
        
        db = get_db()
        db.execute('INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                  (name, email, subject, message))
        db.commit()
        close_db(db)
        flash('✅ Message sent successfully! We will get back to you soon.', 'success')
    except Exception as e:
        flash('❌ An error occurred. Please try again.', 'danger')
        print(f"Contact form error: {e}")
    
    return redirect(url_for('index') + '#contact')


# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with analytics."""
    db = get_db()
    stats = {
        'total_destinations': db.execute('SELECT COUNT(*) FROM destinations').fetchone()[0],
        'total_users': db.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0').fetchone()[0],
        'total_reviews': db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0],
        'total_wishlists': db.execute('SELECT COUNT(*) FROM wishlist').fetchone()[0],
        'messages': db.execute('SELECT COUNT(*) FROM contact_messages WHERE is_read = 0').fetchone()[0],
    }
    recent_reviews = db.execute('''
        SELECT r.*, u.username, d.name as dest_name FROM reviews r 
        JOIN users u ON r.user_id = u.id JOIN destinations d ON r.destination_id = d.id 
        ORDER BY r.created_at DESC LIMIT 5
    ''').fetchall()
    recent_users = db.execute('SELECT * FROM users WHERE is_admin = 0 ORDER BY created_at DESC LIMIT 5').fetchall()

    # Type distribution
    type_dist = db.execute('''
        SELECT travel_type, COUNT(*) as count FROM destinations GROUP BY travel_type
    ''').fetchall()

    close_db(db)
    return render_template('admin/dashboard.html', stats=stats, recent_reviews=recent_reviews,
                           recent_users=recent_users, type_dist=type_dist)


@app.route('/admin/destinations')
@admin_required
def admin_destinations():
    """Admin manage destinations."""
    db = get_db()
    destinations = db.execute('SELECT * FROM destinations ORDER BY created_at DESC').fetchall()
    close_db(db)
    return render_template('admin/destinations.html', destinations=destinations)


@app.route('/admin/destinations/add', methods=['GET', 'POST'])
@admin_required
def admin_add_destination():
    """Add a new destination."""
    if request.method == 'POST':
        db = get_db()
        db.execute('''INSERT INTO destinations (name, country, state, description, image_url,
                     budget_category, travel_type, best_season, duration_days, cost_estimate,
                     rating, attractions, highlights, how_to_reach, best_time_detail)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (request.form.get('name'), request.form.get('country', 'India'),
                   request.form.get('state'), request.form.get('description'),
                   request.form.get('image_url', 'default_dest.jpg'),
                   request.form.get('budget_category'), request.form.get('travel_type'),
                   request.form.get('best_season'), int(request.form.get('duration_days', 3)),
                   int(request.form.get('cost_estimate', 10000)),
                   float(request.form.get('rating', 4.0)),
                   request.form.get('attractions'), request.form.get('highlights'),
                   request.form.get('how_to_reach'), request.form.get('best_time_detail')))
        db.commit()
        close_db(db)
        flash('Destination added successfully!', 'success')
        return redirect(url_for('admin_destinations'))
    return render_template('admin/add_destination.html')


@app.route('/admin/destinations/edit/<int:dest_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_destination(dest_id):
    """Edit an existing destination."""
    db = get_db()
    if request.method == 'POST':
        db.execute('''UPDATE destinations SET name=?, country=?, state=?, description=?,
                     image_url=?, budget_category=?, travel_type=?, best_season=?,
                     duration_days=?, cost_estimate=?, rating=?, attractions=?,
                     highlights=?, how_to_reach=?, best_time_detail=? WHERE id=?''',
                  (request.form.get('name'), request.form.get('country', 'India'),
                   request.form.get('state'), request.form.get('description'),
                   request.form.get('image_url'), request.form.get('budget_category'),
                   request.form.get('travel_type'), request.form.get('best_season'),
                   int(request.form.get('duration_days', 3)),
                   int(request.form.get('cost_estimate', 10000)),
                   float(request.form.get('rating', 4.0)),
                   request.form.get('attractions'), request.form.get('highlights'),
                   request.form.get('how_to_reach'), request.form.get('best_time_detail'), dest_id))
        db.commit()
        close_db(db)
        flash('Destination updated successfully!', 'success')
        return redirect(url_for('admin_destinations'))

    dest = db.execute('SELECT * FROM destinations WHERE id = ?', (dest_id,)).fetchone()
    close_db(db)
    return render_template('admin/add_destination.html', dest=dest, edit=True)


@app.route('/admin/destinations/delete/<int:dest_id>', methods=['POST'])
@admin_required
def admin_delete_destination(dest_id):
    """Delete a destination."""
    db = get_db()
    db.execute('DELETE FROM reviews WHERE destination_id = ?', (dest_id,))
    db.execute('DELETE FROM wishlist WHERE destination_id = ?', (dest_id,))
    db.execute('DELETE FROM destinations WHERE id = ?', (dest_id,))
    db.commit()
    close_db(db)
    flash('Destination deleted.', 'success')
    return redirect(url_for('admin_destinations'))


@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin manage users."""
    db = get_db()
    users = db.execute('''
        SELECT u.*, COUNT(DISTINCT r.id) as review_count, COUNT(DISTINCT w.id) as wishlist_count
        FROM users u LEFT JOIN reviews r ON u.id = r.user_id 
        LEFT JOIN wishlist w ON u.id = w.user_id
        WHERE u.is_admin = 0 GROUP BY u.id ORDER BY u.created_at DESC
    ''').fetchall()
    close_db(db)
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete a user."""
    db = get_db()
    db.execute('DELETE FROM reviews WHERE user_id = ?', (user_id,))
    db.execute('DELETE FROM wishlist WHERE user_id = ?', (user_id,))
    db.execute('DELETE FROM itineraries WHERE user_id = ?', (user_id,))
    db.execute('DELETE FROM preferences WHERE user_id = ?', (user_id,))
    db.execute('DELETE FROM users WHERE id = ? AND is_admin = 0', (user_id,))
    db.commit()
    close_db(db)
    flash('User deleted.', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/messages')
@admin_required
def admin_messages():
    """View contact messages."""
    db = get_db()
    msgs = db.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
    db.execute('UPDATE contact_messages SET is_read = 1')
    db.commit()
    close_db(db)
    return render_template('admin/messages.html', messages=msgs)


# ==================== USER DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Personalized user dashboard."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    # Saved destinations
    saved = db.execute('''
        SELECT d.*, w.created_at as saved_at FROM wishlist w
        JOIN destinations d ON w.destination_id = d.id
        WHERE w.user_id = ? ORDER BY w.created_at DESC LIMIT 6
    ''', (session['user_id'],)).fetchall()

    # Recent searches
    searches = db.execute('''
        SELECT * FROM search_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 10
    ''', (session['user_id'],)).fetchall()

    # User reviews
    reviews = db.execute('''
        SELECT r.*, d.name as dest_name, d.image_url FROM reviews r
        JOIN destinations d ON r.destination_id = d.id
        WHERE r.user_id = ? ORDER BY r.created_at DESC LIMIT 5
    ''', (session['user_id'],)).fetchall()

    # AI Recommendations
    ai_recs = get_ai_recommendations(db, session['user_id'], limit=4)
    travel_profile = get_user_travel_profile(db, session['user_id'])

    # Stats
    stats = {
        'wishlist': db.execute('SELECT COUNT(*) FROM wishlist WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'reviews': db.execute('SELECT COUNT(*) FROM reviews WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'trips': db.execute('SELECT COUNT(*) FROM itineraries WHERE user_id = ?', (session['user_id'],)).fetchone()[0],
        'views': db.execute('SELECT COUNT(*) FROM user_activity WHERE user_id = ? AND action_type = ?', (session['user_id'], 'view')).fetchone()[0],
    }

    # Notifications
    notifs = db.execute('''
        SELECT * FROM notifications WHERE (user_id = ? OR user_id IS NULL)
        ORDER BY created_at DESC LIMIT 5
    ''', (session['user_id'],)).fetchall()

    close_db(db)
    return render_template('dashboard.html', user=user, saved=saved, searches=searches,
                           reviews=reviews, ai_recs=ai_recs, travel_profile=travel_profile,
                           stats=stats, notifs=notifs)


# ==================== API ROUTES ====================

@app.route('/api/destinations')
def api_destinations():
    """API endpoint for destinations."""
    db = get_db()
    dests = db.execute('SELECT id, name, state, rating, cost_estimate, travel_type FROM destinations').fetchall()
    close_db(db)
    return jsonify([dict(d) for d in dests])


@app.route('/api/search')
def api_search():
    """API search endpoint."""
    q = request.args.get('q', '')
    db = get_db()
    # Save search history
    if 'user_id' in session and q:
        db.execute('INSERT INTO search_history (user_id, query) VALUES (?, ?)',
                   (session['user_id'], q))
        db.commit()
    results = db.execute('''
        SELECT id, name, state, image_url, travel_type, cost_estimate 
        FROM destinations WHERE name LIKE ? OR state LIKE ? LIMIT 5
    ''', (f'%{q}%', f'%{q}%')).fetchall()
    close_db(db)
    return jsonify([dict(r) for r in results])


@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    """Chatbot API endpoint."""
    data = request.get_json()
    query = data.get('message', '')
    db = get_db()
    destinations = db.execute('SELECT * FROM destinations').fetchall()
    close_db(db)
    response = chatbot_response(query, destinations)
    # Format destinations for JSON
    dests_json = []
    for d in response['destinations']:
        dests_json.append({
            'id': d['id'], 'name': d['name'], 'state': d.get('state', ''),
            'rating': d.get('rating', 0), 'cost_estimate': d.get('cost_estimate', 0),
            'travel_type': d.get('travel_type', ''), 'image_url': d.get('image_url', ''),
            'budget_category': d.get('budget_category', '')
        })
    return jsonify({'message': response['message'], 'destinations': dests_json})


@app.route('/api/notifications')
@login_required
def api_notifications():
    """Get user notifications."""
    db = get_db()
    notifs = db.execute('''
        SELECT * FROM notifications WHERE (user_id = ? OR user_id IS NULL)
        AND is_read = 0 ORDER BY created_at DESC LIMIT 10
    ''', (session['user_id'],)).fetchall()
    close_db(db)
    return jsonify([dict(n) for n in notifs])


@app.route('/api/notifications/read', methods=['POST'])
@login_required
def mark_notifications_read():
    """Mark all notifications as read."""
    db = get_db()
    db.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ? OR user_id IS NULL',
               (session['user_id'],))
    db.commit()
    close_db(db)
    return jsonify({'success': True})


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', error_404=True), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('base.html', error_500=True), 500


if __name__ == '__main__':
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
