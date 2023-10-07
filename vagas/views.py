from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from empresa.models import Vagas
from empresa.views import BaseView

from .models import Emails, Tarefas


class NovaVaga(BaseView):
    def post(self, request):
        usuario = request.user
        titulo = request.POST.get('titulo')
        email = request.POST.get('email')
        tecnologias_domina = request.POST.getlist('tecnologias_domina')
        tecnologias_nao_domina = request.POST.getlist('tecnologias_nao_domina')
        experiencia = request.POST.get('experiencia')
        data_final = request.POST.get('data_final')
        empresa = request.POST.get('empresa')
        status = request.POST.get('status')

        if (len(titulo.strip()) < 5 or len(email.strip()) < 5 or
                len(experiencia.strip()) < 1 or len(empresa.strip()) < 1 or
                len(status.strip()) < 1 or len(data_final.strip()) < 5):
            messages.add_message(
                request, constants.ERROR,
                'Preencha todos os campos corretamente'
            )
            return redirect(f'/empresa/{empresa}')

        vaga = Vagas(
            usuario=usuario,
            titulo=titulo,
            email=email,
            nivel_experiencia=experiencia,
            data_final=data_final,
            empresa_id=empresa,
            status=status,
        )
        vaga.save()

        vaga.tecnologias_estudar.add(*tecnologias_nao_domina)
        vaga.tecnologias_dominadas.add(*tecnologias_domina)
        vaga.save()
        messages.add_message(
            request, constants.SUCCESS, 'Vaga criada com sucesso.'
        )
        return redirect(f'/empresa/{empresa}')


class Vaga(BaseView):
    def get(self, request, id):
        vaga = Vagas.objects.filter(id=id, usuario=request.user).first()
        tarefas = Tarefas.objects.filter(vaga=vaga)
        emails = Emails.objects.filter(vaga=vaga)
        return render(
            request, 'vaga.html',
            {'vaga': vaga, 'tarefas': tarefas, 'emails': emails}
        )


class NovaTarefa(BaseView):
    def post(self, request, id_vaga):
        titulo = request.POST.get('titulo')
        prioridade = request.POST.get('prioridade')
        data = request.POST.get('data')

        # TODO: validations

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
