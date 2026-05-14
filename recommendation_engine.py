"""
Recommendation Engine for Travel Destination Recommendation System.
Uses a weighted scoring algorithm to match user preferences with destinations.
"""


def get_recommendations(destinations, preferences):
    """Generate travel recommendations based on user preferences."""
    scored = []
    for dest in destinations:
        score = calculate_score(dest, preferences)
        if score > 0:
            d = dict(dest)
            d['match_score'] = score
            d['match_percentage'] = min(int(score * 20), 100)
            scored.append(d)
    scored.sort(key=lambda x: x['match_score'], reverse=True)
    return scored


def calculate_score(destination, preferences):
    """Calculate relevance score using weighted criteria."""
    score = 0.0
    w = {'type': 3.0, 'budget': 2.5, 'season': 2.0, 'duration': 1.5, 'rating': 1.0}
    related = {
        'adventure': ['nature', 'wildlife', 'hill_station'],
        'beach': ['nature'], 'historical': ['cultural', 'pilgrimage'],
        'nature': ['adventure', 'wildlife', 'hill_station', 'beach'],
        'cultural': ['historical', 'pilgrimage'],
        'wildlife': ['nature', 'adventure'],
        'pilgrimage': ['cultural', 'historical'],
        'hill_station': ['nature', 'adventure']
    }

    if preferences.get('travel_type'):
        pt = preferences['travel_type'].lower()
        dt = destination['travel_type'].lower()
        if pt == dt:
            score += w['type']
        elif pt in dt or dt in pt:
            score += w['type'] * 0.5
        elif pt in related and dt in related.get(pt, []):
            score += w['type'] * 0.3

    if preferences.get('budget'):
        pb = preferences['budget'].lower()
        db = destination['budget_category'].lower()
        if pb == db:
            score += w['budget']
        elif pb == 'moderate' and db in ['budget', 'moderate']:
            score += w['budget'] * 0.6
        elif pb == 'luxury' and db == 'moderate':
            score += w['budget'] * 0.4

    if preferences.get('max_cost'):
        try:
            if destination['cost_estimate'] <= int(preferences['max_cost']):
                score += w['budget'] * 0.5
            else:
                score -= w['budget'] * 0.5
        except (ValueError, TypeError):
            pass

    if preferences.get('season'):
        ps = preferences['season'].lower()
        ds = destination['best_season'].lower()
        if ps == ds or ps == 'all' or ds == 'all':
            score += w['season']
        elif ps in ds:
            score += w['season'] * 0.7

    if preferences.get('duration'):
        try:
            diff = abs(int(preferences['duration']) - destination['duration_days'])
            if diff == 0: score += w['duration']
            elif diff <= 2: score += w['duration'] * 0.7
            elif diff <= 4: score += w['duration'] * 0.4
            else: score += w['duration'] * 0.1
        except (ValueError, TypeError):
            pass

    if destination['rating']:
        score += (destination['rating'] / 5.0) * w['rating']

    return score


def get_similar_destinations(destination, all_destinations, limit=4):
    """Find similar destinations."""
    prefs = {
        'travel_type': destination['travel_type'],
        'budget': destination['budget_category'],
        'season': destination['best_season'],
    }
    similar = [d for d in get_recommendations(all_destinations, prefs) if d['id'] != destination['id']]
    return similar[:limit]


def get_trending_destinations(destinations, limit=6):
    """Get top-rated destinations."""
    return sorted(destinations, key=lambda x: x['rating'] or 0, reverse=True)[:limit]


def get_budget_breakdown(cost_estimate, duration):
    """Generate estimated budget breakdown."""
    if not cost_estimate or not duration:
        return None
    return {
        'total': cost_estimate,
        'accommodation': int(cost_estimate * 0.35),
        'food': int(cost_estimate * 0.20),
        'transport': int(cost_estimate * 0.25),
        'activities': int(cost_estimate * 0.12),
        'miscellaneous': int(cost_estimate * 0.08),
        'daily_average': int(cost_estimate / max(duration, 1)),
        'duration': duration
    }


