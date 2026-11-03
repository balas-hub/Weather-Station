import os
import sys
from django.apps import AppConfig

class AiEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_engine'
    verbose_name = 'AI Weather Intelligence Engine'

    def ready(self):
        # Only start scheduler in the main Django server process, avoiding duplicate jobs in dev auto-reload
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
            try:
                from .scheduler import start_weather_ai_scheduler
                start_weather_ai_scheduler()
            except Exception as e:
                print(f"[AI SCHEDULER] Could not start scheduler: {e}")
