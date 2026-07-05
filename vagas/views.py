from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from empresa.models import Vagas
from empresa.views import BaseView

from .forms import VagaForm
from .models import Emails, Tarefas


class NovaVaga(BaseView):
    def post(self, request):
        form = VagaForm(request.POST)
        if not form.is_valid():
            messages.add_message(
                request, constants.ERROR,
                'Preencha todos os campos corretamente'
            )
            return redirect(f'/empresa/{request.POST.get("empresa")}')

        vaga = form.save(commit=False)
        vaga.usuario = request.user
        vaga.save()
        form.save_m2m()

        messages.add_message(
            request, constants.SUCCESS, 'Vaga criada com sucesso.'
        )
        return redirect(f'/empresa/{vaga.empresa_id}')


class Vaga(BaseView):
    def get(self, request, id):
        vaga = Vagas.objects.filter(id=id, usuario=request.user).first()
        tarefas = Tarefas.objects.filter(vaga=vaga)
        emails = Emails.objects.filter(vaga=vaga)
        if vaga:
            return render(
                request, 'vaga.html',
                {'vaga': vaga, 'tarefas': tarefas, 'emails': emails}
            )
        messages.add_message(
            request, constants.ERROR, 'Vaga não encontrada.'
        )
        return redirect('/empresas')


class NovaTarefa(BaseView):
    def post(self, request, id_vaga):
        titulo = request.POST.get('titulo')
        prioridade = request.POST.get('prioridade')
        data = request.POST.get('data')

        if len(titulo.strip()) < 5:
            messages.add_message(
                request, constants.ERROR,
                'Título must be at least 5 characters.'
            )
            return redirect(f'/vagas/vaga/{id_vaga}')

        valid_priorities = ['A', 'B', 'U']
        if prioridade not in valid_priorities:
            messages.add_message(
                request, constants.ERROR,
                'Invalid priority level.'
            )
            return redirect(f'/vagas/vaga/{id_vaga}')

        if not data or len(data.strip()) < 1:
            messages.add_message(
                request, constants.ERROR,
                'Data field is required.'
            )
            return redirect(f'/vagas/vaga/{id_vaga}')

        try:
            Vagas.objects.get(id=id_vaga, usuario=request.user)
        except Vagas.DoesNotExist:
            messages.add_message(
                request, constants.ERROR,
                'Vaga not found or does not belong to you.'
            )
            return redirect('/empresas')

        tarefa = Tarefas(
            titulo=titulo,
            prioridade=prioridade,
            data=data,
            vaga_id=id_vaga
        )
        tarefa.save()
        messages.add_message(
            request, constants.SUCCESS, 'Tarefa criada com sucesso.'
        )
        return redirect(f'/vagas/vaga/{id_vaga}')


class RealizarTarefa(BaseView):
    def post(self, request, id):
        tarefa = Tarefas.objects.filter(id=id).filter(realizada=False)

        if not tarefa.exists():
            messages.add_message(request, constants.ERROR, 'Tarefa não existe')
            return redirect('/empresas')

        tarefa = tarefa.first()
        tarefa.realizada = True
        tarefa.save()
        messages.add_message(request, constants.ERROR, 'Tarefa finalizada!')
        return redirect(f'/vagas/vaga/{tarefa.vaga.id}')


class EnviarEmail(BaseView):
    def get(self, request, id_vaga):
        vaga = Vagas.objects.get(id=id_vaga)
        assunto = request.POST.get('assunto')
        corpo = request.POST.get('corpo')

        conteudo_html = render_to_string(
            'emails/template_email.html', {'corpo': corpo}
        )
        texto = strip_tags(conteudo_html)
        email = EmailMultiAlternatives(
            assunto, texto, settings.EMAIL_HOST_USER, [vaga.email, ]
        )
        email.attach_alternative(conteudo_html, 'text/html')

        if email.send():
            mail = Emails(
                vaga=vaga,
                assunto=assunto,
                corpo=corpo,
                enviado=True
            )
            mail.save()
            messages.add_message(
                request, constants.SUCCESS, 'Email enviado com sucesso.'
            )
        else:
            mail = Emails(
                vaga=vaga,
                assunto=assunto,
                corpo=corpo,
                enviado=False
            )
            mail.save()
            messages.add_message(
                request, constants.ERROR, 'Não conseguimos enviar o seu email!'
            )

        return redirect(f'/vagas/vaga/{id_vaga}')