# ==================== AI-BASED COLLABORATIVE FILTERING ====================

def track_user_activity(db, user_id, destination_id, action_type='view'):
    """Track user activity for AI recommendations.
    action_type: 'view', 'wishlist', 'review', 'itinerary'
    """
    db.execute('''
        INSERT INTO user_activity (user_id, destination_id, action_type) 
        VALUES (?, ?, ?)
    ''', (user_id, destination_id, action_type))
    db.commit()


def get_user_interaction_scores(db):
    """Build user-destination interaction matrix with weighted scores.
    Weights: view=1, wishlist=3, review=4, itinerary=5
    """
    action_weights = {'view': 1, 'wishlist': 3, 'review': 4, 'itinerary': 5}
    interactions = {}

    # Get all user activities
    activities = db.execute('''
        SELECT user_id, destination_id, action_type, COUNT(*) as cnt
        FROM user_activity 
        GROUP BY user_id, destination_id, action_type
    ''').fetchall()

    for act in activities:
        uid = act['user_id']
        did = act['destination_id']
        weight = action_weights.get(act['action_type'], 1)
        if uid not in interactions:
            interactions[uid] = {}
        interactions[uid][did] = interactions[uid].get(did, 0) + (weight * act['cnt'])

    # Also add wishlist data
    wishlists = db.execute('SELECT user_id, destination_id FROM wishlist').fetchall()
    for wl in wishlists:
        uid, did = wl['user_id'], wl['destination_id']
        if uid not in interactions:
            interactions[uid] = {}
        interactions[uid][did] = interactions[uid].get(did, 0) + action_weights['wishlist']

    # Also add review data
    reviews = db.execute('SELECT user_id, destination_id, rating FROM reviews').fetchall()
    for rv in reviews:
        uid, did = rv['user_id'], rv['destination_id']
        if uid not in interactions:
            interactions[uid] = {}
        interactions[uid][did] = interactions[uid].get(did, 0) + (rv['rating'] * action_weights['review'])

    return interactions


