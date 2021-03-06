# Generated by Django 3.2.9 on 2021-11-17 19:02
import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0004_auto_20211114_2041"),
    ]

    operations = [
        migrations.AddField(
            model_name="meal",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="meal",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="meal",
            name="ingredients",
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name="meal",
            name="steps",
            field=models.TextField(blank=True, max_length=10000),
        ),
    ]
