# Generated by Django 3.2 on 2023-11-20 05:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]