# Generated by Django 4.0 on 2022-08-03 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapbook', '0007_rename_vid_id_page_vid_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image_file',
            field=models.FileField(blank=True, upload_to='page_images'),
        ),
    ]
