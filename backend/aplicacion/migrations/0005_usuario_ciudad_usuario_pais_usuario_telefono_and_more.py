# Generated by Django 4.1.6 on 2023-11-25 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0004_rename_materialnoc_estanquematnoc_materialnoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='ciudad',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='pais',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='usuario',
            field=models.CharField(default=False, max_length=100),
        ),
    ]
