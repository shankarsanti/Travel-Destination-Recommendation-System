"""Seed the database with sample travel destinations."""
from database import get_db, close_db
from werkzeug.security import generate_password_hash

DESTINATIONS = [
    {
        "name": "Goa", "country": "India", "state": "Goa",
        "description": "Famous for its stunning beaches, vibrant nightlife, Portuguese heritage, and water sports. Goa offers a perfect blend of relaxation and adventure with its golden sandy beaches and rich cultural heritage.",
        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "beach",
        "best_season": "winter", "duration_days": 5, "cost_estimate": 15000, "rating": 4.5,
        "latitude": 15.2993, "longitude": 74.1240,
        "attractions": "Baga Beach, Basilica of Bom Jesus, Fort Aguada, Dudhsagar Falls, Anjuna Flea Market",
        "highlights": "Water sports, Casino cruises, Spice plantations, Old Goa churches",
        "how_to_reach": "Nearest Airport: Dabolim Airport (GOI). Well connected by train to Madgaon and Vasco stations. Buses available from major cities.",
        "best_time_detail": "October to March offers pleasant weather with temperatures between 20-32°C."
    },
    {
        "name": "Manali", "country": "India", "state": "Himachal Pradesh",
        "description": "A breathtaking hill station nestled in the mountains of Himachal Pradesh. Known for snow-capped peaks, lush green valleys, adventure sports, and ancient temples.",
        "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "hill_station",
        "best_season": "summer", "duration_days": 5, "cost_estimate": 12000, "rating": 4.6,
        "latitude": 32.2396, "longitude": 77.1887,
        "attractions": "Rohtang Pass, Solang Valley, Hadimba Temple, Old Manali, Jogini Waterfall",
        "highlights": "Skiing, Paragliding, River rafting, Trekking, Camping",
        "how_to_reach": "Nearest Airport: Kullu-Manali Airport (Bhuntar). Bus services from Delhi (12-14 hrs). Volvo buses available overnight.",
        "best_time_detail": "March to June for pleasant weather; December to February for snowfall."
    },
    {
        "name": "Jaipur", "country": "India", "state": "Rajasthan",
        "description": "The Pink City of India, known for its stunning palaces, forts, vibrant bazaars, and rich Rajasthani culture. A UNESCO World Heritage city with magnificent architecture.",
        "image_url": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "historical",
        "best_season": "winter", "duration_days": 4, "cost_estimate": 10000, "rating": 4.4,
        "latitude": 26.9124, "longitude": 75.7873,
        "attractions": "Amber Fort, Hawa Mahal, City Palace, Jantar Mantar, Nahargarh Fort",
        "highlights": "Elephant rides, Block printing workshops, Traditional Rajasthani cuisine, Bazaar shopping",
        "how_to_reach": "Jaipur International Airport. Major railway junction. Well connected by NH-48 from Delhi (5 hrs).",
        "best_time_detail": "October to March is ideal with cool, pleasant weather."
    },
    {
        "name": "Kerala Backwaters", "country": "India", "state": "Kerala",
        "description": "Experience the serene backwaters of Kerala on traditional houseboats. Known as God's Own Country, Kerala offers lush greenery, tranquil waters, and Ayurvedic wellness.",
        "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "nature",
        "best_season": "winter", "duration_days": 6, "cost_estimate": 18000, "rating": 4.7,
        "latitude": 9.4981, "longitude": 76.3388,
        "attractions": "Alleppey Backwaters, Munnar Tea Gardens, Periyar Wildlife Sanctuary, Fort Kochi, Kovalam Beach",
        "highlights": "Houseboat cruises, Ayurvedic spa, Tea plantation tours, Kathakali performances",
        "how_to_reach": "Airports at Kochi, Thiruvananthapuram. Well connected by rail and road.",
        "best_time_detail": "September to March offers the best weather for backwater cruises."
    },
    {
        "name": "Ladakh", "country": "India", "state": "Jammu & Kashmir",
        "description": "The Land of High Passes, offering dramatic landscapes, ancient monasteries, pristine lakes, and thrilling adventure experiences at high altitudes.",
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop", "budget_category": "luxury", "travel_type": "adventure",
        "best_season": "summer", "duration_days": 8, "cost_estimate": 35000, "rating": 4.8,
        "latitude": 34.1526, "longitude": 77.5771,
        "attractions": "Pangong Lake, Nubra Valley, Magnetic Hill, Khardung La Pass, Hemis Monastery",
        "highlights": "Mountain biking, Camping, River rafting, Monastery visits, Stargazing",
        "how_to_reach": "Kushok Bakula Rimpochee Airport (Leh). Road trips from Manali or Srinagar.",
        "best_time_detail": "June to September when roads are open and weather is suitable."
    },
    {
        "name": "Varanasi", "country": "India", "state": "Uttar Pradesh",
        "description": "One of the oldest living cities in the world, Varanasi is the spiritual capital of India. Experience the mesmerizing Ganga Aarti, ancient temples, and rich cultural traditions.",
        "image_url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=600&h=400&fit=crop", "budget_category": "budget", "travel_type": "pilgrimage",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 6000, "rating": 4.3,
        "latitude": 25.3176, "longitude": 82.9739,
        "attractions": "Dashashwamedh Ghat, Kashi Vishwanath Temple, Sarnath, Boat ride on Ganges, Ramnagar Fort",
        "highlights": "Ganga Aarti, Silk weaving, Ancient ghats, Street food, Sarnath Buddhist site",
        "how_to_reach": "Lal Bahadur Shastri Airport. Varanasi Junction railway station. Well connected by road.",
        "best_time_detail": "October to March offers pleasant weather for sightseeing."
    },
    {
        "name": "Andaman Islands", "country": "India", "state": "Andaman & Nicobar",
        "description": "A tropical paradise with crystal-clear waters, pristine beaches, vibrant coral reefs, and lush tropical forests. Perfect for beach lovers and water sports enthusiasts.",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=400&fit=crop", "budget_category": "luxury", "travel_type": "beach",
        "best_season": "winter", "duration_days": 7, "cost_estimate": 30000, "rating": 4.6,
        "latitude": 11.7401, "longitude": 92.6586,
        "attractions": "Radhanagar Beach, Cellular Jail, Ross Island, Scuba Diving at Havelock, Baratang Limestone Caves",
        "highlights": "Scuba diving, Snorkeling, Sea walking, Glass-bottom boat rides, Bioluminescence",
        "how_to_reach": "Veer Savarkar International Airport (Port Blair). Ships from Chennai and Kolkata.",
        "best_time_detail": "October to May with calm seas and clear skies."
    },
    {
        "name": "Jim Corbett National Park", "country": "India", "state": "Uttarakhand",
        "description": "India's oldest national park, famous for its Bengal tigers and diverse wildlife. A paradise for nature and wildlife photography enthusiasts.",
        "image_url": "https://images.unsplash.com/photo-1549366021-9f761d450615?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "wildlife",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 10000, "rating": 4.4,
        "latitude": 29.5300, "longitude": 78.7747,
        "attractions": "Dhikala Zone, Bijrani Zone, Jhirna Zone, Corbett Waterfall, Garjia Temple",
        "highlights": "Tiger safari, Bird watching, Elephant rides, River rafting in Kosi",
        "how_to_reach": "Nearest Airport: Pantnagar. Ramnagar Railway Station (12 km). Buses from Delhi (6 hrs).",
        "best_time_detail": "November to June, with best tiger sightings in March-June."
    },
    {
        "name": "Hampi", "country": "India", "state": "Karnataka",
        "description": "A UNESCO World Heritage Site with magnificent ruins of the Vijayanagara Empire. Boulder-strewn landscapes, ancient temples, and rich history make Hampi a unique destination.",
        "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=600&h=400&fit=crop", "budget_category": "budget", "travel_type": "historical",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 5000, "rating": 4.5,
        "latitude": 15.3350, "longitude": 76.4600,
        "attractions": "Virupaksha Temple, Vittala Temple, Lotus Mahal, Elephant Stables, Hemakuta Hill",
        "highlights": "Rock climbing, Coracle rides, Temple architecture, Sunset at Hemakuta, Bicycle exploration",
        "how_to_reach": "Nearest Airport: Hubli (143 km). Hospet Railway Station (13 km). Buses from Bangalore and Goa.",
        "best_time_detail": "October to February with pleasant weather for exploring ruins."
    },
    {
        "name": "Rishikesh", "country": "India", "state": "Uttarakhand",
        "description": "The Yoga Capital of the World, nestled in the foothills of the Himalayas along the sacred Ganges. A perfect blend of spirituality and adventure.",
        "image_url": "https://images.unsplash.com/photo-1600011689032-8b628b8a8747?w=600&h=400&fit=crop", "budget_category": "budget", "travel_type": "adventure",
        "best_season": "all", "duration_days": 4, "cost_estimate": 7000, "rating": 4.5,
        "latitude": 30.0869, "longitude": 78.2676,
        "attractions": "Laxman Jhula, Ram Jhula, Triveni Ghat, Beatles Ashram, Neelkanth Mahadev Temple",
        "highlights": "White water rafting, Bungee jumping, Camping, Yoga retreats, Cliff jumping",
        "how_to_reach": "Nearest Airport: Jolly Grant Airport (35 km). Rishikesh Railway Station. Buses from Delhi (6 hrs).",
        "best_time_detail": "February to May and September to November for adventure activities."
    },
    {
        "name": "Darjeeling", "country": "India", "state": "West Bengal",
        "description": "The Queen of Hills, famous for its tea gardens, stunning views of Kanchenjunga, the toy train, and colonial charm.",
        "image_url": "https://images.unsplash.com/photo-1622308644420-b20142dc993c?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "hill_station",
        "best_season": "spring", "duration_days": 5, "cost_estimate": 12000, "rating": 4.4,
        "latitude": 27.0360, "longitude": 88.2627,
        "attractions": "Tiger Hill, Batasia Loop, Tea Gardens, Peace Pagoda, Darjeeling Himalayan Railway",
        "highlights": "Sunrise at Tiger Hill, Tea tasting, Toy train ride, Trekking, Monastery visits",
        "how_to_reach": "Nearest Airport: Bagdogra (67 km). New Jalpaiguri Railway Station (88 km). Shared jeeps available.",
        "best_time_detail": "March to May for clear views of Kanchenjunga and pleasant weather."
    },
    {
        "name": "Udaipur", "country": "India", "state": "Rajasthan",
        "description": "The City of Lakes, known for its romantic setting, stunning palaces on lake shores, rich cultural heritage, and vibrant art scene.",
        "image_url": "https://images.unsplash.com/photo-1524230572899-a752b3835840?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "cultural",
        "best_season": "winter", "duration_days": 4, "cost_estimate": 12000, "rating": 4.6,
        "latitude": 24.5854, "longitude": 73.7125,
        "attractions": "City Palace, Lake Pichola, Jag Mandir, Saheliyon Ki Bari, Fateh Sagar Lake",
        "highlights": "Boat ride on Lake Pichola, Sunset at Monsoon Palace, Traditional Rajasthani dance, Miniature painting",
        "how_to_reach": "Maharana Pratap Airport. Udaipur City Railway Station. Well connected by road from major cities.",
        "best_time_detail": "September to March for pleasant weather and festive season."
    },
    {
        "name": "Ooty", "country": "India", "state": "Tamil Nadu",
        "description": "The Queen of Hill Stations in the Nilgiri Hills. Known for its botanical gardens, tea estates, scenic toy train, and pleasant climate year-round.",
        "image_url": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=600&h=400&fit=crop", "budget_category": "budget", "travel_type": "hill_station",
        "best_season": "summer", "duration_days": 3, "cost_estimate": 8000, "rating": 4.3,
        "latitude": 11.4102, "longitude": 76.6950,
        "attractions": "Botanical Gardens, Ooty Lake, Doddabetta Peak, Tea Museum, Rose Garden",
        "highlights": "Nilgiri Mountain Railway, Tea plantation tours, Boating, Trekking, Photography",
        "how_to_reach": "Nearest Airport: Coimbatore (88 km). Mettupalayam Railway Station for toy train. Buses from Bangalore and Mysore.",
        "best_time_detail": "April to June for summer retreat; October to November for post-monsoon beauty."
    },
    {
        "name": "Rann of Kutch", "country": "India", "state": "Gujarat",
        "description": "A vast white salt desert that transforms into a magical landscape, especially during the Rann Utsav festival. A unique cultural and natural experience.",
        "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "cultural",
        "best_season": "winter", "duration_days": 4, "cost_estimate": 15000, "rating": 4.3,
        "latitude": 23.7337, "longitude": 69.8597,
        "attractions": "White Rann, Kala Dungar, Mandvi Beach, Aina Mahal, Prag Mahal",
        "highlights": "Rann Utsav festival, Full moon night on white desert, Handicraft villages, Camel safari",
        "how_to_reach": "Nearest Airport: Bhuj (80 km). Bhuj Railway Station. State transport buses available.",
        "best_time_detail": "November to February during Rann Utsav for the best experience."
    },
    {
        "name": "Coorg", "country": "India", "state": "Karnataka",
        "description": "The Scotland of India, nestled in the Western Ghats. Famous for its coffee plantations, misty hills, waterfalls, and Kodava culture.",
        "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "nature",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 9000, "rating": 4.5,
        "latitude": 12.3375, "longitude": 75.8069,
        "attractions": "Abbey Falls, Raja's Seat, Dubare Elephant Camp, Talacauvery, Namdroling Monastery",
        "highlights": "Coffee plantation walks, Trekking, River rafting, Elephant interaction, Kodava cuisine",
        "how_to_reach": "Nearest Airport: Mangalore (160 km) or Mysore (120 km). Buses from Bangalore (5-6 hrs) and Mysore (3 hrs).",
        "best_time_detail": "October to March for pleasant weather; June-September for lush green monsoon beauty."
    },
    {
        "name": "Lakshadweep", "country": "India", "state": "Lakshadweep",
        "description": "A tropical archipelago with stunning coral atolls, turquoise lagoons, and pristine beaches. One of India's most exclusive and untouched paradise destinations.",
        "image_url": "https://images.unsplash.com/photo-1468413253725-0d5181091126?w=600&h=400&fit=crop", "budget_category": "luxury", "travel_type": "beach",
        "best_season": "winter", "duration_days": 5, "cost_estimate": 40000, "rating": 4.7,
        "latitude": 10.5667, "longitude": 72.6417,
        "attractions": "Agatti Island, Bangaram Atoll, Kavaratti, Minicoy Island, Marine Museum",
        "highlights": "Scuba diving, Snorkeling, Kayaking, Glass-bottom boat rides, Coral reef exploration",
        "how_to_reach": "Agatti Airport from Kochi. Ships from Kochi (14-20 hrs). Entry permit required.",
        "best_time_detail": "October to May when the sea is calm for water activities."
    },
    {
        "name": "Mysore", "country": "India", "state": "Karnataka",
        "description": "The City of Palaces, known for its royal heritage, magnificent Mysore Palace, Dasara festival, silk sarees, and rich cultural traditions.",
        "image_url": "https://images.unsplash.com/photo-1595658658481-d53d3f999875?w=600&h=400&fit=crop", "budget_category": "budget", "travel_type": "cultural",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 6000, "rating": 4.4,
        "latitude": 12.2958, "longitude": 76.6394,
        "attractions": "Mysore Palace, Chamundi Hills, Brindavan Gardens, St. Philomena's Church, Mysore Zoo",
        "highlights": "Palace illumination, Dasara festival, Silk shopping, Mysore Pak sweets, Yoga traditions",
        "how_to_reach": "Mysore Airport. Mysore Junction Railway Station. Well connected by road from Bangalore (3 hrs).",
        "best_time_detail": "October to February; Dasara in October is spectacular."
    },
    {
        "name": "Shimla", "country": "India", "state": "Himachal Pradesh",
        "description": "The former summer capital of British India, known for its colonial architecture, scenic beauty, pleasant climate, and charming Mall Road.",
        "image_url": "https://images.unsplash.com/photo-1597074866923-dc0589150358?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "hill_station",
        "best_season": "summer", "duration_days": 4, "cost_estimate": 10000, "rating": 4.3,
        "latitude": 31.1048, "longitude": 77.1734,
        "attractions": "Mall Road, The Ridge, Christ Church, Jakhoo Temple, Kufri, Chadwick Falls",
        "highlights": "Toy train ride, Ice skating, Trekking, Colonial architecture walk, Apple orchards",
        "how_to_reach": "Jubbarhatti Airport (23 km). Shimla Railway Station (toy train from Kalka). Buses from Delhi (8-10 hrs).",
        "best_time_detail": "March to June for summer escape; December to February for snowfall."
    },
    {
        "name": "Kaziranga National Park", "country": "India", "state": "Assam",
        "description": "Home to two-thirds of the world's great one-horned rhinoceros. A UNESCO World Heritage Site with diverse wildlife and stunning landscapes.",
        "image_url": "https://images.unsplash.com/photo-1456926631375-92c8ce872def?w=600&h=400&fit=crop", "budget_category": "moderate", "travel_type": "wildlife",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 12000, "rating": 4.6,
        "latitude": 26.5775, "longitude": 93.1711,
        "attractions": "Elephant Safari, Jeep Safari, Central Range, Western Range, Orchid Park",
        "highlights": "One-horned rhino sighting, Elephant safari, Bird watching, Tea garden visits",
        "how_to_reach": "Nearest Airport: Jorhat (97 km) or Guwahati (217 km). Furkating Railway Station (75 km). NH-37 connects the park.",
        "best_time_detail": "November to April when the park is open. Best wildlife sighting in Feb-March."
    },
    {
        "name": "Amritsar", "country": "India", "state": "Punjab",
        "description": "The spiritual and cultural center of the Sikh religion. Home to the iconic Golden Temple, vibrant Punjabi culture, and the historic Wagah Border ceremony.",
        "image_url": "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?w=600&h=400&fit=crop", "budget_category": "budget", "travel_type": "pilgrimage",
        "best_season": "winter", "duration_days": 3, "cost_estimate": 5000, "rating": 4.7,
        "latitude": 31.6340, "longitude": 74.8723,
        "attractions": "Golden Temple, Wagah Border, Jallianwala Bagh, Partition Museum, Hall Bazaar",
        "highlights": "Langar at Golden Temple, Wagah Border ceremony, Punjabi street food, Phulkari shopping",
        "how_to_reach": "Sri Guru Ram Dass Jee International Airport. Amritsar Junction Railway Station. Well connected by road.",
        "best_time_detail": "October to March for comfortable weather."
    }
]


