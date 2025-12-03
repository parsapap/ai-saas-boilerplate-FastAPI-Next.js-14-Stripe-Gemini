from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
)

# Scheduled tasks
celery_app.conf.beat_schedule = {
    'reset-daily-usage': {
        'task': 'reset_daily_usage',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight UTC
    },
    'generate-usage-reports': {
        'task': 'generate_usage_reports',
        'schedule': crontab(hour=1, minute=0, day_of_week=1),  # Weekly on Monday at 1 AM UTC
    },
    'check-subscription-renewals': {
        'task': 'check_subscription_renewals',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM UTC
    },
    'cleanup-old-usage-data': {
        'task': 'cleanup_old_usage_data',
        'schedule': crontab(hour=2, minute=0, day_of_month=1),  # Monthly on 1st at 2 AM UTC
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks(['app.tasks'])
