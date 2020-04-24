"""CLOG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.regist),
    path('login/', views.login),
    path('teacher_new/', views.teacher_new),
    path('LR_t/', views.LR_t),
    path('grade_t/', views.grade_t),
    path('feedback_t/', views.feedback_t),

    path('student_new/', views.student_new),
    path('ER_s/', views.ER_s),
    path('LR_s/', views.LR_s),
    path('grade_s/', views.grade_s),
    path('feedback_s/', views.feedback_s),
]

