web: cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
worker: cd backend && celery -A app.tasks.celery_app worker --loglevel=info
beat: cd backend && celery -A app.tasks.celery_app beat --loglevel=info
