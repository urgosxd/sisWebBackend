# Generated by Django 5.0.1 on 2024-02-20 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0004_tour_ppe_tour_pve'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='figma',
            field=models.CharField(default='url', max_length=250),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('servicio', models.CharField(max_length=100)),
                ('pppAdulto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ppeAdulto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pppNinio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ppeNinio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pppInfante', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ppeInfante', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estudianteP', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estudianteE', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Guiado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicio', models.CharField(max_length=100)),
                ('idioma', models.CharField(max_length=100)),
                ('detalle', models.CharField(max_length=300)),
                ('ptapull', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ptbpull', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ptapriv', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ptbpriv', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('clase', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('telefonoRecepcion', models.CharField(max_length=100)),
                ('simple', models.DecimalField(decimal_places=2, max_digits=8)),
                ('doble', models.DecimalField(decimal_places=2, max_digits=8)),
                ('triple', models.DecimalField(decimal_places=2, max_digits=8)),
                ('horarioDesayuno', models.TimeField()),
                ('checkIn', models.TimeField()),
                ('checkOut', models.TimeField()),
                ('figma', models.CharField(max_length=250)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FichaTecnicaHotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Extension', models.CharField(max_length=40, null=True)),
                ('FileName', models.CharField(max_length=200, null=True)),
                ('Doc_Content', models.BinaryField(null=True)),
                ('Hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fichasTecnicas', to='crud.hotel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('especialidad', models.CharField(max_length=100)),
                ('tipoDeServicio', models.CharField(max_length=100)),
                ('horarioDeAtencion', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefonoReserva', models.CharField(max_length=100)),
                ('telefonoRecepcion', models.CharField(max_length=100)),
                ('precioMenu', models.DecimalField(decimal_places=2, max_digits=8)),
                ('precioMenuE', models.DecimalField(decimal_places=2, max_digits=8)),
                ('figma', models.CharField(max_length=250)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FichaTecnicaRestaurante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Extension', models.CharField(max_length=40, null=True)),
                ('FileName', models.CharField(max_length=200, null=True)),
                ('Doc_Content', models.BinaryField(null=True)),
                ('Restaurante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fichasTecnicas', to='crud.restaurante')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('servicio', models.CharField(max_length=100)),
                ('ppp', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ppe', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Traslado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('servicio', models.CharField(max_length=100)),
                ('tipoDeVehiculo', models.CharField(max_length=100)),
                ('ppp', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ppe', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('empresa', models.CharField(max_length=100)),
                ('ruta', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=100)),
                ('precioAdulto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('precioNino', models.DecimalField(decimal_places=2, max_digits=8)),
                ('precioInfante', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UpSelling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicioProducto', models.CharField(max_length=100)),
                ('detalle', models.CharField(max_length=300)),
                ('ppp', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ppe', models.DecimalField(decimal_places=2, max_digits=8)),
                ('lastAccessUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
