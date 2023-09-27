from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from empresa.models import Empresa, Tecnologias, Vagas


class NovaVagaTeste(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='teste',
            password='1234Abcd!'
        )

        self.empresa = Empresa.objects.create(
            usuario=self.user,
            nome='Minha Empresa',
        )

        self.tecnologia = Tecnologias.objects.create(
            tecnologia='Python'
        )

        self.client.login(username='teste', password='1234Abcd!')
        self.valores = {
            'usuario': self.user,
            'titulo': 'Vaga de teste',
            'nivel_experiencia': 'P',
            'data_final': '2024-01-01',
            'email': 'teste@email.com',
            'status': 'C',
        }
        self.valores['empresa'] = self.empresa

        self.vaga = Vagas.objects.create(**self.valores)
        self.vaga.tecnologias_dominadas.add(self.tecnologia)

    def teste_nova_vaga_cadastrada_com_sucesso(self):
        for campo, valor in self.valores.items():
            with self.subTest(campo=campo):
                self.assertEqual(getattr(self.vaga, campo), valor)

        self.assertEqual(self.vaga.tecnologias_dominadas.count(), 1)
        self.assertEqual(self.vaga.tecnologias_estudar.count(), 0)

    def teste_nova_vaga_cadastro_invalido(self):
        valores = {
            'titulo': ' ',
            'nivel_experiencia': ' ',
            'data_final': ' ',
            'email': ' ',
            'status': ' ',
        }

        for campo, valor in valores.items():
            with self.subTest(campo=campo):
                self.assertNotEqual(getattr(self.vaga, campo), valor)

    def teste_nova_nao_aceita_requisicao_get(self):
        response = self.client.get(reverse('nova_vaga'))
        self.assertEqual(response.status_code, 405)
