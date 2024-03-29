from django.contrib.auth.models import User
from django.db import models


class Tecnologias(models.Model):
    tecnologia = models.CharField(max_length=30)

    def __str__(self):
        return self.tecnologia


class Empresa(models.Model):
    choices_nicho_mercado = (
        ('M', 'Marketing'),
        ('SF', 'Setor Financeiro'),
        ('T', 'Tecnologia'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logo_empresa', null=True, blank=True)
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    cidade = models.CharField(max_length=30)
    tecnologias = models.ManyToManyField(Tecnologias)
    endereco = models.CharField(max_length=30)
    caracteristica_empresa = models.TextField()
    nicho_mercado = models.CharField(
        max_length=3, choices=choices_nicho_mercado
    )

    def qtd_vagas(self):
        return Vagas.objects.filter(empresa__id=self.id).count()

    def __str__(self):
        return self.nome


class Vagas(models.Model):
    choices_experiencia = (
        ('J', 'Júnior'),
        ('P', 'Pleno'),
        ('S', 'Sênior')
    )

    choices_status = (
        ('I', 'Interesse'),
        ('C', 'Currículo enviado'),
        ('E', 'Entrevista'),
        ('D', 'Desafio técnico'),
        ('F', 'Finalizado')
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    titulo = models.CharField(max_length=30)
    nivel_experiencia = models.CharField(
        max_length=2, choices=choices_experiencia
    )
    data_final = models.DateField()
    email = models.EmailField(null=True)
    status = models.CharField(max_length=30, choices=choices_status)
    tecnologias_dominadas = models.ManyToManyField(Tecnologias)
    tecnologias_estudar = models.ManyToManyField(
        Tecnologias, related_name='estudar'
    )

    def progresso(self):
        porcentagem = [((i+1) * 20, j[0]) for i, j in enumerate(self.choices_status)]
        porcentagem = list(filter(lambda x: x[1] == self.status, porcentagem))[0][0]
        return porcentagem

    def __str__(self):
        return self.titulo
