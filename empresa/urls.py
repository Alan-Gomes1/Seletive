from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('confirmar_login/', views.confirmar_login, name='confirmar_login'),
    path(
        'confirmar_cadastro/', views.confirmar_cadastro,
        name='confirmar_cadastro'
    ),
    path('nova_empresa/', views.nova_empresa, name='nova_empresa'),
    path('empresas/', views.empresas, name='empresas'),
    path(
        'excluir_empresa/<int:id>/',
        views.excluir_empresa, name='excluir_empresa'
    ),
    path('empresa/<int:id>/', views.empresa, name='empresa'),
]
