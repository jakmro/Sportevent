# Generated by Django 5.0.3 on 2024-04-25 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='facility',
            unique_together={('latitude', 'longitude')},
        ),
    ]
