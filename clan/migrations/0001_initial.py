# Generated by Django 5.0.7 on 2024-07-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClanMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_tag', models.CharField(max_length=50)),
                ('member_name', models.CharField(max_length=50)),
                ('trophies', models.IntegerField()),
                ('tracked_stars', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WarAttacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attacker_tag', models.CharField(max_length=50)),
                ('defender_tag', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
            ],
        ),
    ]
