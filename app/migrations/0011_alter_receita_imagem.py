# Generated by Django 4.0 on 2023-11-11 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_receitaingrediente_quantidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receita',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='media/static/img/receitas-img'),
        ),
    ]
