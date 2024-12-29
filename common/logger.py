
import logging


djangoLogger = logging.getLogger('django')
celeryLogger = logging.getLogger('celery')
databaseLogger = logging.getLogger('django.db.backends')
requestLogger = logging.getLogger('django.request')
debugLogger = logging.getLogger('django.debug')