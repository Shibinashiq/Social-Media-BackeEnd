# Generated by Django 5.0.2 on 2024-04-15 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='content',
        ),
        migrations.AddField(
            model_name='story',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='story_images/'),
        ),
        migrations.AddField(
            model_name='story',
            name='text_content',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='story_videos/'),
        ),
    ]
