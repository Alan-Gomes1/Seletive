from django.urls import path
from . import views


urlpatterns = [
    path('nova_vaga/', views.NovaVaga.as_view(), name='nova_vaga'),
    path('vaga/<int:id>/', views.Vaga.as_view(), name='vaga'),
    path(
        'nova_tarefa/<int:id_vaga>/',
        views.NovaTarefa.as_view(), name='nova_tarefa'
        ),
    path(
        'realizar_tarefa/<int:id>/',
        views.RealizarTarefa.as_view(), name='realizar_tarefa'
    ),
    path(
        'envia_email/<int:id_vaga>/',
        views.EnviarEmail.as_view(), name='envia_email'
        ),
]
