# Django settings for example project.
import os
PROJECT_DIR = lambda base : os.path.abspath(os.path.join(os.path.dirname(__file__), base).replace('\\','/'))
gettext = lambda s: s

DEBUG = False
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PROJECT_DIR('../db/example.db'),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', gettext("English")), # Main language!
    ('hy', gettext("Armenian")),
    ('nl', gettext("Dutch")),
    ('ru', gettext("Russian")),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_DIR(os.path.join('..', 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_DIR(os.path.join('..', 'static'))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR(os.path.join('..', 'media', 'static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6sf18c*w971i8a-m^1coasrmur2k6+q5_kyn*)s@(*_dk5q3&r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR('templates')
)

#FIXTURE_DIRS = (
#   PROJECT_DIR(os.path.join('..', 'fixtures'))
#)

INSTALLED_APPS = (
    # Django core and contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',

    # Third party apps used in the project
    'south', # Database migration app
    'tinymce', # TinyMCE
    'filebrowser', # Filebrowser for TinyMCE

    # Other project specific apps
    #'admin_tools_dashboard', # Admin dashboard
    'foo', # Test app
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGIN_ERROR_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

# localeurl locale independent paths (language code won't be appended)
LOCALE_INDEPENDENT_PATHS = (
    r'^/sitemap.*\.xml$', # Global regex for all XML sitemaps
    #r'^/administration/',
    #r'^/dashboard/',
)

# Tell localeurl to use sessions for language store.
LOCALEURL_USE_SESSION = True

# TinyMCE Settings
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'tiny_mce/tiny_mce.js')
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, 'tiny_mce/')
TINYMCE_CONFIG_PLUGINS = "inlinepopups,visualchars,paste,media,template,table"
TINYMCE_CONFIG_THEME = "advanced"
TINMYCE_CONFIG_MODE = "textareas"
TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS1 = "formatselect,styleselect,|,bold,italic,underline,|,undo,redo,|,bullist,numlist,hr,|,link,unlink,anchor,|,charmap,|,image,media,|,code,|,pastetext,pasteword,tablecontrols"
TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS2 = ""
TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS3 = ""
TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS4 = ""
TINYMCE_CONFIG_THEME_ADVANCED_TOOLBAR_LOCATION = "top"
TINYMCE_CONFIG_THEME_ADVANCED_TOOLBAR_ALIGN = "left"
TINYMCE_CONFIG_THEME_ADVANCED_STATUSBAR_LOCATION = "bottom"
TINYMCE_CONFIG_THEME_ADVANCED_PATH = 0
TINYMCE_CONFIG_THEME_ADVANCED_RESIZING = 1
TINYMCE_CONFIG_RELATIVE_URLS = 0
TINYMCE_CONFIG_WIDTH = '90%'
TINYMCE_CONFIG_HEIGHT = '300'
TINYMCE_CONFIG_DELTA_HEIGHT = '300'
TINYMCE_CONFIG_THEME_ADVANCED_RESIZE_HORIZONTAL = 0
TINYMCE_CONFIG_CONTENT_CSS = MEDIA_URL +"css/style_tinymce.css"
TINYMCE_CONFIG_THEME_ADVANCED_BLOCKFORMATS = "p,h2,h3,h4,h5,blockquote" #h1,
TINYMCE_CONFIG_THEME_ADVANCED_STYLES = "Big=big;Uppercase=uppercase;h1=h1;h2=h2;h3=h3;h4=h4;h5=h5;h6=h6"
TINYMCE_DEFAULT_CONFIG = {
    'plugins': TINYMCE_CONFIG_PLUGINS,
    'theme': TINYMCE_CONFIG_THEME,
    'mode': TINMYCE_CONFIG_MODE,
    'theme_advanced_buttons1': TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS1,
    'theme_advanced_buttons2': TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS2,
    'theme_advanced_buttons3': TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS3,
    'theme_advanced_buttons4': TINYMCE_CONFIG_THEME_ADVANCED_BUTTONS4,
    'theme_advanced_toolbar_location': TINYMCE_CONFIG_THEME_ADVANCED_TOOLBAR_LOCATION,
    'theme_advanced_toolbar_align': TINYMCE_CONFIG_THEME_ADVANCED_TOOLBAR_ALIGN,
    'theme_advanced_statusbar_location': TINYMCE_CONFIG_THEME_ADVANCED_STATUSBAR_LOCATION,
	'theme_advanced_path': TINYMCE_CONFIG_THEME_ADVANCED_PATH,
    'theme_advanced_resizing': TINYMCE_CONFIG_THEME_ADVANCED_RESIZING,
    'relative_urls': TINYMCE_CONFIG_RELATIVE_URLS,
    'width': TINYMCE_CONFIG_WIDTH,
    'delta_height': TINYMCE_CONFIG_DELTA_HEIGHT,
    'theme_advanced_resize_horizontal': TINYMCE_CONFIG_THEME_ADVANCED_RESIZE_HORIZONTAL,
    #'content_css' : TINYMCE_CONFIG_CONTENT_CSS,
    'theme_advanced_blockformats': TINYMCE_CONFIG_THEME_ADVANCED_BLOCKFORMATS,
    'external_link_list_url': "ss.mp4",
    #"file_browser_callback": TINYMCE_CONFIG_FILEBROWSER_CALLBACK,
    # Style formats
    'theme_advanced_styles': TINYMCE_CONFIG_THEME_ADVANCED_STYLES,
    'paste_auto_cleanup_on_paste': 1,
    'cleanup_on_startup': 1,
    'custom_undo_redo_levels': 20,
    'paste_remove_styles': 1,
    'paste_remove_styles_if_webkit': 1,
    'paste_strip_class_attributes': 1,
}

# HTML tags which come from TinyMCE will be whitelisted to this list.
TINYMCE_DISABLE_CLEANING = True
TINYMCE_ALLOWED_TAGS = [
    'a', 'b', 'em', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', \
    'li', 'ol', 'p', 'strong', 'ul', 'img', 'br', 'table', \
    'thead', 'tbody', 'th', 'tr', 'td', 'blockquote', 'hr'
]
TINYMCE_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'style', 'align', 'class'],
    'img': ['id', 'src', 'alt', 'style', 'width', 'height', 'class', 'title', 'align'],
    'div': ['class', 'style'],
    'table': ['cellpadding', 'cellspacing', 'border',],
    'object': ['class', 'style', 'width', 'height', 'data', 'type', 'id', 'align'],
    'param': ['name', 'value'],
}
TINYMCE_ALLOWED_STYLES = ['width', 'height']

