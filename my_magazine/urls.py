from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^products/get/(?P<product_id>\d+)/$', 'my_magazine.views.product', name='product'),
    url(r'^products/addlike/(?P<product_id>\d+)/$', 'my_magazine.views.addlike', name='addlike'),
    url(r'^products/addcomment/(?P<product_id>\d+)/$', 'my_magazine.views.addcomment', name='addcomment'),

    url(r'^page/(\d+)/$', 'my_magazine.views.products', name='products'),
    url(r'^category/get/(?P<category_id>\d+)/$', 'my_magazine.views.product_cat', name='product_cat'),
    url(r'^brands/$', 'my_magazine.views.brands', name='brands'),
    url(r'^keyword/$', 'my_magazine.views.keywords', name='keywords'),
    url(r'^author/(?P<id>\d+)/$', 'my_magazine.views.authors', name='authors'),
    url(r'^home/$', 'my_magazine.views.home', name='home'),

    url(r'^$', 'my_magazine.views.products', name='products'),
    ]