# Generated by Django 4.1.3 on 2023-04-05 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='award',
            old_name='title',
            new_name='award_category',
        ),
        migrations.RenameField(
            model_name='award',
            old_name='monto',
            new_name='monto_bp',
        ),
        migrations.RemoveField(
            model_name='award',
            name='created',
        ),
        migrations.RemoveField(
            model_name='award',
            name='rendido',
        ),
        migrations.AddField(
            model_name='award',
            name='monto_cash',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
