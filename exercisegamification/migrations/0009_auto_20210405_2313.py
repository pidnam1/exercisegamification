# Generated by Django 3.1.6 on 2021-04-06 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercisegamification', '0008_auto_20210405_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercisegamification.profile'),
        ),
    ]
