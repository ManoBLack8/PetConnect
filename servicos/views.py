from django.shortcuts import render, redirect
from django.contrib import messages
from db_utils import execute_sql
from datetime import datetime

def formulario_servico(request):
    """Processa o formulário de criação/edição de serviços"""
    if request.method == 'POST':
        # Obter dados do formulário
        id_servico = request.POST.get('id_servico')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        valor = float(request.POST.get('valor', 0))
        if id_servico:  # Modo edição
            query = """
            UPDATE servico SET
                nome = %s, descricao = %s, valor = %s
            WHERE id_servico = %s
            """
            params = [nome, descricao, valor, id_servico]
            message = 'Serviço atualizado com sucesso!'
        else:  # Modo criação
            query = """
            INSERT INTO servico (
                nome, descricao, valor
            ) VALUES (%s, %s, %s)
            """
            params = [nome, descricao, valor]
            message = 'Serviço cadastrado com sucesso!'

        try:
            execute_sql(query, params, False)
        except Exception as e:
            print(f"erro : {e}")



    return redirect('servico')

def listar_servicos():
    """Lista todos os serviços com possíveis filtros"""
    # Query base
    query = """
    SELECT id_servico, nome, descricao, valor
    FROM servico
    WHERE 1=1
    """

    servicos = execute_sql(query, [], False)
    return servicos

def delete_servico(request):
    id_a = request.POST.get('id')
    query = """
    DELETE FROM servico WHERE id_servico = %s
    """
    try: 
        if delete(query, id_a):
            messages.success(request, "Deletado com sucesso!")
        else: 
            messages.error(request, "O Serviço está sendo usado!") 
    except Exception as e:
        messages.error(request, "O Serviço está sendo usado") 
        print(f"erro : {e}")
    
    return redirect("pets")