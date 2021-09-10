# Generated by Django 3.2.3 on 2021-09-08 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0014_auto_20210908_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('second_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('birthday', models.DateField(blank=True, default=None, null=True)),
                ('phone', models.CharField(blank=True, default=None, max_length=16, null=True)),
                ('registration_ip', models.GenericIPAddressField(default='192.168.0.1')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
    ]