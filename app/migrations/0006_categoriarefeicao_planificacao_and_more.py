# Generated by Django 4.0 on 2023-11-05 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0005_receita_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaRefeicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Planificacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.categoriarefeicao')),
                ('receita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.receita')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.RenameModel(
            old_name='ReceitasListaCompras',
            new_name='ListaCompras',
        ),
        migrations.DeleteModel(
            name='ReceitasPlanificacao',
        ),
    ]
