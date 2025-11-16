from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accueil/', views.cached_home, name='cached_home'),
    path('projets/', views.projects, name='projects'),
    path('projets/<slug:slug>/', views.project_detail, name='project_detail'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cv/', views.download_cv, name='download_cv'),
    
    # Dashboard et administration
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
    path('api/message/<int:message_id>/read/', views.mark_message_read, name='mark_message_read'),
]