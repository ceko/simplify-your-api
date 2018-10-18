from yodaspeak.default_settings import *


# Allow websites from other domains to access your API
CORS_ORIGIN_ALLOW_ALL = True

# Register our app and dependencies as discoverable Django apps, this tells Django
# that these packages contain some Django hooks, like model migrations.
INSTALLED_APPS += (
    'yodaspeak',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
)

# Middleware allows you to operate on the request and response globally, in this case
# the CORS middleware will apply our CORS_* rules for us.
MIDDLEWARE += (
    'corsheaders.middleware.CorsMiddleware',
)

# Django Rest Framework configuration elements are contained in
# this dictionary.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    #    'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    #'DEFAULT_THROTTLE_CLASSES': (
    #    'rest_framework.throttling.AnonRateThrottle',
    #    'rest_framework.throttling.UserRateThrottle'
    #),
    #'DEFAULT_THROTTLE_RATES': {
    #    'anon': '100/day',
    #    'user': '100/min'
    #},
    #'PAGE_SIZE': 100
}