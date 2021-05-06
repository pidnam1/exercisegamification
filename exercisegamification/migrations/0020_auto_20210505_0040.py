# Generated by Django 3.1.7 on 2021-05-05 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercisegamification', '0019_pointachievement_icon_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointachievement',
            name='icon_name',
        ),
        migrations.AddField(
            model_name='pointachievement',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='achievements/'),
        ),
    ]