def seed_database():
    """Insert sample data into the database."""
    db = get_db()
    cursor = db.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM destinations")
    if cursor.fetchone()[0] > 0:
        print("Database already seeded.")
        close_db(db)
        return

    # Insert destinations
    for d in DESTINATIONS:
        cursor.execute('''
            INSERT INTO destinations (name, country, state, description, image_url, 
            budget_category, travel_type, best_season, duration_days, cost_estimate, 
            rating, latitude, longitude, attractions, highlights, how_to_reach, best_time_detail)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (d['name'], d['country'], d['state'], d['description'], d['image_url'],
              d['budget_category'], d['travel_type'], d['best_season'], d['duration_days'],
              d['cost_estimate'], d['rating'], d['latitude'], d['longitude'],
              d['attractions'], d['highlights'], d['how_to_reach'], d['best_time_detail']))

    # Create admin user
    admin_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name, is_admin)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@travel.com', admin_hash, 'System Administrator', 1))

    # Create demo users for AI collaborative filtering
    demo_users = [
        ('traveler_beach', 'beach@demo.com', 'Beach Explorer', 0),
        ('traveler_adventure', 'adventure@demo.com', 'Adventure Seeker', 0),
        ('traveler_culture', 'culture@demo.com', 'Culture Enthusiast', 0),
        ('traveler_nature', 'nature@demo.com', 'Nature Lover', 0),
        ('traveler_budget', 'budget@demo.com', 'Budget Backpacker', 0),
    ]
    demo_hash = generate_password_hash('demo1234', method='pbkdf2:sha256')
    for uname, email, fname, admin in demo_users:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', (uname, email, demo_hash, fname, admin))

    # Seed user activity data for AI recommendations
    # User profiles: (user_id, list of destination_ids they interact with)
    # Admin=1, beach=2, adventure=3, culture=4, nature=5, budget=6
    activity_profiles = {
        2: [1, 7, 16, 4, 15],     # Beach lover: Goa, Andaman, Lakshadweep, Kerala, Coorg
        3: [5, 10, 2, 8, 19],     # Adventure: Ladakh, Rishikesh, Manali, Corbett, Kaziranga
        4: [3, 12, 14, 17, 6],    # Culture: Jaipur, Udaipur, Kutch, Mysore, Varanasi
        5: [4, 15, 11, 13, 8],    # Nature: Kerala, Coorg, Darjeeling, Ooty, Corbett
        6: [6, 9, 10, 20, 17],    # Budget: Varanasi, Hampi, Rishikesh, Amritsar, Mysore
    }

    for user_id, dest_ids in activity_profiles.items():
        for dest_id in dest_ids:
            # Multiple views to simulate real browsing
            for _ in range(3):
                cursor.execute('''
                    INSERT INTO user_activity (user_id, destination_id, action_type)
                    VALUES (?, ?, 'view')
                ''', (user_id, dest_id))
            # Wishlist the top 2
            if dest_ids.index(dest_id) < 2:
                cursor.execute('''
                    INSERT INTO wishlist (user_id, destination_id)
                    VALUES (?, ?)
                ''', (user_id, dest_id))

    db.commit()

    # Seed notifications
    notifications = [
        (None, 'Best time to visit Manali!', 'December-February is perfect for snow activities in Manali', 'weather', '/destination/2'),
        (None, 'New destination added!', 'Explore the stunning Lakshadweep islands', 'new', '/destination/16'),
        (None, 'Summer deals available', 'Budget-friendly hill station trips starting at ₹5,000', 'deal', '/explore?season=summer'),
        (None, 'Trending: Goa is hot!', 'Goa is the most wishlisted destination this season', 'info', '/destination/1'),
        (None, 'Winter is coming', 'Plan your winter getaway to Rajasthan now!', 'weather', '/explore?season=winter'),
    ]
    for user_id, title, message, ntype, link in notifications:
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, notif_type, link)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, message, ntype, link))

    # Add gallery images for select destinations
    gallery_data = {
        'Goa': 'https://images.unsplash.com/photo-1614082242765-7c98ca0f3df3?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1587922546307-776227941871?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400&h=300&fit=crop',
        'Manali': 'https://images.unsplash.com/photo-1571401835393-8c5f35328320?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=400&h=300&fit=crop',
        'Jaipur': 'https://images.unsplash.com/photo-1534751516642-a1af1ef26a56?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1477587458883-47145ed94245?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1599661046289-e31897846e41?w=400&h=300&fit=crop',
        'Ladakh': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=400&h=300&fit=crop|https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop',
    }
    for name, imgs in gallery_data.items():
        cursor.execute('UPDATE destinations SET gallery_images = ? WHERE name = ?', (imgs, name))

    db.commit()
    close_db(db)
    print("Database seeded with sample destinations, users, and AI activity data!")


if __name__ == '__main__':
    seed_database()

