# Generated by Django 5.1.3 on 2024-11-22 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='roster_lineup',
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_schedule',
        ),
    ]
