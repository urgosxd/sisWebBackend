# Generated by Django 5.0.1 on 2024-02-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_rename_precionino_tren_precioninio'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='drive',
            field=models.CharField(default='url', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurante',
            name='drive',
            field=models.CharField(default='url', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='drive',
            field=models.CharField(default='url', max_length=250),
            preserve_default=False,
        ),
    ]
