from django.shortcuts import render, redirect
from db_utils import execute_sql
from django.contrib import messages

def formulario_pets(request): 
    if request.method == 'POST':
        # Obter dados do formulário
        id_pet = request.POST.get('id_pet')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        raca = request.POST.get('raca')
        idade = request.POST.get('idade')
        peso = request.POST.get('peso')
        id_tutor = request.POST.get('tutor')
        cuidados_especiais = request.POST.get('cuidados_especiais', '')
        descricao = request.POST.get('descricao', '')
        ativo = request.POST.get('ativo') == 'on'
        
        if id_pet:  # Modo edição
            query = """
            UPDATE pets SET
                nome = %s, tipo = %s, raca = %s, idade = %s,
                peso = %s, id_tutor = %s, cuidados_especiais = %s, 
                descricao = %s
            WHERE id_pets = %s
            """
            params = [
                nome, tipo, raca, idade or None,
                peso, id_tutor, cuidados_especiais, 
                descricao, id_pet
            ]
            message = 'Pet atualizado com sucesso!'
        else:  # Modo criação
            query = """
            INSERT INTO pets (
                nome, tipo, raca, idade, peso, 
                id_tutor, cuidados_especiais, descricao, ativo, data_cadastro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            params = [
                nome, tipo, raca, idade or None,
                peso, id_tutor, cuidados_especiais, 
                descricao
            ]
            message = 'Pet cadastrado com sucesso!'
            
        try:
            execute_sql(query, params, False)
            messages.success(request, message)
        except Exception as e:
            messages.error(request, f'Erro ao salvar pet: {str(e)}')
            print(f"Erro: {e}")

    return redirect('pets')

def listar_pets():
    # Query base
    query = """
    SELECT id_pets, p.nome, tipo, raca, idade, peso, cuidados_especiais, descricao, t.id_tutor, t.nome
    FROM pets p
    INNER JOIN tutor t ON p.id_tutor = t.id_tutor
    """
    
    pets_paginados = execute_sql(query, [], False)
    return pets_paginados