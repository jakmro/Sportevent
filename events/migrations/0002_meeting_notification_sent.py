# Generated by Django 5.0.3 on 2024-05-12 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='notification_sent',
            field=models.BooleanField(default=False),
        ),
    ]
