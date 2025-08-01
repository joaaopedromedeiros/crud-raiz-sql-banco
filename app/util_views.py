from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .util_conexao import *


from abc import ABC, abstractmethod


class ViewGenericCRUD():

    @abstractmethod
    def obter_campos_formulario(self, dados): pass

    def adicionar_informacoes_no_contexto(self, context):
        return context

    def __init__(self, TEMPLATE_PREFIXO, SQL_LISTAGEM, SQL_OBTER_REGISTRO, FORMULARIO_CLASS, 
                 SQL_EXCLUSAO, SQL_INCLUSAO, SQL_ALTERACAO):
        self.TEMPLATE_PREFIXO = TEMPLATE_PREFIXO
        self.SQL_LISTAGEM = SQL_LISTAGEM
        self.SQL_OBTER_REGISTRO = SQL_OBTER_REGISTRO
        self.FORMULARIO_CLASS = FORMULARIO_CLASS
        self.SQL_EXCLUSAO = SQL_EXCLUSAO
        self.SQL_INCLUSAO = SQL_INCLUSAO
        self.SQL_ALTERACAO = SQL_ALTERACAO


    def listar(self, request):
        try:
            # obtem todos os registros retornados
            sql = self.SQL_LISTAGEM
            registros = executar_select(sql)
            print(f'\n\n{sql}\n')

            # configura contexto
            context = {'registros': registros}
            context = self.adicionar_informacoes_no_contexto(context)
            # define a pagina a ser carregada, adicionando os registros das tabelas 
            return render(request, f'{self.TEMPLATE_PREFIXO}_listar.html', context=context)
        
        # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
        except Exception as err:
            return render(request, f'{self.TEMPLATE_PREFIXO}_listar.html', context={'ERRO': err})


    # exibe a pagina de inclusao/alteracao/exclusao dos registros
    def editar(self, request, acao=None, id=None,):
        try:

            # inserir registro
            if acao == 'incluir':
                # configura contexto
                context={'acao': 'Inclusão', 'form': self.FORMULARIO_CLASS(),}
                context = self.adicionar_informacoes_no_contexto(context)
                # retorna
                return render(request, f'{self.TEMPLATE_PREFIXO}_editar.html', context=context)
            
            # alterar ou excluir
            elif acao in ['alterar', 'excluir']:
                
                # seleciona o registro pelo ID
                sql = self.SQL_OBTER_REGISTRO.format(id)
                print(f'\n\n{sql}\n')
                reg, cursor = executar_select( sql , retornar_cursor=True)
                reg = reg[0]
                
                nomes_campos = [column[0] for column in cursor.description]
                print(f'\n\nNOMES_CAMPOS_SELECT_POR_ID:\n{nomes_campos}\n')

                # obtem primeiro elemento retornado (indice=[0])
                # reg = self.obter_registro_como_dict( reg[0] )

                reg_dict = {}
                for i_col, nome_campo in enumerate(nomes_campos):
                    reg_dict[nome_campo] = reg[i_col]
                print(f'\n\nDICT_VALORES_EXIBIR_FORMULARIO:\n{reg_dict}\n')

                acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
                
                form = None if acao == 'excluir' else self.FORMULARIO_CLASS(initial=reg_dict)

                # configura contexto
                context={'acao': acao, 'reg': reg, 'form': form}
                context = self.adicionar_informacoes_no_contexto(context)
                # retorna
                return render(request, f'{self.TEMPLATE_PREFIXO}_editar.html', 
                            context=context)
        
        # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
        except Exception as err:
            return render(request, f'{self.TEMPLATE_PREFIXO}_editar.html', context={'ERRO': err})


    # metodo para salvar o registro incluido/alterado/excluido 
    def salvar(self, request):
        try:
            # obtem a acao a ser executada
            acao = request.POST['acao']

            # obtem os dados do formulario submetido
            form = self.FORMULARIO_CLASS(request.POST) 

            if acao == 'Exclusão':
                # informa o ID do registro a ser excluido
                sql = self.SQL_EXCLUSAO.format(request.POST['id'])
            
            else:
                if not form.is_valid():
                    # configura contexto
                    context={'form': form}
                    context = self.adicionar_informacoes_no_contexto(context)
                    # retorna
                    return render(request, f'{self.TEMPLATE_PREFIXO}_editar.html', context=context)

                form_data = form.cleaned_data
                
                # se for inclusao de registro
                if acao == 'Inclusão':
                    valores = self.obter_valores(form_data, remover_id=True)
                    sql = self.SQL_INCLUSAO.format(*valores)
                    # print(f'\n\nVALORES:\n{valores}\n')
                
                # se for exclusao de registro
                elif acao == 'Exclusão':
                    # informa o ID do registro a ser excluido
                    sql = self.SQL_EXCLUSAO.format(form_data['id'])
                
                # se for alteracao de registro
                else:
                    valores = self.obter_valores(form_data)
                    sql = self.SQL_ALTERACAO.format(*valores)
                    # print(f'\n\nVALORES:\n{valores}\n')
            


            # executa o INSERT/UPDATE/DELETE 
            executar_sql(sql)
            print(f'\n\n{sql}\n')

            # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
            # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
            return HttpResponseRedirect( f'/{self.TEMPLATE_PREFIXO}' )

        # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
        except Exception as err:
            return render(request, f'{self.TEMPLATE_PREFIXO}_editar.html', context={'ERRO': err})


    def obter_valores(self, form_data, remover_id=False):
        valores = list()
        tem_id = False
        for campo in self.obter_campos_formulario():
            if campo == 'id':
                tem_id = True
            else:    
                valores.append(form_data[campo])

        if tem_id and not remover_id:
            valores.append(form_data['id'])
        return valores