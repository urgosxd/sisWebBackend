# Generated by Django 5.0.1 on 2024-02-05 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 16, 5, 22, 613533, tzinfo=datetime.timezone.utc)),
        ),
    ]
