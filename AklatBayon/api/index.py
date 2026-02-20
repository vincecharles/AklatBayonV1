import os
import sys

# Add the aklatbayon_api directory to the python path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'aklatbayon_api'))

from aklatbayon_api.wsgi import application

# Vercel requires the app variable
app = application
