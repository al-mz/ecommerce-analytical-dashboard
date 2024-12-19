import os
import logging
from celery.schedules import crontab
from flask_appbuilder.security.manager import AUTH_OAUTH
from flask_caching.backends.filesystemcache import FileSystemCache
from superset.config import DATA_DIR
from superset.utils.log import DBEventLogger

# BASE SETTING
SUPERSET_DEPLOYED_ENVIRONMENT = os.getenv("SUPERSET_DEPLOYED_ENVIRONMENT")
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("SUPERSET_METADATA_DATABASE_URL")
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')

# if mapbox api key is not set, log a warning
if not MAPBOX_API_KEY:
    logging.warning("MAPBOX_API_KEY is not set. Map will not be displayed.")

# set persistent storage backend for flask rate limiter
RATELIMIT_STORAGE_URI = "redis://redis:6379"

# set cache backend
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG


# set celery config
class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig