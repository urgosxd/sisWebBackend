# Generated by Django 5.0.1 on 2024-02-08 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_alter_tour_lastaccessuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=300),
        ),
    ]
