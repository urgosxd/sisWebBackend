# Generated by Django 5.0.1 on 2024-03-05 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0028_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 5, 19, 15, 13, 666989, tzinfo=datetime.timezone.utc)),
        ),
    ]
