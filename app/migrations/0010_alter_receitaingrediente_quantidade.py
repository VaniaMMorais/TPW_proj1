# Generated by Django 4.0 on 2023-11-07 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receitaingrediente',
            name='quantidade',
            field=models.FloatField(default=1.0),
        ),
    ]
