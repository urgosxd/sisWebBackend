# Generated by Django 5.0.1 on 2024-02-22 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0020_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 22, 16, 31, 33, 483278, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('administrator', 'Administrator'), ('ventas', 'Ventas'), ('operaciones', 'Operaciones')], max_length=30),
        ),
    ]
