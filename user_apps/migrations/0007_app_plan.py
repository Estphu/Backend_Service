# Generated by Django 5.0.3 on 2024-03-16 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_apps', '0006_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_apps.plan'),
        ),
    ]
