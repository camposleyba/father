# Generated by Django 3.2.7 on 2021-09-14 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager', models.CharField(blank=True, max_length=200)),
                ('developer', models.CharField(blank=True, max_length=200)),
                ('tot_bots', models.IntegerField(default=0)),
                ('tot_hours', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
            ],
        ),
    ]
