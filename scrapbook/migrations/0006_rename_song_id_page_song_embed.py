# Generated by Django 4.0 on 2022-07-27 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbook', '0005_page_vid_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='song_id',
            new_name='song_embed',
        ),
    ]
