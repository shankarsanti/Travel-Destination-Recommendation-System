import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'travel-recommendation-secret-key-2025'
    
    # Use /tmp directory for database in serverless environment (Vercel)
    if os.environ.get('VERCEL'):
        DATABASE = '/tmp/travel.db'
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'travel.db')
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

