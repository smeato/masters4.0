# Generated by Django 4.0 on 2022-08-09 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='has_scrapbook',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='shares_scrapbook',
            field=models.BooleanField(default=False),
        ),
    ]
