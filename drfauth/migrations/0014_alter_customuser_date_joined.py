# Generated by Django 5.0.1 on 2024-02-08 22:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0013_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 8, 22, 38, 53, 779806, tzinfo=datetime.timezone.utc)),
        ),
    ]