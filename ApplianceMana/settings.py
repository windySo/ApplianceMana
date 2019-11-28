"""
Django settings for ApplianceMana project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p3q+ajbz$^9+go1)0(*ihnn@t@wj9v&5opm05y)j38^681#r3+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
'*',
]

# 使用自定义用户(app.model)
AUTH_USER_MODEL = 'myuser.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_jwt',
    'redis',
    'myuser.apps.MyuserConfig',
    'appliance.apps.ApplianceConfig',
    'django_apscheduler',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域

    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ApplianceMana.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'ApplianceMana.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appliance',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 时区设置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# 静态文件设置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]

# 文件上传路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_DIRS = [
    os.path.join(BASE_DIR,'media'),
]

#邮箱设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com' #发送邮件的SMTP服务器
EMAIL_HOST_USER = 'XXX'
EMAIL_HOST_PASSWORD = 'PASSWORD'
EMAIL_PORT = 25 #发件箱的SMTP服务器端口
EMAIL_USE_TLS = True #使用TLS安全传输协议
DEFAULT_FROM_EMAIL = 'XXX'


# JWT配置

JWT_AUTH = {
    # 使用自定义Handler
    'JWT_RESPONSE_PAYLOAD_HANDLER':'myuser.utils.jwt_response_playload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=86400),
}

# 使用自定义后台认证
AUTHENTICATION_BACKENDS = [
    'myuser.utils.UsernameMobileAuthBackend',
]


# Cache缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"



# 日志配置
LOG_PATH = os.path.join(BASE_DIR, 'log')
LOGGING = {
    'version': 1, #保留字
    # 是否禁用其他
    'disable_existing_loggers': False,
    'formatters': {
        # 详细
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d  %(thread)d %(message)s'
        },
        # 简单，可以自己添加或减少，看需求
        'simple': {
            'format': '%(levelname)s %(module)s  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },

        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '%s/all.log'%LOG_PATH,
            'formatter':'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file','console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file','console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}



# 跨域忽略配置
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
REST_FRAMEWORK = {
    'PAGE_SIZE': 2
}
