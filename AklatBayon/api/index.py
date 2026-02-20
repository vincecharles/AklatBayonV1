import os
import sys

# Define path to exactly where the settings live
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
API_DIR = os.path.join(PROJECT_DIR, 'aklatbayon_api')
sys.path.insert(0, API_DIR)

from aklatbayon_api.wsgi import application
app = application
