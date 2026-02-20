import os
import sys

# Add the outer aklatbayon_api directory to the python path so the inner aklatbayon_api module is found
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'aklatbayon_api'))

# Import the WSGI application
from aklatbayon_api.wsgi import application

# Vercel Serverless requires the variable to be named 'app'
app = application
