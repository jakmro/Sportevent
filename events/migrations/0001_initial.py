# Generated by Django 5.0.3 on 2024-04-27 08:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facilities', '0003_alter_facility_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField()),
                ('sport_type', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('is_cyclic', models.BooleanField()),
                ('max_people_no', models.IntegerField()),
                ('min_people_no', models.IntegerField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.facility')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
