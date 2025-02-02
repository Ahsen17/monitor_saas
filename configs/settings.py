"""
Django settings for saas project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from configs.config import *
from common.utils.parsers import TomlParser
from register import apps

from django.core.management.commands.runserver import Command


# ===============================================
# service configurations 
# ===============================================
serviceConf = ServiceConfig()
runtimeEnv = serviceConf.environment
os.environ.setdefault('RUNTIME_ENV', runtimeEnv)
Command.default_addr = serviceConf.host
Command.default_port = serviceConf.port

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j9k*^79@e1x^dsqmoa@*=^gty2#e&)rwvvt+-93=$&)7=mp57a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
INSTALLED_APPS.extend(apps.APPS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'router.routes'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

mysqlConf = MysqlConfig()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': mysqlConf.host,
        'PORT': mysqlConf.port,
        'NAME': mysqlConf.database,
        'USER': mysqlConf.user,
        'PASSWORD': mysqlConf.password
    },
    'standalone': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===============================================
# cache configurations 
# ===============================================

redisConf = RedisConfig()

CACHE_BROKER = f"redis://{redisConf.username}:{redisConf.password}" + \
    f"@{redisConf.host}:{redisConf.port}/{redisConf.database}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHE_BROKER,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        }
    }
}


# ===============================================
# logger configurations 
# ===============================================

# 指定日志的目录所在，如果不存在则创建
LOG_ROOT = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

# 日志配置（基本跟原生的TimedRotatingFileHandler一样）
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'servers': {
            'class': 'common.utils.log.InterceptTimedRotatingFileHandler',  # 这个路径看你本地放在哪里(下面的log文件)
            'filename': os.path.join(LOG_ROOT, 'server.log'),
            'when': "D",
            'interval': 1,
            'backupCount': 1,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'debug': {
            'class': 'common.utils.log.InterceptTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'debug.log'),
            'when': "D",
            'interval': 1,
            'backupCount': 1,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'db': {
            'class': 'common.utils.log.InterceptTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'database.log'),
            'when': "D",
            'interval': 1,
            'backupCount': 1,
            'formatter': 'standard',
            'encoding': 'utf-8',
            'logging_levels': ['debug']  
        },
        'celery': {
            'class': 'common.utils.log.InterceptTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'celery.log'),
            'when': "D",
            'interval': 1,
            'backupCount': 1,
            'formatter': 'standard',
            'encoding': 'utf-8',
            'logging_levels': ['debug']  
        }
    },
    'loggers': {
        # Django全局绑定
        'django': {
            'handlers': ['servers'],
            'propagate': True,
            'level': "INFO"
        },
        'celery': {
            'handlers': ['celery'],
            'propagate': False,
            'level': "INFO"
        },
        'django.db.backends': {
            'handlers': ['db'],
            'propagate': False,
            'level': "INFO"
        },
        'django.request': {
            'handlers': ['servers'],
            'propagate': False,
            'level': "INFO"
        },
        'django.debug': {
            'handlers': ['debug'],
            'propagate': False,
            'level': "DEBUG"
        },
    }
}
