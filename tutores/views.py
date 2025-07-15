from django.shortcuts import render, redirect
from django.contrib import messages
from db_utils import execute_sql, delete 
from datetime import datetime

def formulario_tutor(request): 
    if request.method == 'POST':
    
        # Obter dados do formulário
        id_tutor = request.POST.get('id_tutor')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        tipo_conta = request.POST.get('tipo_conta', 'pf')
        endereco = request.POST.get('endereco', '')
        ativo = request.POST.get('ativo') == 'on'
        
        if id_tutor:  # Modo edição
            query = """
            UPDATE tutor SET
                nome = %s, email = %s, cpf = %s, data_nascimento = %s,
                telefone = %s, tipo_conta = %s, endereco = %s, ativo = %s
            WHERE id_tutor = %s
            """
            params = [nome, email, cpf, data_nascimento or None, 
                        telefone, tipo_conta, endereco, ativo, id_tutor]
            message = 'Tutor atualizado com sucesso!'
            messages.success(request, message)
        else:  # Modo criação
            query = """
            INSERT INTO tutor (
                nome, email, cpf, data_nascimento, telefone, 
                tipo_conta, endereco, ativo, data_cadastro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            params = [nome, email, cpf, data_nascimento or None, 
                        telefone, tipo_conta, endereco, ativo]
            message = 'Tutor cadastrado com sucesso!'
            messages.success(request, message)
            
        try:
            execute_sql(query, params, False)
        except Exception as e:
            print(f"erro : {e}")

    return redirect('tutores')

def listar_tutores(request):
    # Query base
    query = """
    SELECT id_tutor, nome, cpf, email, telefone, data_nascimento, 
           endereco, tipo_conta, ativo, data_cadastro
    FROM tutor
    """
    
    params = []
    
    # Filtros
    q = request.GET.get('q')
    status = request.GET.get('status')
    
    if q:
        query += " AND (nome LIKE %s OR cpf LIKE %s OR email LIKE %s)"
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%'])
    
    if status == 'ativo':
        query += " AND ativo = TRUE"
    elif status == 'inativo':
        query += " AND ativo = FALSE"
    
    query += " ORDER BY nome"
    
    tutores_paginados = execute_sql(query,[q], False)
    return tutores_paginados

def qtd_novos_tutores():
    query = """
    SELECT COUNT(*)
    FROM tutor
    WHERE data_cadastro >= CURRENT_DATE - INTERVAL '7 days'
	GROUP BY data_cadastro
    ORDER BY data_cadastro DESC;
    """
    tutores = execute_sql(query,[], True)
    return tutores

def delete_tutor(request):
    id_a = request.POST.get('id')
    try: 
        query = """
        DELETE FROM tutor WHERE id_tutor = %s
        """
        if delete(query, id_a):
            messages.success(request, "Deletado com sucesso")
        else: 
            messages.error(request, "O Tutor está sendo usado") 
    except Exception as e:
        messages.error(request, "O Tutor está sendo usado") 
        print(f"erro : {e}")

    return redirect("tutores")