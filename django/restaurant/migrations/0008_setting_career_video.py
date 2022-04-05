# Generated by Django 3.2.9 on 2022-03-11 19:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_auto_20220305_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='career_video',
            field=models.FileField(blank=True, null=True, upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'mp4', 'avi', 'ogg', 'webm'])], verbose_name='Видео на странице карьеры'),
        ),
    ]