def calculate_user_similarity(user1_scores, user2_scores):
    """Calculate cosine similarity between two users' interaction vectors."""
    common_dests = set(user1_scores.keys()) & set(user2_scores.keys())
    if not common_dests:
        return 0.0

    dot_product = sum(user1_scores[d] * user2_scores[d] for d in common_dests)
    magnitude1 = sum(v ** 2 for v in user1_scores.values()) ** 0.5
    magnitude2 = sum(v ** 2 for v in user2_scores.values()) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def get_ai_recommendations(db, user_id, limit=6):
    """AI-based collaborative filtering recommendations.
    
    Algorithm:
    1. Build user-destination interaction matrix
    2. Calculate cosine similarity with all other users
    3. Find top similar users
    4. Recommend destinations that similar users liked but current user hasn't seen
    5. Rank by weighted score from similar users
    
    Returns: list of (destination, score, reason) tuples
    """
    interactions = get_user_interaction_scores(db)

    if user_id not in interactions or len(interactions) < 2:
        return []

    current_user_scores = interactions[user_id]
    current_user_dests = set(current_user_scores.keys())

    # Calculate similarity with all other users
    similar_users = []
    for other_id, other_scores in interactions.items():
        if other_id == user_id:
            continue
        sim = calculate_user_similarity(current_user_scores, other_scores)
        if sim > 0:
            similar_users.append((other_id, sim, other_scores))

    if not similar_users:
        return []

    # Sort by similarity (most similar first)
    similar_users.sort(key=lambda x: x[1], reverse=True)
    top_similar = similar_users[:10]  # Top 10 similar users

    # Collect recommendation scores from similar users
    dest_scores = {}
    dest_users = {}  # Track which similar users liked each destination
    for other_id, similarity, other_scores in top_similar:
        for dest_id, score in other_scores.items():
            if dest_id not in current_user_dests:
                weighted = score * similarity
                dest_scores[dest_id] = dest_scores.get(dest_id, 0) + weighted
                if dest_id not in dest_users:
                    dest_users[dest_id] = 0
                dest_users[dest_id] += 1

    if not dest_scores:
        return []

    # Get destination details and build results
    sorted_dests = sorted(dest_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
    results = []
    for dest_id, score in sorted_dests:
        dest = db.execute('SELECT * FROM destinations WHERE id = ?', (dest_id,)).fetchone()
        if dest:
            d = dict(dest)
            d['ai_score'] = round(score, 2)
            d['similar_user_count'] = dest_users.get(dest_id, 0)
            d['match_percentage'] = min(int((score / max(s for _, s in sorted_dests)) * 100), 100) if sorted_dests else 0
            results.append(d)

    return results


def get_popular_with_similar_users(db, user_id, destination_id, limit=4):
    """'Users who viewed X also viewed Y' — item-based collaborative filtering.
    
    Finds destinations commonly viewed by users who also viewed the given destination.
    """
    # Find users who viewed/interacted with this destination
    viewers = db.execute('''
        SELECT DISTINCT user_id FROM user_activity 
        WHERE destination_id = ? AND user_id != ?
    ''', (destination_id, user_id)).fetchall()

    viewer_ids = [v['user_id'] for v in viewers]

    # Also include users who wishlisted this destination
    wishlisted = db.execute('''
        SELECT DISTINCT user_id FROM wishlist 
        WHERE destination_id = ? AND user_id != ?
    ''', (destination_id, user_id)).fetchall()

    viewer_ids.extend([w['user_id'] for w in wishlisted])
    viewer_ids = list(set(viewer_ids))

    if not viewer_ids:
        return []

    # Find other destinations these users interacted with
    placeholders = ','.join('?' * len(viewer_ids))
    related = db.execute(f'''
        SELECT d.*, COUNT(DISTINCT ua.user_id) as viewer_count
        FROM destinations d
        JOIN user_activity ua ON d.id = ua.destination_id
        WHERE ua.user_id IN ({placeholders})
        AND d.id != ?
        GROUP BY d.id
        ORDER BY viewer_count DESC
        LIMIT ?
    ''', (*viewer_ids, destination_id, limit)).fetchall()

    results = []
    for dest in related:
        d = dict(dest)
        d['recommended_by'] = d.pop('viewer_count', 0)
        results.append(d)

    return results


def get_user_travel_profile(db, user_id):
    """Analyze user behavior to build a travel profile.
    Returns: dict with preferred types, budgets, seasons based on activity.
    """
    # Analyze viewed/interacted destinations
    profile_data = db.execute('''
        SELECT d.travel_type, d.budget_category, d.best_season, 
               COUNT(*) as interactions
        FROM user_activity ua
        JOIN destinations d ON ua.destination_id = d.id
        WHERE ua.user_id = ?
        GROUP BY d.travel_type, d.budget_category, d.best_season
        ORDER BY interactions DESC
    ''', (user_id,)).fetchall()

    if not profile_data:
        return None

    # Aggregate preferences
    types = {}
    budgets = {}
    seasons = {}
    for row in profile_data:
        count = row['interactions']
        types[row['travel_type']] = types.get(row['travel_type'], 0) + count
        budgets[row['budget_category']] = budgets.get(row['budget_category'], 0) + count
        seasons[row['best_season']] = seasons.get(row['best_season'], 0) + count

    return {
        'top_type': max(types, key=types.get) if types else None,
        'top_budget': max(budgets, key=budgets.get) if budgets else None,
        'top_season': max(seasons, key=seasons.get) if seasons else None,
        'type_breakdown': types,
        'budget_breakdown': budgets,
        'season_breakdown': seasons,
        'total_interactions': sum(types.values())
    }


# ==================== AUTO ITINERARY GENERATOR ====================

def generate_day_plan(destination):
    """Auto-generate a day-by-day travel itinerary from destination data."""
    duration = destination['duration_days'] or 3
    try:
        attractions_raw = destination['attractions'] or ''
    except (KeyError, IndexError):
        attractions_raw = ''
    try:
        highlights_raw = destination['highlights'] or ''
    except (KeyError, IndexError):
        highlights_raw = ''
    name = destination['name']
    try:
        travel_type = destination['travel_type'] or ''
    except (KeyError, IndexError):
        travel_type = ''

    attractions = [a.strip() for a in attractions_raw.split(',') if a.strip()]
    highlights = [h.strip() for h in highlights_raw.split(',') if h.strip()]
    all_items = attractions + highlights

    # Time slots for activities
    time_slots = [
        ('7:00 AM', 'morning'),
        ('10:00 AM', 'late_morning'),
        ('1:00 PM', 'afternoon'),
        ('4:00 PM', 'evening'),
        ('7:00 PM', 'night')
    ]

    # Generic activities by type
    generic = {
        'beach': ['Beach walk & sunrise', 'Water sports', 'Seafood lunch', 'Sunset at beach', 'Night market exploration'],
        'adventure': ['Morning trek', 'Adventure activity', 'Local lunch', 'Sightseeing', 'Campfire & stargazing'],
        'historical': ['Fort/Palace visit', 'Museum exploration', 'Local cuisine', 'Temple/Monument tour', 'Cultural show'],
        'nature': ['Nature trail/Hike', 'Scenic viewpoint', 'Picnic lunch', 'Wildlife/Bird watching', 'Sunset photography'],
        'cultural': ['Temple/Heritage walk', 'Art gallery visit', 'Traditional meal', 'Local market', 'Cultural performance'],
        'wildlife': ['Early morning safari', 'Bird watching', 'Nature walk', 'Afternoon safari', 'Documentary at camp'],
        'pilgrimage': ['Temple darshan', 'Pooja/Aarti', 'Prasad lunch', 'Heritage walk', 'Evening aarti'],
        'hill_station': ['Sunrise viewpoint', 'Tea garden visit', 'Local cuisine', 'Toy train / Lake visit', 'Bonfire & hot cocoa'],
    }

    tips_pool = [
        'Start early to avoid crowds at popular spots',
        'Carry water and sunscreen for outdoor activities',
        'Try the local street food — it\'s a must!',
        'Book your activities in advance during peak season',
        'Don\'t miss the sunset — find a good viewpoint',
        'Interact with locals for hidden gems and tips',
        'Keep some cash handy for local vendors',
        'Wear comfortable shoes for walking tours',
        f'Check weather forecast before heading out in {name}',
        'Take a break and enjoy the scenery at a local café',
    ]

    type_activities = generic.get(travel_type, generic['nature'])
    days = []

    for d in range(1, duration + 1):
        day_activities = []
        for i, (time, period) in enumerate(time_slots):
            if d == 1 and i == 0:
                desc = f'Arrive in {name} and check-in to hotel'
            elif d == duration and i == len(time_slots) - 1:
                desc = f'Pack up and depart from {name}'
            else:
                idx = ((d - 1) * len(time_slots) + i) % len(all_items) if all_items else 0
                if all_items:
                    desc = f'Visit {all_items[idx]}' if i < 3 else f'Explore {all_items[idx]}'
                else:
                    desc = type_activities[i % len(type_activities)]

            day_activities.append({'time': time, 'description': desc})

        title = f'Day {d}'
        if d == 1:
            title = f'Day {d} — Arrival & Exploration'
        elif d == duration:
            title = f'Day {d} — Final Day & Departure'
        else:
            title = f'Day {d} — {name} Adventure'

        tip = tips_pool[(d - 1) % len(tips_pool)]
        days.append({'day': d, 'title': title, 'activities': day_activities, 'tip': tip})

    return days


# ==================== CHATBOT ENGINE ====================

def chatbot_response(query, destinations):
    """Simple rule-based chatbot for travel suggestions."""
    query_lower = query.lower().strip()

    # Budget queries
    budget_keywords = {'cheap': 'budget', 'budget': 'budget', 'affordable': 'budget',
                       'moderate': 'moderate', 'mid-range': 'moderate', 'mid range': 'moderate',
                       'luxury': 'luxury', 'expensive': 'luxury', 'premium': 'luxury'}

    # Extract budget amount if mentioned
    import re
    amount_match = re.search(r'(?:under|below|within|less than|max|upto|up to)\s*(?:₹|rs\.?|inr)?\s*([\d,]+)', query_lower)
    max_budget = None
    if amount_match:
        max_budget = int(amount_match.group(1).replace(',', ''))

    # Type detection
    type_keywords = {
        'beach': 'beach', 'sea': 'beach', 'ocean': 'beach',
        'adventure': 'adventure', 'trek': 'adventure', 'trekking': 'adventure',
        'historical': 'historical', 'history': 'historical', 'heritage': 'historical', 'fort': 'historical',
        'nature': 'nature', 'forest': 'nature', 'green': 'nature',
        'cultural': 'cultural', 'culture': 'cultural', 'art': 'cultural',
        'wildlife': 'wildlife', 'safari': 'wildlife', 'animals': 'wildlife', 'tiger': 'wildlife',
        'pilgrimage': 'pilgrimage', 'temple': 'pilgrimage', 'spiritual': 'pilgrimage', 'religious': 'pilgrimage',
        'hill': 'hill_station', 'hill station': 'hill_station', 'mountains': 'hill_station', 'hills': 'hill_station',
    }

    # Season detection
    season_keywords = {'summer': 'summer', 'winter': 'winter', 'monsoon': 'monsoon', 'rain': 'monsoon', 'spring': 'spring'}

    # Determine filters
    detected_type = None
    detected_budget = None
    detected_season = None

    for kw, val in type_keywords.items():
        if kw in query_lower:
            detected_type = val
            break

    for kw, val in budget_keywords.items():
        if kw in query_lower:
            detected_budget = val
            break

    for kw, val in season_keywords.items():
        if kw in query_lower:
            detected_season = val
            break

    # Filter destinations
    results = []
    for dest in destinations:
        d = dict(dest)
        match = True
        if detected_type and d['travel_type'] != detected_type:
            match = False
        if detected_budget and d['budget_category'] != detected_budget:
            match = False
        if detected_season and d['best_season'] != detected_season and d['best_season'] != 'all':
            match = False
        if max_budget and d['cost_estimate'] > max_budget:
            match = False
        if match:
            results.append(d)

    results.sort(key=lambda x: x.get('rating', 0) or 0, reverse=True)

    # Build response
    if not results and not detected_type and not detected_budget and not max_budget and not detected_season:
        return {
            'message': "👋 Hi! I'm TravelSmart Bot. Ask me things like:\n• \"Suggest a beach destination under ₹15,000\"\n• \"Best places for winter?\"\n• \"Where to go for adventure on a budget?\"\n• \"Suggest luxury destinations\"",
            'destinations': [],
            'query_understood': False
        }

    filters_used = []
    if detected_type:
        filters_used.append(detected_type.replace('_', ' ').title())
    if detected_budget:
        filters_used.append(detected_budget.title() + ' budget')
    if detected_season:
        filters_used.append(detected_season.title())
    if max_budget:
        filters_used.append(f'under ₹{max_budget:,}')

    if results:
        msg = f"🎯 Found {len(results)} destination(s)"
        if filters_used:
            msg += f" matching: {', '.join(filters_used)}"
        msg += ". Here are my top picks:"
    else:
        msg = f"😔 No destinations found matching {', '.join(filters_used) if filters_used else 'your criteria'}. Try broader filters!"

    return {
        'message': msg,
        'destinations': results[:5],
        'query_understood': True
    }

