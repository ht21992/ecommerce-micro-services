# inventory_service/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory_service.settings")

app = Celery("inventory_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

app.autodiscover_tasks()

app.conf.task_routes = {
    "inventory.tasks.*": {"queue": "inventory-queue"},
}
