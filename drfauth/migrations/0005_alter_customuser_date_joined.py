# Generated by Django 5.0.1 on 2024-02-07 14:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0004_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 7, 14, 57, 3, 262468, tzinfo=datetime.timezone.utc)),
        ),
    ]
