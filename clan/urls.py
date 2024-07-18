from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.members_page, name='clan_members_page'),
    path('refresh_stars/', views.refresh_stars, name='refresh_stars'),
    path('current_war_details/', views.current_war, name='current_war_details'),
]