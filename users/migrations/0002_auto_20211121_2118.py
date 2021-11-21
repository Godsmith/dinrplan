# Generated by Django 3.2.9 on 2021-11-21 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_week_offset",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="number_of_weeks_to_show",
            field=models.PositiveSmallIntegerField(default=2),
        ),
    ]