# Generated by Django 3.2.3 on 2021-05-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210521_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/default_profile_picture.png', null=True, upload_to='static/images/profiles'),
        ),
    ]