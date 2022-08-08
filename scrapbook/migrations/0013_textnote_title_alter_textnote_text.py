# Generated by Django 4.0 on 2022-08-07 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbook', '0012_remove_textnote_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='textnote',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textnote',
            name='text',
            field=models.TextField(max_length=10000),
        ),
    ]