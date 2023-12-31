# Generated by Django 3.2 on 2023-11-29 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0007_alter_tagmodel_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('spending', models.DecimalField(decimal_places=0, default=0, max_digits=11)),
                ('incomde', models.DecimalField(decimal_places=0, default=0, max_digits=11)),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.tagmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
