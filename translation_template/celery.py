import os
from dotenv import load_dotenv
from celery import Celery

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
load_dotenv(env_file)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'translation_template.settings')
app = Celery('translation_template',  broker=os.environ.get('CELERY_BROKER_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
