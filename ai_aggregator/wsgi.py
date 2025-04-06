# ai_aggregator/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_aggregator.settings')

# We renamed 'application' to 'app' here!
application = get_wsgi_application()