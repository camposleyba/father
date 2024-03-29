# Generated by Django 4.1.3 on 2023-07-21 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='images')),
                ('band', models.CharField(max_length=2)),
                ('pmr', models.DecimalField(decimal_places=2, max_digits=4)),
                ('salary_increase_ytd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_monthly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='mid_exchrate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.CharField(max_length=2)),
                ('midpoint', models.DecimalField(decimal_places=2, max_digits=10)),
                ('exch_rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
