# Generated by Django 5.0.4 on 2024-04-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
