# Generated by Django 5.0.3 on 2024-03-16 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_apps', '0007_app_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='plan',
        ),
    ]
