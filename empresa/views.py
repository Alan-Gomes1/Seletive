from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from .forms import CadastroForm, LoginForm
from .models import Empresa, Tecnologias, Vagas


class BaseView(View, LoginRequiredMixin):
    ...


class Login(View):
    def get(self, request):
        return render(request, 'login_e_cadastro.html')


class ConfirmarLogin(View):
    def post(self, request):
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            nome = formulario.cleaned_data.get('nome')
            senha = formulario.cleaned_data.get('senha')

        try:
            autenticacao = authenticate(
                request.user, username=nome, password=senha
            )
            if autenticacao.is_authenticated:
                login(request, autenticacao)
                messages.add_message(
                    request, constants.SUCCESS, 'Logado com sucesso!'
                )
                return redirect(reverse('empresas'))
        except:
            messages.add_message(
                request, constants.ERROR, 'Usuário ou senha inválidos'
            )
            return render(request, 'login_e_cadastro.html')

        return render(request, 'login_e_cadastro.html')


class ConfirmarCadastro(View):
    def post(self, request):
        formulario = CadastroForm(request.POST,)

        if formulario.is_valid():
            nome = formulario.cleaned_data.get('nome')
            formulario.username = nome
            formulario.save()
            # senha = formulario.cleaned_data.get('senha')
            # usuario = formulario.save(commit=False)
            # usuario.set_password(senha)

            messages.add_message(
                request, constants.SUCCESS, 'Cadastro realizado com sucesso!'
            )
            return redirect(reverse('login'))

        messages.add_message(request, constants.ERROR, 'Erro ao cadastrar!')
        return render(
            request, 'login_e_cadastro.html', {'formulario': formulario}
        )


class NovaEmpresa(BaseView):
    def get(self, request):
        techs = Tecnologias.objects.all()
        nichos = Empresa.choices_nicho_mercado
        return render(
            request, 'nova_empresa.html', {'techs': techs, 'nichos': nichos}
        )

    def post(self, request):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        nicho = request.POST.get('nicho')
        caracteristicas = request.POST.get('caracteristicas')
        tecnologias = request.POST.getlist('tecnologias')
        logo = request.FILES.get('logo')

        if (len(nome.strip()) == 0 or len(email.strip()) == 0 or
            len(cidade.strip()) == 0 or len(endereco.strip()) == 0 or
            len(nicho.strip()) == 0 or len(caracteristicas.strip()) == 0
                or (not logo)):
            messages.add_message(
                request, constants.ERROR, 'Preencha todos os campos'
            )
            return redirect(reverse('nova_empresa'))

        if logo.size > 100_000_000:
            messages.add_message(
                request, constants.ERROR,
                'A logo da empresa deve ter menos de 10MB'
            )
            return redirect(reverse('nova_empresa'))

        if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
            messages.add_message(
                request, constants.ERROR, 'Nicho de mercado inválido'
            )
            return redirect(reverse('nova_empresa'))

        empresa = Empresa(
            logo=logo,
            nome=nome,
            email=email,
            cidade=cidade,
            endereco=endereco,
            nicho_mercado=nicho,
            caracteristica_empresa=caracteristicas)
        empresa.save()
        empresa.tecnologias.add(*tecnologias)
        empresa.save()
        messages.add_message(
            request, constants.SUCCESS, 'Empresa cadastrada com sucesso'
        )
        return redirect(reverse('empresas'))


class Empresas(BaseView):
    def get(self, request):
        empresas = Empresa.objects.all()
        empresas = Empresa.objects.all()
        tecnologias = Tecnologias.objects.all()

        filtro_tecnologias = request.GET.get('tecnologias')
        filtro_nome = request.GET.get('nome')

        if filtro_tecnologias:
            empresas = empresas.filter(tecnologias=filtro_tecnologias)

        if filtro_nome:
            empresas = empresas.filter(nome__icontains=filtro_nome)

        return render(
            request, 'empresas.html',
            {'empresas': empresas, 'tecnologias': tecnologias}
        )


class ExcluirEmpresa(BaseView):
    def get(self, request, id):
        empresa = get_object_or_404(Empresa, id=id)
        empresa.delete()
        messages.add_message(
            request, constants.SUCCESS, 'Empresa excluida com sucesso'
        )
        return redirect(reverse('empresas'))


class EmpresaView(BaseView):
    def get(self, request, id):
        empresa = get_object_or_404(Empresa, id=id)
        tecnologias = Tecnologias.objects.all()
        empresas = Empresa.objects.all()
        vagas = Vagas.objects.filter(empresa_id=id)
        return render(
            request, 'empresa.html', {
                'empresa': empresa, 'tecnologias': tecnologias,
                'empresas': empresas, 'vagas': vagas
             }
        )
