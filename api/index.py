import sys
import os

# Add the project root to the sys.path so Vercel can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# This file acts as the entry point for Vercel
# Vercel looks for an 'app' object in a file in the api/ directory
