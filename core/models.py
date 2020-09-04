from django.contrib.postgres.fields import JSONField
from django.db import models
from django_pandas.managers import DataFrameManager


class Decisor(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=400, blank=True)
    decisores = models.ManyToManyField('Decisor', related_name='+')
    avaliado = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.nome


class Alternativa(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)

    # TODO imagem na alternativa
    # imagem = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.jpg')

    def __str__(self):
        return self.nome


class Criterio(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)
    numerico = models.BooleanField(default=False)

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


class PageView(models.Model):
    views = models.IntegerField()
