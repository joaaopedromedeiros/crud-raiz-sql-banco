"""
URL configuration for proj_bd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import (
    views_app, 
    views_departamentos, 
    views_funcionarios,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ===========================================================================
    # Exibe a pagina inicial da nossa aplicacao
    path('', views_app.home, name='home'),

    # ===========================================================================
    # Rotas: DEPARTAMENTOS
    #   - departamentos/              : exibe página de listagem
    #   - departamentos/incluir/      : exibe a página de inclusao de registro
    #   - departamentos/alterar/<id>/ : exibe a página de alteracao de registro
    #   - departamentos/excluir/<id>/ : exibe a página de exclusao de registro
    #   - departamentos/salvar/       : insere, altera ou exclui um registro do BD
    path('departamentos/', views_departamentos.VIEW_CRUD.listar, name='departamentos_listar'),
    path('departamentos/<str:acao>/<int:id>', views_departamentos.VIEW_CRUD.editar, name='departamentos_editar'),
    path('departamentos/salvar/', views_departamentos.VIEW_CRUD.salvar, name='departamentos_salvar'),

    # ===========================================================================
    # Rotas: FUNCIONARIOS
    path('funcionarios/', views_funcionarios.VIEW_CRUD.listar, name='funcionarios_listar'),
    path('funcionarios/<str:acao>/<int:id>', views_funcionarios.VIEW_CRUD.editar, name='funcionarios_editar'),
    path('funcionarios/salvar/', views_funcionarios.VIEW_CRUD.salvar, name='funcionarios_salvar'),
] 
