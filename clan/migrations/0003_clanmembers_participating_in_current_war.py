# Generated by Django 5.0.7 on 2024-07-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clan', '0002_clanmembers_attacked_in_current_war_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clanmembers',
            name='participating_in_current_war',
            field=models.BooleanField(default=False),
        ),
    ]
