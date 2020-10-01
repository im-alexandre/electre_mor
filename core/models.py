from django.contrib.postgres.fields import JSONField
from django.db import models
from django_pandas.managers import DataFrameManager


class Decisor(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'projeto'],
                                    name='unique_decisor')
        ]

    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=400)
    qtde_classes = models.IntegerField(null=False)
    lamb = models.FloatField(null=True, default=0.5)

    def __str__(self):
        return self.nome


class Alternativa(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'projeto'],
                                    name='unique_alternativa')
        ]

    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Criterio(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'projeto'],
                                    name='unique_criterio')
        ]

    escolhas = ((1, "lucro"), (2, "custo"))
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20, blank=False, null=False)
    numerico = models.BooleanField(default=False)
    monotonico = models.IntegerField(choices=escolhas, default=1)

    def __str__(self):
        return self.nome


class AvaliacaoCriterios(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    decisor = models.ForeignKey('Decisor', on_delete=models.CASCADE)
    criterioA = models.ForeignKey('Criterio',
                                  on_delete=models.CASCADE,
                                  related_name='criterioA')
    criterioB = models.ForeignKey('Criterio',
                                  on_delete=models.CASCADE,
                                  related_name='criterioB')
    nota = models.IntegerField(null=True)
    objects = DataFrameManager()


class AvaliacaoAlternativas(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    decisor = models.ForeignKey('Decisor', on_delete=models.CASCADE)
    criterio = models.ForeignKey('Criterio', on_delete=models.CASCADE)
    alternativaA = models.ForeignKey('Alternativa',
                                     on_delete=models.CASCADE,
                                     related_name='alternativaA')
    alternativaB = models.ForeignKey('Alternativa',
                                     on_delete=models.CASCADE,
                                     related_name='alternativaB')
    nota = models.IntegerField(null=True)

    objects = DataFrameManager()


class AlternativaCriterio(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    criterio = models.ForeignKey('Criterio',
                                 on_delete=models.CASCADE,
                                 related_name='criterio')
    alternativa = models.ForeignKey('Alternativa',
                                    on_delete=models.CASCADE,
                                    related_name='alternativa')

    nota = models.FloatField(null=True)

    objects = DataFrameManager()


class CriterioParametro(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    criterio = models.ForeignKey('Criterio', on_delete=models.CASCADE)
    p = models.FloatField()
    q = models.FloatField()
    v = models.FloatField()

    objects = DataFrameManager()
