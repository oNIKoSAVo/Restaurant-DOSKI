# Generated by Django 3.2.3 on 2021-08-31 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_menue_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menue',
            name='image',
            field=models.ImageField(blank=True, default='images/product.jpg', null=True, upload_to='images/', verbose_name='Изображение'),
        ),
    ]