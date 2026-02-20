import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
path = str(Path(__file__).resolve().parent.parent)
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aklatbayon_api.settings')

application = get_wsgi_application()

# Vercel needs the application assigned to a variable named 'app'
app = application
