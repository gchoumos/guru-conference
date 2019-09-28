from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detectGuru', views.detect_guru, name='Detect Guru'),
]