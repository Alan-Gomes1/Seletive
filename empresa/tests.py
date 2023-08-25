from django.test import TestCase
from django.urls import reverse


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

    def teste_confirmar_cadastro_view_retorna_status_code_200(self):
        self.assertEqual(self.resposta.status_code, 200)

    def teste_confirmar_cadastro_view_carrega_template_login_e_cadastro(self):
        self.assertTemplateUsed(self.resposta, 'login_e_cadastro.html')

    def teste_confirmar_cadastro_view_nao_aceita_requisicao_get(self):
        resposta = self.client.get(reverse('confirmar_cadastro'), {})
        self.assertEqual(resposta.status_code, 405)


class ConfirmarLoginTeste(TestCase):
    def setUp(self):
        self.resposta = self.client.post(reverse('confirmar_login'))

    def teste_confirmar_login_view_retorna_status_code_200(self):
        self.assertEqual(self.resposta.status_code, 200)

    def teste_confirmar_login_conteudo(self):
        self.assertIn('login', self.resposta.content.decode('utf-8'))
