# Generated by Django 3.2.7 on 2021-09-16 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='bot_nbr',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]