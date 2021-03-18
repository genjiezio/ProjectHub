from django.urls import path, re_path

from padmin.views import *

app_name = 'padmin'
urlpatterns = [
    re_path(r'get_csrf_token$', get_csrf_token),
]
