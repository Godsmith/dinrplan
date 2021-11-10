# Generated by Django 3.2.9 on 2021-11-06 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='meal',
            name='persons',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='meal',
            name='source',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='meal',
            name='steps',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AddField(
            model_name='meal',
            name='time',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]