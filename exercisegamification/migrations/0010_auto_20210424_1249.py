# Generated by Django 3.1.7 on 2021-04-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercisegamification', '0009_auto_20210424_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='reach_date',
            field=models.DateTimeField(verbose_name='reach date'),
        ),
    ]
