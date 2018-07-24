# Django settings for spreadsite project.

import sys

import environ

env = environ.Env(
    DEBUG=(bool, False),
    STATIC_ROOT=(str, None),
    STATIC_URL=(str, None),
    SECRET_KEY=str,
    HTTPLIB2_CACHE_DIR=(str, '/var/tmp/jeremydaysite-httplib2-cache'),
)
environ.Env.read_env()
local_file = environ.Path(__file__) - 1

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    'spreadsite.org',
    'www.spreadsite.org',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'development.db'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = local_file('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/home/spreadsite/media/'

if env('STATIC_ROOT'):
    STATIC_URL = env('STATIC_URL', default='//static.spreadsite.org/')
    STATIC_ROOT = env('STATIC_ROOT')  # e.g., '/home/spreadsite/static')
    if not DEBUG:
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
else:
    STATIC_URL = '/STATIC/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

CACHES = {
    'default': (
        {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    if DEBUG else
        {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': env('CACHE_DIR'),
        }
    ),
}

SPREADLINKS_DIR = local_file('resource-libraries')
SPREADLINKS_PER_PAGE = 25

DOWNBLOG_DIR = local_file('blog-entries')

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret-key-value' if DEBUG else env('SECRET_KEY')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'spreadsite.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'downblog',
    'spreadlinks',
)
