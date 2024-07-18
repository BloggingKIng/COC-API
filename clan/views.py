from django.shortcuts import render
from .models import ClanMembers, WarAttacks
import requests
import os
# Create your views here.

api_key = os.getenv('API_KEY')
clan_tag = "2G8YV0J02"
def members_page(request):
    fetch_members = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/members", headers={'Authorization': f"Bearer {api_key}"})
    members = fetch_members.json()
    for member in members['items']:
        tag = member['tag']
        member_exist  = ClanMembers.objects.filter(member_tag=tag).exists()
        if not member_exist:
            new_member = ClanMembers(member_tag=member['tag'], member_name=member['name'], trophies=member['trophies'], tracked_stars=0)
            new_member.save()
    members_list = ClanMembers.objects.all()
    
    return render(request, 'clan/clan_members_details.html', {'members': members_list})