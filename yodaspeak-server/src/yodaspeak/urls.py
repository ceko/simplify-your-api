try:
    from . import api
except ImportError:
    api = None

from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path(r'api/auth/', include('rest_framework.urls')),
    path(r'', lambda _: HttpResponse("Welcome to the server, <a href='/api/'>the API is this way.</a>"))
]

if api and hasattr(api, 'urlpatterns'):
    urlpatterns += [path(r'api/', include(getattr(api, 'urlpatterns', [])))]