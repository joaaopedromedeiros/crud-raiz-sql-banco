from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .util_conexao import *
from .util_views import *


# define o PREFIXO da página HTML (template) que deverá será carregada
TEMPLATE_PREFIXO = 'departamentos'


# Comando SELECT geral para retornar os registros
SQL_SELECT_GERAL = """
    SELECT   dep.id,
             dep.nome
    FROM     Departamento dep
""" 


# Comando SQL para selecionar o registro pelo "id" informado
SQL_OBTER_REGISTRO = SQL_SELECT_GERAL + '\n    ' \
                   + 'WHERE   dep.id = {}'


# Comando SQL para retornar todos os registros definindo a ordenação
SQL_LISTAGEM = SQL_SELECT_GERAL + '\n    ' \
             + 'ORDER BY dep.nome'


# Comando SQL para excluir um registro
SQL_EXCLUSAO = """ 
    DELETE FROM Departamento 
    WHERE id = {}
"""


# Comando SQL para incluir um registro
SQL_INCLUSAO = """ 
    INSERT INTO Departamento(nome) 
    VALUES('{}')
"""


# Comando SQL para alterar um registro
SQL_ALTERACAO = """
    UPDATE Departamento 
    SET nome = '{}' 
    WHERE id = {}
"""


# classe que herda de "ViewGenericCRUD"
class ViewCRUD (ViewGenericCRUD):
    
    def obter_campos_formulario(self):
        return [    
            # OBS-1: INFORME OS CAMPOS NA ORDEM QUE APARECEM NO SQL DE INCLUSAO/ALTERACAO 
            'nome',
            # 0BS-2: DEIXAR O ID POR ULTIMO
            'id',
        ]

    

# formulario utilizado para edicao de registros
class Formulario(forms.Form):
    # ID (DEIXAR ASSIM, NÃO ALTERAR)
    id = forms.IntegerField(label='ID', 
         widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    # campos do formulario
    nome = forms.CharField(label='Nome', max_length=30, required=True)



# classe que será utilizada como VIEW e que contem os métodos listar(), editar() e salvar()
# OBS: NÃO PRECISA ALTERAR ESTA PARTE DO CÓDIGO
VIEW_CRUD = ViewCRUD(
    TEMPLATE_PREFIXO=TEMPLATE_PREFIXO, 
    SQL_LISTAGEM=SQL_LISTAGEM, 
    SQL_OBTER_REGISTRO=SQL_OBTER_REGISTRO, 
    SQL_INCLUSAO=SQL_INCLUSAO, 
    SQL_ALTERACAO=SQL_ALTERACAO,
    SQL_EXCLUSAO=SQL_EXCLUSAO, 
    FORMULARIO_CLASS=Formulario, 
)


