from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .util_conexao import *
from .util_views import *


# define o PREFIXO da página HTML (template) que deverá será carregada
TEMPLATE_PREFIXO = 'funcionarios'


# Comando SELECT geral para retornar os registros
SQL_SELECT_GERAL = """
    SELECT  fun.id,
            fun.nome,
            fun.telefones,
            fun.idade,
            fun.data_nascimento,
            fun.endereco,
            fun.departamento_id,
            dep.nome as departamento_nome
    
    FROM    Funcionario fun
    INNER JOIN Departamento dep ON dep.id = fun.departamento_id 
""" 


# Comando SQL para selecionar o registro pelo "id" informado
SQL_OBTER_REGISTRO = SQL_SELECT_GERAL + '\n    ' \
                   + 'WHERE   fun.id = {}'


# Comando SQL para retornar todos os registros definindo a ordenação
SQL_LISTAGEM = SQL_SELECT_GERAL + '\n    ' \
             + 'ORDER BY fun.nome'


# Comando SQL para excluir um registro
SQL_EXCLUSAO = """ 
    DELETE FROM Funcionario 
    WHERE id = {}
"""


# Comando SQL para incluir um registro
SQL_INCLUSAO = """ 
    INSERT INTO Funcionario(nome, telefones, idade, data_nascimento, endereco, departamento_id) 
    VALUES('{}', '{}', {}, '{}', '{}', {})
"""


# Comando SQL para alterar um registro
SQL_ALTERACAO = """
    UPDATE Funcionario 
    SET nome = '{}',
        telefones = '{}', 
        idade = {}, 
        data_nascimento = '{}', 
        endereco = '{}', 
        departamento_id = {} 
    WHERE id = {}
"""

# classe que herda de "ViewGenericCRUD"
class ViewCRUD (ViewGenericCRUD):
    
    def obter_campos_formulario(self):
        return [    
            # OBS-1: INFORME OS CAMPOS NA ORDEM QUE APARECEM NO SQL DE INCLUSAO/ALTERACAO 
            'nome',
            'telefones',
            'idade',
            'dataNascimento',
            'endereco',
            'departamento_id',
            # 0BS-2: DEIXAR O ID POR ULTIMO
            'id',
        ]

        
# formulario utilizado para edicao dos registros (inclusao e alteracao)
class Formulario(forms.Form):
    # ID (DEIXAR ASSIM, NÃO ALTERAR)
    id = forms.IntegerField(label='ID', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    # campos do formulario
    nome = forms.CharField(label='Nome', max_length=90, required=True)
    telefones = forms.CharField(label='Telefones', max_length=20, required=True)
    idade = forms.IntegerField(label='Idade', required=True)           
    dataNascimento = forms.DateField(label='Nascimento', required=True)        
    endereco = forms.CharField(label='Endereço', max_length=200, required=True)
    departamento_id = forms.ChoiceField(label='Categoria')

    # construtor do Formulario
    def __init__(self, *args, **kwargs):
            # chama construtor da classe-Pai
            super().__init__(*args, **kwargs)
            # obtem os registros da tabela Departamentos
            departamentos = executar_select('SELECT id, nome FROM Departamento ORDER BY nome')
            # carrega os departamentos no <select> da página usando o ChoiceField
            self.fields['departamento_id'].choices = departamentos
    




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


