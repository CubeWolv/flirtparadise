# Generated by Django 5.1.4 on 2025-01-11 17:28

import gender.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gender', '0009_blogpost_remove_guy_habits_remove_girl_habits_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default=gender.models.slug_default, unique=True),
        ),
    ]
