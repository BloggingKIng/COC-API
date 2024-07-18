from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.members_page, name='clan_members_page'),
    path('refresh_stars/', views.refresh_stars, name='refresh_stars'),
]