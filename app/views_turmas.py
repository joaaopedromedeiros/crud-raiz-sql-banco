# views_turma.py

from django import forms
from .util_conexao import *
from .util_views import *

TEMPLATE_PREFIXO = 'turmas'

SQL_SELECT_GERAL = """
    SELECT id, nome
    FROM Turma
"""

SQL_OBTER_REGISTRO = SQL_SELECT_GERAL + '\nWHERE id = {}'

SQL_LISTAGEM = SQL_SELECT_GERAL + '\nORDER BY nome'

SQL_EXCLUSAO = "DELETE FROM Turma WHERE id = {}"

SQL_INCLUSAO = "INSERT INTO Turma (nome) VALUES ('{}')"

SQL_ALTERACAO = "UPDATE Turma SET nome = '{}' WHERE id = {}"

class ViewCRUD(ViewGenericCRUD):
    def obter_campos_formulario(self):
        return ['nome', 'id']

class Formulario(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    nome = forms.CharField(label='Nome da Turma', max_length=30, required=True)

VIEW_CRUD = ViewCRUD(
    TEMPLATE_PREFIXO=TEMPLATE_PREFIXO,
    SQL_LISTAGEM=SQL_LISTAGEM,
    SQL_OBTER_REGISTRO=SQL_OBTER_REGISTRO,
    SQL_INCLUSAO=SQL_INCLUSAO,
    SQL_ALTERACAO=SQL_ALTERACAO,
    SQL_EXCLUSAO=SQL_EXCLUSAO,
    FORMULARIO_CLASS=Formulario,
)
