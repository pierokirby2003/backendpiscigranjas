# Generated by Django 4.1.6 on 2023-11-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0008_empresas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='usuario',
            field=models.CharField(default='0000', max_length=100),
        ),
    ]
