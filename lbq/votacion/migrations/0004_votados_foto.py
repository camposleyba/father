# Generated by Django 4.1.3 on 2023-08-03 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votacion', '0003_categorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='votados',
            name='foto',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]