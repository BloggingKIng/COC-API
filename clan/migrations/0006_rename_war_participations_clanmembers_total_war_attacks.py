# Generated by Django 5.0.7 on 2024-07-18 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0005_clanmembers_war_participations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clanmembers',
            old_name='war_participations',
            new_name='total_war_attacks',
        ),
    ]
