from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.members_page, name='clan_members_page'),
]