# views_aluno.py

from django import forms
from .util_conexao import *
from .util_views import *

TEMPLATE_PREFIXO = 'alunos'

SQL_SELECT_GERAL = """
    SELECT  alu.id,
            alu.nome,
            alu.telefone,
            alu.idade,
            alu.data_nascimento,
            alu.turma_id,
            tur.nome as turma_nome
    FROM Aluno alu
    INNER JOIN Turma tur ON tur.id = alu.turma_id
"""

SQL_OBTER_REGISTRO = SQL_SELECT_GERAL + '\nWHERE alu.id = {}'

SQL_LISTAGEM = SQL_SELECT_GERAL + '\nORDER BY alu.nome'

SQL_EXCLUSAO = "DELETE FROM Aluno WHERE id = {}"

SQL_INCLUSAO = """
    INSERT INTO Aluno (nome, telefone, idade, data_nascimento, turma_id)
    VALUES ('{}', '{}', {}, '{}', {})
"""

SQL_ALTERACAO = """
    UPDATE Aluno SET 
        nome = '{}',
        telefone = '{}',
        idade = {},
        data_nascimento = '{}',
        turma_id = {}
    WHERE id = {}
"""

class ViewCRUD(ViewGenericCRUD):
    def obter_campos_formulario(self):
        return ['nome', 'telefone', 'idade', 'data_nascimento', 'turma_id', 'id']

class Formulario(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    nome = forms.CharField(label='Nome', max_length=90, required=True)
    telefone = forms.CharField(label='Telefone', max_length=20, required=False)
    idade = forms.IntegerField(label='Idade', required=True)
    data_nascimento = forms.DateField(label='Data de Nascimento', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    turma_id = forms.ChoiceField(label='Turma')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        turmas = executar_select('SELECT id, nome FROM Turma ORDER BY nome')
        self.fields['turma_id'].choices = turmas

VIEW_CRUD = ViewCRUD(
    TEMPLATE_PREFIXO=TEMPLATE_PREFIXO,
    SQL_LISTAGEM=SQL_LISTAGEM,
    SQL_OBTER_REGISTRO=SQL_OBTER_REGISTRO,
    SQL_INCLUSAO=SQL_INCLUSAO,
    SQL_ALTERACAO=SQL_ALTERACAO,
    SQL_EXCLUSAO=SQL_EXCLUSAO,
    FORMULARIO_CLASS=Formulario,
)
