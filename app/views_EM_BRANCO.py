from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .util_conexao import *
from .util_views import *


# DEFINE O PREFIXO DA PÁGINA HTML (TEMPLATE) QUE DEVERÁ SERÁ CARREGADA
#    - Exemplo: 'categorias', 'funcionarios'
TEMPLATE_PREFIXO = 'DEFINA_O_PREFIXO'


# COMANDO SELECT GERAL PARA RETORNAR OS REGISTROS
SQL_SELECT_GERAL = """
    SELECT  t1.id,
            t1.?,
            t2.?,
    
    FROM    TABELA t1
    INNER JOIN TABELA_2 t2 dep ON t2.id = t1.CHAVE_ESTRANGEIRA 
""" 

# COMANDO SQL PARA RETORNAR TODOS OS REGISTROS DEFININDO A ORDENAÇÃO
SQL_LISTAGEM = SQL_SELECT_GERAL + '\n    ' \
             + 'ORDER BY t1.CAMPO_PARA_ORDENAR'


# COMANDO SQL PARA SELECIONAR O REGISTRO PELO "id" INFORMADO
SQL_OBTER_REGISTRO = SQL_SELECT_GERAL + '\n    ' \
                   + 'WHERE   t1.id = {}'



# ======================================================================== #
# COMANDO SQL PARA EXCLUIR UM REGISTRO
# ======================================================================== #
SQL_EXCLUSAO = """ 
    DELETE FROM TABELA 
    WHERE id = {}
"""


# ======================================================================== #
# COMANDO SQL PARA INCLUIR UM REGISTRO
# 
# ATENÇÃO: observe o tipo de campo (VARCHAR, INT, DATE...) e 
#          se o seu valor deve estar entre aspas-simples ('')
# ======================================================================== #
SQL_INCLUSAO = """ 
    INSERT INTO TABELA( CAMPO_1, CAMPO_2, CAMPO_3, CAMPO_4) 
    VALUES('{}', '{}', {}, {})
"""


# ======================================================================== #
# COMANDO SQL PARA ALTERAR UM REGISTRO
# 
# ATENÇÃO-1: insira os campos na MESMA ORDEM utilizada no SQL_INCLUSAO
# 
# ATENÇÃO-2: observe o tipo de campo (VARCHAR, INT, DATE...) e 
#            se o seu valor deve estar entre aspas-simples ('')
# ======================================================================== #
SQL_ALTERACAO = """
    UPDATE TABELA 

    SET CAMPO_1 = '{}',
        CAMPO_2 = '{}', 
        CAMPO_3 = {}, 
        CAMPO_4 = {} 
    
    WHERE id = {}
"""

# CLASSE QUE HERDA DE "ViewGenericCRUD"
class ViewCRUD (ViewGenericCRUD):
    # metodo para obter os dados informados no <form> HTML
    def obter_campos_formulario(self):
        return [    
            # OBS-1: INFORME OS NOMES DOS CAMPOS NA ORDEM 
            #        QUE APARECEM NO SQL DE INCLUSAO/ALTERACAO 
            'CAMPO_1',
            'CAMPO_2',
            'CAMPO_3',
            'CAMPO_4',
            # 0BS-2: DEIXAR O ID POR ULTIMO
            'id',
        ]

    



# ======================================================================== #
# A T E N Ç Ã O - ESCOLHA 1 DENTRE OS 2 FORMULÁRIOS DE EXEMPLO ABAIXO      #
#                 E APAGUE AQUELE QUE VOCÊ NÃO FOR USAR                    #
# ======================================================================== #

# =============================================================
# FORMULÁRIO - EXEMPLO 1
# =============================================================
class Formulario(forms.Form):
    # ID (DEIXAR ASSIM, NÃO ALTERAR)
    id = forms.IntegerField(label='ID', 
            widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    # campos do formulario
    nome = forms.CharField(label='Nome', max_length=30, required=True)
        
# =============================================================
# FORMULÁRIO - EXEMPLO 2   ( CONTENDO CAMPO <SELECT> )
# =============================================================
class Formulario(forms.Form):
    # ID (DEIXAR ASSIM, NÃO ALTERAR)
    id = forms.IntegerField(label='ID', 
            widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    # campos do formulario
    nome = forms.CharField(label='Nome', max_length=90, required=True)
    idade = forms.IntegerField(label='Idade', required=True)           
    dataNascimento = forms.DateField(label='Nascimento', required=True)        
    departamento_id = forms.ChoiceField(label='Categoria')

    # construtor do Formulario
    def __init__(self, *args, **kwargs):
            # chama construtor da classe-Pai
            super().__init__(*args, **kwargs)
            # obtem os registros da tabela Departamentos
            departamentos = executar_select('SELECT id, nome FROM Departamento ORDER BY nome')
            # carrega os departamentos no <select> da página usando o ChoiceField
            self.fields['departamento_id'].choices = departamentos
    



# ============================================================= #
# OBS: NÃO PRECISA ALTERAR ESTA PARTE DO CÓDIGO                 #
# ============================================================= #
# classe que será utilizada como VIEW e que contem os 
# métodos listar(), editar() e salvar()
VIEW_CRUD = ViewCRUD(
    TEMPLATE_PREFIXO=TEMPLATE_PREFIXO, 
    SQL_LISTAGEM=SQL_LISTAGEM, 
    SQL_OBTER_REGISTRO=SQL_OBTER_REGISTRO, 
    SQL_INCLUSAO=SQL_INCLUSAO, 
    SQL_ALTERACAO=SQL_ALTERACAO,
    SQL_EXCLUSAO=SQL_EXCLUSAO, 
    FORMULARIO_CLASS=Formulario, 
)


