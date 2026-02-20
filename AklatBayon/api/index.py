import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'aklatbayon_api'))

from aklatbayon_api.wsgi import application

app = application
