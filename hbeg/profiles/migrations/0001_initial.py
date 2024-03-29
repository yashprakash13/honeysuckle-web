# Generated by Django 3.2.4 on 2021-07-08 12:46

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_id', models.CharField(max_length=30)),
                ('story_name', models.CharField(max_length=100)),
                ('author_name', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=100)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Stories',
                'ordering': ['-added_on'],
            },
        ),
        migrations.CreateModel(
            name='StoryRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(blank=True, choices=[('O', 'Outstanding'), ('E', 'Exceeds Expectations'), ('A', 'Acceptable'), ('P', 'Poor'), ('D', 'Dreadful'), ('T', 'Troll')], max_length=50, null=True)),
                ('story_id', models.CharField(max_length=30)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StoryRating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StoryContrib',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('is_accepted', models.BooleanField(default=False)),
                ('given_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StoryContrib', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('is_author', models.BooleanField(choices=[(True, 'Yes,I am.'), (False, 'Nope.')], default=False)),
                ('ffn_url', models.CharField(blank=True, max_length=100, null=True)),
                ('story_contribs', models.PositiveIntegerField(default=0)),
                ('story_referrals', models.PositiveIntegerField(default=0)),
                ('is_early_adopter', models.BooleanField(default=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=120)),
                ('folder_desc', models.TextField(blank=True, null=True)),
                ('is_visible', models.BooleanField(choices=[(True, 'Visible'), (False, 'Invisible')], default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Folders', to=settings.AUTH_USER_MODEL)),
                ('story', models.ManyToManyField(blank=True, null=True, to='profiles.Story')),
            ],
            options={
                'verbose_name_plural': 'Folders',
                'ordering': ['-created_at'],
            },
        ),
    ]
