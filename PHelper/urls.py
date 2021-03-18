"""PHelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic import TemplateView

import student.urls
import teacher.urls
import wechart.urls
import padmin.urls
from PHelper.views import *

admin.site.site_header = "PHelper Admin"
admin.site.site_title = "PHelper Admin Portal"
admin.site.index_title = "Welcome to PHelper Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('send/', send_email),
    re_path(r'^padmin_api/', include(padmin.urls, namespace='padmin')),
    re_path(r'^student_api/', include(student.urls, namespace='student')),
    re_path(r'^teacher_api/', include(teacher.urls, namespace='teacher')),
    re_path(r'^wechart_api/', include(wechart.urls, namespace='wechart')),
    re_path(r'^$', TemplateView.as_view(template_name="index.html"), name='login'),
    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
]
