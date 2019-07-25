from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # url(r'^',views.register, name='register'),
    url(r'^$',views.index, name='index'),
    url(r'^(?P<product_id>[0-9]+)/$',views.detail,name= 'detail'),
    url(r'^(?P<product_id>[0-9]+)/added$',views.addInCart,name='addInCart'),
    url(r'^(?P<product_id>[0-9]+)/removed$',views.remove,name='remove'),
	path('register/', views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='shop/logout.html'), name = 'logout'),
    path('filter/', views.filter, name='filter'),
]
# template_name denoted that take this file as base for login
