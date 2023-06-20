from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path(
        'confirmar_login/',
        views.ConfirmarLogin.as_view(), name='confirmar_login'
        ),
    path(
        'confirmar_cadastro/', views.ConfirmarCadastro.as_view(),
        name='confirmar_cadastro'
    ),
    path('nova_empresa/', views.NovaEmpresa.as_view(), name='nova_empresa'),
    path('empresas/', views.Empresas.as_view(), name='empresas'),
    path(
        'excluir_empresa/<int:id>/',
        views.ExcluirEmpresa.as_view(), name='excluir_empresa'
    ),
    path('empresa/<int:id>/', views.EmpresaView.as_view(), name='empresa'),
]
