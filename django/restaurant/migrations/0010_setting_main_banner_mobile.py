# Generated by Django 3.2.9 on 2022-03-31 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_auto_20220318_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='main_banner_mobile',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Баннер на главной странице в мобильной версии'),
        ),
    ]
