# Generated by Django 5.0.1 on 2024-02-19 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0003_alter_notification_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='ppe',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='pve',
            field=models.DecimalField(decimal_places=2, default='100', max_digits=8),
            preserve_default=False,
        ),
    ]