from django.conf.urls import url
from . import views
from .views import CuponApply


urlpatterns = [
    url(r'^apply', views.CuponApply, name='apply')
]