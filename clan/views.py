from django.shortcuts import render, redirect
from .models import ClanMembers, WarAttacks
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
# Create your views here.

api_key = os.getenv('API_KEY')
clan_tag = "2G8YV0J02"

status = "Loading ...."

def members_page(request):
    members_list = ClanMembers.objects.all().order_by('-tracked_stars')
    return render(request, 'clan/clan_members_details.html', {'members': members_list})

def refresher():
    print("Refreshing Data")
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
                        m.total_war_attacks += 1
                        print(f"{attacker_tag} -> {defender_tag} : {stars}")
                    stars_ += stars
                m.stars_in_current_war = stars_
                m.attacked_in_current_war = True
                m.attacks_used = len(attacks)
                m.participating_in_current_war = True
                m.save()
            except KeyError:
                m.attacked_in_current_war = False
                m.stars_in_current_war = 0
                m.attacks_used = 0
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
    print("Data Refreshed")

def refresh_stars(request):
    refresher()
    return redirect(request.META.get('HTTP_REFERER'))


def current_war(request):
    members = ClanMembers.objects.filter(participating_in_current_war=True).order_by('-stars_in_current_war')
    total_stars = 0
    attacking_members = 0
    for member in members:
        total_stars += member.stars_in_current_war
        if member.attacked_in_current_war:
            attacking_members += 1
    context = {
        'total_stars': total_stars,
        'attacking_members': attacking_members,
        'members': members,
        'status': status
    }
    return render(request, 'clan/current_war_details.html', context)

def refresh_status():
    global status
    war_endpoint = f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar"
    war = requests.get(war_endpoint, headers={'Authorization': f"Bearer {api_key}"})
    war = war.json()
    status = war['state']

def start():
    refresh_scheduler = BackgroundScheduler()
    refresh_scheduler.add_job(refresher, 'interval', minutes=10, next_run_time=datetime.now())
    refresh_scheduler.add_job(refresh_status, 'interval', minutes=30, next_run_time=datetime.now())
    refresh_scheduler.start()