# Generated by Django 5.0.1 on 2024-02-17 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfauth', '0014_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('administrator', 'Administrator'), ('ventas', 'Ventas'), ('operaciones', 'Operaciones')], default='administrator', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 23, 10, 6, 773259, tzinfo=datetime.timezone.utc)),
        ),
    ]
