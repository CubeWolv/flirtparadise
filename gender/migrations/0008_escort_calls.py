# Generated by Django 5.1.4 on 2025-01-09 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gender', '0007_rename_vip_escort_premium_escort_is_new_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='escort',
            name='calls',
            field=models.CharField(default='Fair', max_length=20),
        ),
    ]