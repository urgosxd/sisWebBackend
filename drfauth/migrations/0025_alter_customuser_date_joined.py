# Generated by Django 5.0.1 on 2024-02-29 21:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0024_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 29, 21, 36, 28, 928119, tzinfo=datetime.timezone.utc)),
        ),
    ]
