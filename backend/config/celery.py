import os

from celery import Celery

# Tell Celery which Django settings file to use
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

app = Celery("food_marketplace")

# Read all settings that start with CELERY_
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# Automatically discover tasks.py in all installed apps
app.autodiscover_tasks()