# Generated by Django 5.1.4 on 2025-01-08 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_date_profile_date_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_modified',
        ),
    ]
