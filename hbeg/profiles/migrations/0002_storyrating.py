# Generated by Django 3.2.3 on 2021-06-04 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(blank=True, choices=[('O', 'Outstanding'), ('E', 'Exceeds Expectations'), ('A', 'Acceptable'), ('P', 'Poor'), ('D', 'Dreadful'), ('T', 'Troll')], max_length=50, null=True)),
                ('story_id', models.CharField(max_length=30)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StoryRating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]