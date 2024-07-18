from django.shortcuts import render, redirect
from .models import ClanMembers, WarAttacks
import requests
import os
# Create your views here.

api_key = os.getenv('API_KEY')
clan_tag = "2G8YV0J02"
def members_page(request):
    members_list = ClanMembers.objects.all()
    return render(request, 'clan/clan_members_details.html', {'members': members_list})

def refresher():
    fetch_members = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/members", headers={'Authorization': f"Bearer {api_key}"})
    members = fetch_members.json()
    for member in members['items']:
        tag = member['tag']
        member_exist  = ClanMembers.objects.filter(member_tag=tag).exists()
        if not member_exist:
            new_member = ClanMembers(member_tag=member['tag'], member_name=member['name'], trophies=member['trophies'], tracked_stars=0)
            new_member.save()
        else:
            m = ClanMembers.objects.filter(member_tag=tag).first()
            m.trophies = member['trophies']
            m.save()

    war_endpoint = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar"
    war = requests.get(war_endpoint, headers={'Authorization': f"Bearer {api_key}"})
    war = war.json()

    clan_members = ClanMembers.objects.all()
    for member in clan_members:
        member.participating_in_current_war = False
        member.save()
    
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
            m.participating_in_current_war = True
            m.save()
    elif war['state'] == "preparation":
        for member in war['clan']['members']:
            tag = member['tag']
            m = ClanMembers.objects.filter(member_tag=tag).first()
            if not m:
                player_details = requests.get(f"https://api.clashofclans.com/v1/players/%23{tag}", headers={'Authorization': f"Bearer {api_key}"})
                if player_details.status_code != 200:
                    print(player_details.json())
                    continue
                player_details = player_details.json()
                m = ClanMembers.objects.create(member_tag=tag, member_name=player_details['name'], trophies=player_details['trophies'], tracked_stars=0, participating_in_current_war=False)
            m.participating_in_current_war = True
            m.attacked_in_current_war = False
            m.stars_in_current_war = 0
            m.save()

def refresh_stars(request):
    refresher()
    return redirect(request.META.get('HTTP_REFERER'))


def current_war(request):
    members = ClanMembers.objects.filter(participating_in_current_war=True)
    total_attacks = 0
    total_stars = 0
    attacking_members = 0
    for member in members:
        total_attacks += member.stars_in_current_war
        total_stars += member.tracked_stars
        if member.attacked_in_current_war:
            attacking_members += 1
    context = {
        'total_attacks': total_attacks,
        'total_stars': total_stars,
        'attacking_members': attacking_members,
        'members': members
    }
    return render(request, 'clan/current_war_details.html', context)