# Generated by Django 4.2.6 on 2023-11-23 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_rename_familiamaterial_materialnocivo_familiamaterial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estanquematnoc',
            old_name='materialNoc',
            new_name='materialnoc',
        ),
    ]
