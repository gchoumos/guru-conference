from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detectGuru/', views.detect_guru_no_spec, name='Detect Guru'),
    path('detectGuru/<project>/', views.detect_team_guru, name='Detect Guru Team'),
    path('detectGuru/<project>/results/', views.results, name='Guru Results'),
]
