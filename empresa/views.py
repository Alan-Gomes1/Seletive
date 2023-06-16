from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render

from .forms.login import LoginForm
from .models import Empresa, Tecnologias, Vagas


def login_view(request):
    return render(request, 'login_e_cadastro.html')


def nova_empresa(request):
    if request.method == 'GET':
        techs = Tecnologias.objects.all()
        nichos = Empresa.choices_nicho_mercado
        return render(
            request, 'nova_empresa.html', {'techs': techs, 'nichos': nichos}
        )
    elif request.method == 'POST':
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
            return redirect('/nova_empresa')

        if logo.size > 100_000_000:
            messages.add_message(
                request, constants.ERROR,
                'A logo da empresa deve ter menos de 10MB'
            )
            return redirect('/nova_empresa')

        if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
            messages.add_message(
                request, constants.ERROR, 'Nicho de mercado inválido'
            )
            return redirect('/nova_empresa')

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
        return redirect('/empresas')


def empresas(request):
    empresas = Empresa.objects.all()
    tecnologias = Tecnologias.objects.all()

    filtro_tecnologias = request.GET.get('tecnologias')
    filtro_nome = request.GET.get('nome')

    if filtro_tecnologias:
        empresas = empresas.filter(tecnologias=filtro_tecnologias)

    if filtro_nome:
        empresas = empresas.filter(nome__icontans=filtro_nome)

    if request.method == 'POST':
        formulario = LoginForm(request.POST)

        if formulario.is_valid():
            autenticacao = authenticate(
                nome=formulario.cleaned_data.get('nome', ''),
                senha=formulario.cleaned_data.get('senha', ''),
            )

            if autenticacao is not None:
                messages.add_message(
                    request, constants.SUCCESS, 'Logado com sucesso!'
                )
                login(request, autenticacao)
            else:
                messages.add_message(
                    request, constants.ERROR, 'Dados incorretos'
                )
                return redirect('/login')
        else:
            messages.add_message(
                    request, constants.ERROR, 'Usuário ou senha inválido'
            )

    return render(
        request, 'empresas.html',
        {'empresas': empresas, 'tecnologias': tecnologias}
    )


def excluir_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    empresa.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Empresa excluida com sucesso'
    )
    return redirect('/empresas')


def empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    tecnologias = Tecnologias.objects.all()
    empresas = Empresa.objects.all()
    vagas = Vagas.objects.filter(empresa_id=id)
    return render(
        request, 'empresa.html',
        {'empresa': empresa, 'tecnologias': tecnologias,
         'empresas': empresas, 'vagas': vagas}
    )
