from django.db import models

# Create your models here.

class ClanMembers(models.Model):
    member_tag = models.CharField(max_length=50)
    member_name = models.CharField(max_length=50)
    trophies = models.IntegerField()
    tracked_stars = models.IntegerField(default=0)
    attacked_in_current_war = models.BooleanField(default=False)
    stars_in_current_war = models.IntegerField(default=0)
    participating_in_current_war = models.BooleanField(default=False)
    attacks_used = models.IntegerField(default=0)
    total_war_attacks = models.IntegerField(default=0)

class WarAttacks(models.Model):
    attacker_tag = models.CharField(max_length=50)
    defender_tag = models.CharField(max_length=50)
    stars = models.IntegerField()