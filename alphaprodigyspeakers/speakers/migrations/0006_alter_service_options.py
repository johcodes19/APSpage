# Generated by Django 5.1.4 on 2025-01-15 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0005_rename_preferences_profile_bio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['name']},
        ),
    ]
