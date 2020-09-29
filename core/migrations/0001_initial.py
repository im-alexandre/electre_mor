# Generated by Django 3.1 on 2020-09-29 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Criterio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('numerico', models.BooleanField(default=False)),
                ('monotonico', models.IntegerField(choices=[(1, 'lucro'), (2, 'custo')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('descricao', models.TextField(blank=True, max_length=400)),
                ('qtde_classes', models.IntegerField(default=2, null=True)),
                ('lamb', models.FloatField(default=0.5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Decisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('projeto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='CriterioParametro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p', models.FloatField()),
                ('q', models.FloatField()),
                ('v', models.FloatField()),
                ('criterio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.criterio')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.AddField(
            model_name='criterio',
            name='projeto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.projeto'),
        ),
        migrations.CreateModel(
            name='AvaliacaoCriterios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(null=True)),
                ('criterioA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterioA', to='core.criterio')),
                ('criterioB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterioB', to='core.criterio')),
                ('decisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.decisor')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='AvaliacaoAlternativas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(null=True)),
                ('alternativaA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternativaA', to='core.alternativa')),
                ('alternativaB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternativaB', to='core.alternativa')),
                ('criterio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.criterio')),
                ('decisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.decisor')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='AlternativaCriterio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.FloatField(null=True)),
                ('alternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternativa', to='core.alternativa')),
                ('criterio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio', to='core.criterio')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.AddField(
            model_name='alternativa',
            name='projeto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.projeto'),
        ),
    ]
