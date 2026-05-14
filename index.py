"""
Vercel Entry Point
This file is used by Vercel to run the Flask application
"""
from app import app

# Vercel expects the app to be named 'app' or exposed via this file
# This is the WSGI application that Vercel will use
