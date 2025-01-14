"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from decouple import config
from azure.monitor.opentelemetry import configure_azure_monitor
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

try:
    if config("APPLICATIONINSIGHTS_CONNECTION_STRING", default=""):
        configure_azure_monitor()
except Exception as e:
    print(f"Azure Monitor configuration failed: {e}")

try:
    application = get_wsgi_application()
except Exception as e:
    print(f"Failed to load WSGI application: {e}")
    raise