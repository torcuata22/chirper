# Generated by Django 4.2.6 on 2023-11-20 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chirper', '0005_chirp_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='homepage_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
