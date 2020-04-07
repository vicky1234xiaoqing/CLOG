from django.contrib import admin
from django.urls import path
from online import views

urlpatterns = [
    path('', views.login, name = 'login'),
    path('login/', views.login, name = 'regist'),
    path('regist/', views.regist, name = 'regist'),
    path('index/', views.index, name = 'index'),
    path('logout/', views.logout, name = 'logout'),
]
