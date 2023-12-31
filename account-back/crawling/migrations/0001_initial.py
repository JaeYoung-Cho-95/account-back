# Generated by Django 3.2 on 2023-12-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('img_url', models.TextField(default=None)),
                ('news_url', models.TextField(default=None)),
            ],
        ),
    ]