FEINCMS_RICHTEXT_INIT_CONTEXT  = {
   'TINYMCE_JS_URL': TINYMCE_JS_URL,
   'TINYMCE_CONTENT_CSS_URL':  MEDIA_URL +"css/style_tinymce.css",
   'TINYMCE_LINK_LIST_URL': None
}

#URL_FILEBROWSER_MEDIA = '%sfilebrowser/' % (STATIC_URL)
#FILEBROWSER_URL_FILEBROWSER_MEDIA = '%sfilebrowser/' % (STATIC_URL)
#FILEBROWSER_URL_WWW = '%suploads/' % (MEDIA_URL)
#FILEBROWSER_URL_TINYMCE = TINYMCE_JS_ROOT
FILEBROWSER_DIRECTORY = 'uploads/'
# A list of Images to generate in the format (prefix, image width).
FILEBROWSER_IMAGE_GENERATOR_LANDSCAPE = [('500px_width_', 500), ('230px_width_', 230),]

# A list of Images to generate in the format (prefix, image width).
FILEBROWSER_IMAGE_GENERATOR_PORTRAIT = [('500px_width_', 500), ('230px_width_', 230),]

# A list of Images to generate in the format (prefix, image width, image height).
FILEBROWSER_IMAGE_CROP_GENERATOR = []

#FILEBROWSER_EXTENSIONS = {
#    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
#    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
#    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
#    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p']
#}
#FILEBROWSER_SELECT_FORMATS = {
#    'File': ['Folder','Image','Document','Video','Audio'],
#    'Image': ['Image'],
#    'Document': ['Document'],
#    'Media': ['Video','Audio'],
#}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s [%(pathname)s:%(lineno)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'django_log': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../logs/django.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_log'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Do not put any settings below this line
try:
    from local_settings import *
except:
    pass

if DEBUG and DEBUG_TOOLBAR:
    # debug_toolbar
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
	)

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
