# Generated by Django 4.0 on 2023-11-05 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_categoriarefeicao_planificacao_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
    ]
