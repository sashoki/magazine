from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^login/', 'loginsys.views.login', name='login'),
    url(r'^logout/', 'loginsys.views.logout', name='logout'),
    url(r'^register/', 'loginsys.views.register', name='register'),


]