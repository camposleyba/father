# Generated by Django 4.1.3 on 2023-08-03 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0004_votados_foto'),
    ]

    operations = [
        migrations.DeleteModel(
            name='nominados',
        ),
    ]