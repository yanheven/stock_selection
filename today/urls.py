"""today URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^today/', views.get, name='get'),
    url(r'^tomorrow/', views.get_tomorrow, name='get_tomorrow'),
    url(r'^yestoday/', views.get_yestoday, name='get_yestoday'),
    url(r'^report/', views.get_report, name='get_report'),
    url(r'^test/', views.test, name='test'),
]
