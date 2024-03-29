from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from empresa.models import Empresa, Tecnologias, Vagas

from .models import Emails, Tarefas


class NovaVagaTeste(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='teste',
            password='1234Abcd!'
        )

        self.image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        self.empresa = Empresa.objects.create(
            nome='Minha Empresa',
            logo=self.image,
            usuario=self.user,
            email='empresa@teste.com',
            cidade='Minha Cidade',
            endereco='Rua da Empresa',
            caracteristica_empresa='Descrição da Empresa',
            nicho_mercado='T',
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
        self.valores['empresa'] = Empresa.objects.get(id=self.empresa.id)

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

    def teste_nova_vaga_nao_aceita_requisicao_get(self):
        response = self.client.get(reverse('nova_vaga'))
        self.assertEqual(response.status_code, 405)

    def teste_nova_vaga_mensagem_de_sucesso(self):
        valores = {
            'titulo': 'Vaga de Teste',
            'email': 'test@example.com',
            'experiencia': 'P',
            'data_final': '2023-12-31',
            'empresa': self.empresa.id,
            'status': 'C',
        }
        self.vaga.tecnologias_dominadas.add(self.tecnologia)
        response = self.client.post(
            reverse('nova_vaga'), data=valores, follow=True
        )
        mensagem = list(response.wsgi_request._messages)
        self.assertEqual(mensagem[0].message, 'Vaga criada com sucesso.')

    def teste_nova_vaga_retorna_status_code_200(self):
        valores = {
            'titulo': 'Vaga de Teste',
            'email': 'test@example.com',
            'experiencia': 'P',
            'data_final': '2023-12-31',
            'empresa': self.empresa.id,
            'status': 'C',
        }
        self.vaga.tecnologias_dominadas.add(self.tecnologia)
        response = self.client.post(
            reverse('nova_vaga'), data=valores, follow=True
        )
        self.assertEqual(response.status_code, 200)

    def teste_NovaVaga_redireciona_para_login_se_nao_estiver_autenticado(self):
        self.client.logout()
        response = self.client.post(
            reverse('nova_vaga'), data=self.valores, follow=True
        )
        self.assertTemplateUsed(response, 'login_e_cadastro.html')


class VagaTeste(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='teste',
            password='1234Abcd!'
        )

        self.image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        self.empresa = Empresa.objects.create(
            nome='Minha Empresa',
            logo=self.image,
            usuario=self.user,
            email='empresa@teste.com',
            cidade='Minha Cidade',
            endereco='Rua da Empresa',
            caracteristica_empresa='Descrição da Empresa',
            nicho_mercado='T',
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
        self.valores['empresa'] = Empresa.objects.get(id=self.empresa.id)

        self.vaga = Vagas.objects.create(**self.valores)
        self.vaga.tecnologias_dominadas.add(self.tecnologia)

    def teste_vaga_retorna_status_code_200(self):
        response = self.client.get(reverse('vaga', args=[self.vaga.id]))
        self.assertEqual(response.status_code, 200)

    def teste_vaga_nao_aceita_requisicao_post(self):
        response = self.client.post(reverse('vaga', args=[self.vaga.id]))
        self.assertEqual(response.status_code, 405)

    def teste_vaga_redireciona_para_login_se_nao_estiver_autenticado(self):
        self.client.logout()
        response = self.client.get(
            reverse('vaga', args=[self.vaga.id]), follow=True
        )
        self.assertTemplateUsed(response, 'login_e_cadastro.html')

    def teste_vaga_view_carrega_template_vaga(self):
        response = self.client.get(
            reverse('vaga', args=[self.vaga.id]), follow=True
        )
        self.assertTemplateUsed(response, 'vaga.html')

    def teste_vaga_com_tarefa(self):
        tarefa = Tarefas.objects.create(
            vaga=self.vaga,
            titulo='Tarefa de teste',
            prioridade='U',
            data='2023-01-01',
        )
        response = self.client.get(
            reverse('vaga', args=[self.vaga.id]), follow=True
        )
        self.assertEqual(response.context['tarefas'][0], tarefa)

    def teste_vaga_com_email(self):
        email = Emails.objects.create(
            vaga=self.vaga,
            assunto='Assunto de teste',
            corpo='Corpo de teste',
            enviado=True,
        )
        response = self.client.get(
            reverse('vaga', args=[self.vaga.id]), follow=True
        )
        self.assertEqual(response.context['emails'][0], email)

    def teste_vaga_nao_existe(self):
        response = self.client.get(
            reverse('vaga', args=[self.vaga.id + 1]), follow=True
        )
        mensagem = list(response.wsgi_request._messages)
        self.assertEqual(mensagem[0].message, 'Vaga não encontrada.')
