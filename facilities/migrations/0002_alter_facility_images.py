# Generated by Django 5.0.3 on 2024-04-07 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='images',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]