# Generated by Django 4.1.3 on 2023-02-09 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0006_alter_todo_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='category',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
