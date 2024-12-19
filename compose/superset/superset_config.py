import os

MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://redis:6379/1'}
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://superset:superset@postgres:5432/superset'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisISaSECRET_1234'

# -----------------------------------------------------------------
import os
from typing import Any

from celery.schedules import crontab
from flask_appbuilder.security.manager import AUTH_OAUTH
from flask_caching.backends.filesystemcache import FileSystemCache
from superset.config import DATA_DIR
from superset.utils.log import DBEventLogger

# BASE SETTING
SUPERSET_DEPLOYED_ENVIRONMENT = os.getenv("SUPERSET_DEPLOYED_ENVIRONMENT")
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("SUPERSET_METADATA_DATABASE_URL")

# # Create custom event logger
# class FileDBEventLogger(DBEventLogger):
#     """Event logger that commits logs to Superset DB and writes logs to a file"""

#     def __init__(self) -> None:
#         super().__init__()

#     def log(  # pylint: disable=too-many-arguments,too-many-locals
#         self,
#         user_id: int | None,
#         action: str,
#         dashboard_id: int | None,
#         duration_ms: int | None,
#         slice_id: int | None,
#         referrer: str | None,
#         *args: Any,
#         **kwargs: Any,
#     ) -> None:
#         super().log(
#             user_id,
#             action,
#             dashboard_id,
#             duration_ms,
#             slice_id,
#             referrer,
#             *args,
#             **kwargs,
#         )
#         # Include the current date in the log filename
#         date_str = datetime.now().strftime("%Y_%m_%d")
#         self.file_path = os.path.join(DATA_DIR, "logs", f"events_{date_str}.log")

#         # make sure the directory exists
#         os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

#         records = kwargs.get("records", [])
#         separator = "-" * 30
#         with open(self.file_path, "a") as log_file:
#             for record in records:
#                 try:
#                     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     log_message = (
#                         f"Timestamp: {timestamp}, User_id: {user_id}, Action: {action}, "
#                         f"Dashboard_id: {dashboard_id}, Duration_ms: {duration_ms}, "
#                         f"Slice_id: {slice_id}, Referrer: {referrer}, Record: {json.dumps(record)}"
#                     )
#                     log_file.write(log_message + "\n")
#                     log_file.write(separator + "\n")
#                 except Exception as ex:  # pylint: disable=broad-except
#                     logging.error("FileDBEventLogger failed to write log record")
#                     logging.exception(ex)


# EVENT_LOGGER = FileDBEventLogger()


# Custom query logger
# def custom_query_logger(
#     database_url,
#     query,
#     schema=None,
#     client=None,
#     security_manager=None,
#     log_params=None,
# ):
#     log_message = (
#         f"Query: {query}, Schema: {schema}, Client: {client}, Security Manager: {security_manager}, "
#         f"Log Params: {log_params}"
#     )
#     separator = "-" * 30

#     # log directory
#     date_str = datetime.now().strftime("%Y_%m_%d")
#     log_file_path = os.path.join(DATA_DIR, "logs", f"query_{date_str}.log")
#     os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

#     # Log the query to a file
#     with open(log_file_path, "a") as log_file:
#         log_file.write(log_message + "\n")
#         log_file.write(separator + "\n")


# QUERY_LOGGER = custom_query_logger

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