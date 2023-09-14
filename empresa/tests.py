from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Empresa


class LoginTeste(TestCase):
    def setUp(self):
        self.resposta = self.client.get(reverse('login'))

    def teste_login_view_retorna_status_code_200(self):
        self.assertEqual(self.resposta.status_code, 200)

    def teste_login_view_carrega_template_login(self):
        self.assertTemplateUsed(self.resposta, 'login_e_cadastro.html')

    def teste_login_view_conteudo_login(self):
        self.assertIn('login', self.resposta.content.decode('utf-8'))

    def test_login_view_nao_aceita_requisicao_post(self):
        resposta = self.client.post(reverse('login'), {})
        self.assertEqual(resposta.status_code, 405)


class ConfirmarCadastroTeste(TestCase):
    def setUp(self):
        self.resposta = self.client.post(reverse('confirmar_cadastro'))
        self.formulario = {
            'nome': 'teste',
            'email': 'teste@email.com',
            'senha': '1234Abcd!',
            'confirmar_senha': '1234Abcd!'
        }

    def teste_confirmar_cadastro_view_retorna_status_code_200(self):
        self.assertEqual(self.resposta.status_code, 200)

    def teste_confirmar_cadastro_view_carrega_template_login_e_cadastro(self):
        self.assertTemplateUsed(self.resposta, 'login_e_cadastro.html')

    def teste_confirmar_cadastro_view_nao_aceita_requisicao_get(self):
        resposta = self.client.get(reverse('confirmar_cadastro'), {})
        self.assertEqual(resposta.status_code, 405)

    def teste_confirmar_cadastro_valido(self):
        resposta = self.client.post(
            reverse('confirmar_cadastro'), self.formulario
        )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(
            mensagem[0].message, 'Cadastro realizado com sucesso!'
        )

    def teste_campo_nome_deve_ter_menos_de_100_caracteres(self):
        nome = 'a' * 101
        self.formulario['nome'] = nome
        resposta = self.client.post(
            reverse('confirmar_cadastro'), self.formulario
        )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(
            mensagem[0].message,
            f'Certifique-se de que o valor tenha no máximo 100 caracteres (ele possui {len(nome)}).'  # noqa: E501
        )

    def teste_campo_email_deve_ter_um_endereco_email_valido(self):
        self.formulario['email'] = 'teste@email'
        resposta = self.client.post(
            reverse('confirmar_cadastro'), self.formulario
        )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(
            mensagem[0].message, 'Informe um endereço de email válido.'
        )

    def teste_campos_senha_e_confirmar_senha_devem_ser_iguais(self):
        self.formulario['senha'] = '1234Abcd!'
        self.formulario['confirmar_senha'] = '1234Abcd!1'
        resposta = self.client.post(
            reverse('confirmar_cadastro'), self.formulario
        )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(
            mensagem[0].message, 'senha e confirmar senha não são iguais'
        )

    def teste_campo_email_deve_ser_unico(self):
        for _ in range(2):
            resposta = self.client.post(
                reverse('confirmar_cadastro'), self.formulario
            )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(mensagem[1].message, 'Email já existe')


class ConfirmarLoginTeste(TestCase):
    def setUp(self):
        self.resposta = self.client.post(reverse('confirmar_login'))

    def teste_confirmar_login_view_retorna_status_code_200(self):
        self.assertEqual(self.resposta.status_code, 200)

    def teste_confirmar_login_conteudo(self):
        self.assertIn('login', self.resposta.content.decode('utf-8'))

    def teste_confirmar_login_nao_aceita_requisicao_get(self):
        resposta = self.client.get(reverse('confirmar_login'), {})
        self.assertEqual(resposta.status_code, 405)

    def teste_confirmar_login_invalido(self):
        resposta = self.client.post(
            reverse('confirmar_login'), data={'nome': 'teste', 'senha': '1234'}
        )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(mensagem[0].message, 'Usuário ou senha inválidos')

    def teste_confirmar_login_valido(self):
        formulario = {
            'nome': 'teste', 'email': 'teste@email.com',
            'senha': '1234Abcd!', 'confirmar_senha': '1234Abcd!'
        }
        self.client.post(reverse('confirmar_cadastro'), formulario)
        resposta = self.client.post(
            reverse('confirmar_login'),
            data={'nome': 'teste', 'senha': '1234Abcd!'}
        )
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(mensagem[1].message, 'Logado com sucesso!')


class EmpresasTeste(TestCase):
    def setUp(self):
        # Crie um usuário de teste
        self.user = User.objects.create_user(
            username='teste',
            password='1234Abcd!'
        )
        self.client.login(username='teste', password='1234Abcd!')

    def teste_empresas_redireciona_para_login_se_nao_estiver_autenticado(self):
        self.client.logout()
        resposta = self.client.get(reverse('empresas'), follow=True)
        self.assertTemplateUsed(resposta, 'login_e_cadastro.html')

    def teste_empresas_view_retorna_status_code_200(self):
        resposta = self.client.get(reverse('empresas'))
        self.assertEqual(resposta.status_code, 200)

    def teste_empresas_view_carrega_template_empresas(self):
        resposta = self.client.get(reverse('empresas'))
        self.assertTemplateUsed(resposta, 'empresas.html')

    def teste_empresas_view_nao_aceita_requisicao_post(self):
        resposta = self.client.post(reverse('empresas'))
        self.assertEqual(resposta.status_code, 405)

    def teste_quantidade_empresas_listadas(self):
        for numero in range(1, 4):
            Empresa.objects.create(usuario=self.user, nome=f'Empresa {numero}')

        response = self.client.get(reverse('empresas'))
        empresas_listadas = response.context['empresas']
        self.assertEqual(len(empresas_listadas), 3)


class ExcluirEmpresaTeste(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste',
            password='1234Abcd!'
        )
        self.client.login(username='teste', password='1234Abcd!')

    def teste_excluir_empresa_redireciona_se_nao_estiver_autenticado(self):
        self.client.logout()
        resposta = self.client.get(
            reverse('excluir_empresa', args=[1]), follow=True
        )
        self.assertTemplateUsed(resposta, 'login_e_cadastro.html')

    def teste_excluir_empresa_view_retorna_status_code_200(self):
        resposta = self.client.get(
            reverse('excluir_empresa', args=[0]), follow=True
        )
        self.assertEqual(resposta.status_code, 200)

    def teste_excluir_empresa_com_sucesso(self):
        Empresa.objects.create(usuario=self.user, nome='Empresa excluida')
        resposta = self.client.get(reverse('excluir_empresa', args=[0]))
        mensagem = list(resposta.wsgi_request._messages)
        self.assertEqual(mensagem[0].message, 'Empresa excluida com sucesso')
