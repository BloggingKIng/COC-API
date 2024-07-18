from django.shortcuts import render, redirect
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

def refresh_stars(request):
    war_endpoint = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar"
    war = requests.get(war_endpoint, headers={'Authorization': f"Bearer {api_key}"})
    war = war.json()
    if war['state'] == "inWar":
        for member in war['clan']['members']:
            tag = member['tag']
            m = ClanMembers.objects.filter(member_tag=tag).first()
            if not m:
                player_details = requests.get(f"https://api.clashofclans.com/v1/players/%23{tag}", headers={'Authorization': f"Bearer {api_key}"})
                if player_details.status_code != 200:
                    print(player_details.json())
                    continue
                player_details = player_details.json()
                m = ClanMembers.objects.create(member_tag=tag, member_name=player_details['name'], trophies=player_details['trophies'], tracked_stars=0)
            try:
                stars_ = 0
                attacks = member['attacks']
                for attack in attacks:
                    attacker_tag = attack['attackerTag']
                    defender_tag = attack['defenderTag']
                    stars = attack['stars']
                    attack_exist = WarAttacks.objects.filter(attacker_tag=attacker_tag, defender_tag=defender_tag, stars=stars).exists()
                    if attack_exist:
                        pass
                    else:
                        new_attack = WarAttacks(attacker_tag=attacker_tag, defender_tag=defender_tag, stars=stars)
                        new_attack.save()
                        m.tracked_stars += stars
                    stars_ += stars
                m.stars_in_current_war = stars_
                m.attacked_in_current_war = True
                m.save()
            except KeyError:
                m.attacked_in_current_war = False
                m.stars_in_current_war = 0
                m.save()

    return redirect('clan_members_page')
