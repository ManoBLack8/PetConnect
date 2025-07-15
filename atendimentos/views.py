from django.shortcuts import render, redirect
from django.contrib import messages
from db_utils import execute_sql, update
from datetime import datetime

def formulario_atendimento(request):
    """Processa o formulário de criação/edição de atendimentos"""
    if request.method == 'POST':
        print(request.POST.get('pet'))
        # Obter dados do formulário
        id_atendimento = request.POST.get('id_atendimento')
        tipo = request.POST.get('tipo')
        status = request.POST.get('status')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        pet_id = request.POST.get('pet')
        nivel = request.POST.get('nivel')
        id_servico = request.POST.get('servico')
        veterinario_id = request.POST.get('veterinario')
        observacoes = request.POST.get('observacoes', '')
        concluir = request.POST.get('concluir') == '1'

        # Se estiver concluindo, atualiza o status
        if concluir:
            status = 'CONCLUIDO'

        if id_atendimento:  # Modo edição
            query = """
            UPDATE atendimento SET
                tipo = %s, status = %s, dt_inicio_atendimento = %s, dt_fim_atendimento = %s,
                id_pets = %s, id_veterinario = %s, observacao = %s, id_servico= %s
            WHERE id_atendimento = %s
            RETURNING  id_atendimento
            """
            params = [
                nivel, status, data_inicio, data_fim,
                int(pet_id), int(veterinario_id), observacoes,id_servico, id_atendimento
            ]
            update(query, params)
            message = 'Atendimento atualizado com sucesso!'
            messages.success(request, message)
        else:  # Modo criação
            query = """
            INSERT INTO atendimento (
                tipo, status, dt_inicio_atendimento, dt_fim_atendimento, id_pets,
                id_veterinario, observacao, id_servico
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING  id_atendimento
            """
            params = [
                nivel, status, data_inicio, data_fim,
                pet_id, veterinario_id, observacoes, id_servico
            ]
            atendimento = execute_sql(query, params)
            if atendimento:
                message = 'Atendimento cadastrado com sucesso!'
            else: 
                message = 'Erro ao cadastrar'   
            messages.success(request, message)

    return redirect('atendimentos')

def listar_atendimentos():
    query = """
    SELECT 
        a.id_atendimento id,
        a.dt_inicio_atendimento,
		p.nome pet,
		t.nome tutor,
		a.tipo tipo,
		v.nome vet,
        a.status status
    FROM atendimento a
    JOIN pets p ON a.id_pets = p.id_pets
    JOIN tutor t ON p.id_tutor = t.id_tutor
    JOIN veterinario v ON a.id_veterinario = v.id_veterinario
    WHERE 1=1
    """
    
    params = []
    
    atendimentos = execute_sql(query, params, False)
    return atendimentos

def obter_atendimento_edicao(request):
    """Retorna os dados de um veterinário para edição (usado pelo modal)"""
    if request.method == 'GET' and 'id' in request.GET:
        id_atendimento = request.GET.get('id')
        query = """
        SELECT 
            a.id_atendimento,
            a.dt_inicio_atendimento,
            p.nome pet,
            t.nome tutor,
            a.tipo tipo,
            v.nome vet,
            a.status status,
            p.id_pets,
            v.id_veterinario,
            a.observacao,
            a.id_servico
        FROM atendimento a
        JOIN pets p ON a.id_pets = p.id_pets
        JOIN tutor t ON p.id_tutor = t.id_tutor
        JOIN veterinario v ON a.id_veterinario = v.id_veterinario
        LEFT JOIN servico s ON a.id_servico = s.id_servico
        WHERE a.id_atendimento = %s
        """
        atendimento = execute_sql(query, [id_atendimento], fetchone=True)
    return atendimento

def listar_atendimnetos_hoje():
    query = """
    SELECT 
        a.id_atendimento id,
        TO_CHAR(a.dt_inicio_atendimento, 'HH24:MI') AS hora_inicio,
        a.dt_inicio_atendimento,
        p.nome pet,
        t.nome tutor,
        a.tipo tipo,
        v.nome vet,
        a.status status
    FROM atendimento a
    INNER JOIN pets p ON a.id_pets = p.id_pets
    JOIN tutor t ON p.id_tutor = t.id_tutor
    JOIN veterinario v ON a.id_veterinario = v.id_veterinario
    WHERE DATE(a.dt_inicio_atendimento) = CURRENT_DATE
    AND a.status = 'PENDENTE'
    ORDER BY a.dt_inicio_atendimento ASC
    """
    
    params = []
    
    atendimentos = execute_sql(query, params, False)
    return atendimentos

def atendimentos_essa_semana():
    query = """
    SELECT 
	    COUNT(*)
    FROM atendimento a
    JOIN pets p ON a.id_pets = p.id_pets
    JOIN tutor t ON p.id_tutor = t.id_tutor
    JOIN veterinario v ON a.id_veterinario = v.id_veterinario
    WHERE a.dt_inicio_atendimento >= CURRENT_DATE - INTERVAL '7 days';
    """
    atendimentos = execute_sql(query, [], True)
    return atendimentos

def qtd_emergencia():
    query = """
    SELECT 
        COUNT(*)
    FROM atendimento a
    WHERE DATE(a.dt_inicio_atendimento) = CURRENT_DATE
    AND a.tipo ILIKE 'EMERGENCIA';
    """
    atendimentos = execute_sql(query, [], True)
    return atendimentos

def faturamento():
    query="""
    SELECT 
        CASE 
            WHEN SUM(s.valor) IS NULL OR SUM(s.valor) < 1 THEN '0,00'
            ELSE TO_CHAR(SUM(s.valor), 'FM999G990D00')
        END AS total_valor_emergencia
    FROM atendimento a
    INNER JOIN servico s ON a.id_servico = s.id_servico
    WHERE DATE(a.dt_inicio_atendimento) = CURRENT_DATE
    AND a.status = 'CONCLUIDO';
    """
    atendimentos = execute_sql(query, [], True)
    return atendimentos

def dados_grafico():
    query = """
    SELECT 
    p.tipo, 
    count(*)
    FROM
        atendimento a
    INNER JOIN pets p ON a.id_pets = p.id_pets
    WHERE a.dt_inicio_atendimento >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY p.tipo
    """
    atendimentos = execute_sql(query, [], False)
    return atendimentos