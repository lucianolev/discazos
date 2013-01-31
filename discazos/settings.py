import os

# Django settings for discazos project.

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Luciano Leveroni', 'lucianolev@gmail.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-AR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, '../media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, '../static')

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'discazos.urls'

LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
    #Django third-party
    'debug_toolbar',
    'django_nose',
    'south',
    'django_extensions',
    'django_countries',
    'sorl.thumbnail',
    'dajaxice',
    'registration',
    'floppyforms',
    'bootstrap-pagination',
    
    #Discazos
    'discazos.website',
    'discazos.albums',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'discazos.context_processors.VersionContextProcessor',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

DEFAULT_FROM_EMAIL = 'Discazos <no-reply@discazos.net>'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/discazos.log'
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        #'django.request': {
        #    'handlers': ['mail_admins'],
        #    'level': 'ERROR',
        #    'propagate': True,
        #},
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False,
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Project-specific settings

BROWSER_EXTENSION_VERSION = '0.5.3'
CREATOR_XML_CURRENT_VER = '0.3'

ALBUM_SEARCH_RESULTS_LIMIT = 5
ALBUMS_PER_PAGE = 10
ARTISTS_PER_PAGE = 10

PROBLEM_REPORT_EMAIL = "contacto@discazos.net"

# End of project-specific settings

try:
    from local_settings import *
except ImportError:
    print("There's no local_settings.py defined. Please base it in "
          "local_settings.py.example")
    exit()

