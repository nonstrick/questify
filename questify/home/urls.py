from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    path('test/', views.test_view, name='test'),
    path('test/chat/', views.test_chat_view, name='test_chat'),
    path('test/reset/', views.test_reset_view, name='test_reset'),
    path('community/', views.community_view, name='community'),
]
