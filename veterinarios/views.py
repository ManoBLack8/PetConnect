from django.shortcuts import render, redirect
from django.contrib import messages
from db_utils import execute_sql,update
from datetime import datetime

def formulario_veterinarios(request):
    """Processa o formulário de criação/edição de veterinários"""
    if request.method == 'POST':
        # Obter dados do formulário
        id_veterinario = request.POST.get('id_veterinario')
        nome = request.POST.get('nome')
        crmv = request.POST.get('crmv')
        especialidade = request.POST.get('especialidade')
        status = request.POST.get('status')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco', '')

        # Validações básicas
        if not all([nome, crmv, especialidade, status, telefone, email]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('veterinarios')

        if id_veterinario:  # Modo edição
            query = """
            UPDATE veterinario SET
                nome = %s, crmv = %s, especialidade = %s, status = %s,
                telefone = %s, email = %s, endereco = %s
            WHERE id_veterinario = %s
            """
            params = [
                nome, crmv, especialidade, status,
                telefone, email, endereco, id_veterinario
            ]
            update(query, params)
            messages.success(request, 'Veterinário atualizado com sucesso!')
        else:  # Modo criação
            query = """
            INSERT INTO veterinario (
                nome, crmv, especialidade, status, telefone, email, endereco
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            returning id_veterinario
            """
            params = [
                nome, crmv, especialidade, status,
                telefone, email, endereco
            ]
            execute_sql(query, params)
            messages.success(request, 'Veterinário cadastrado com sucesso!')

        return redirect('veterinarios')

    # Se for GET, apenas renderiza o template (o modal será tratado no template)
    return redirect('veterinarios')

def listar_veterinarios(request):
    """Lista todos os veterinários com possíveis filtros"""
    # Obter parâmetros de filtro
    busca = request.GET.get('q', '')
    especialidade = request.GET.get('especialidade', '')
    status = request.GET.get('status', '')

    # Construir query base
    query = """
    SELECT id_veterinario, nome, telefone, email, endereco, especialidade, crmv, status
    FROM veterinario
    WHERE 1=1
    """
    
    params = []
    
    # Aplicar filtros
    if busca:
        query += " AND (LOWER(nome) LIKE LOWER(%s) OR LOWER(crmv) LIKE LOWER(%s) OR LOWER(email) LIKE LOWER(%s))"
        params.extend([f"%{busca}%", f"%{busca}%", f"%{busca}%"])
    
    if especialidade:
        query += " AND especialidade ILIKE %s"
        params.append(especialidade)
    
    if status:
        query += " AND status = %s"
        params.append(status)

    # Ordenação padrão
    query += " ORDER BY nome ASC"
    
    veterinarios = execute_sql(query, params, False)

    
    return veterinarios

def excluir_veterinario(request, id_veterinario):
    """Exclui um veterinário"""
    if request.method == 'POST':
        try:
            query = "DELETE FROM veterinario WHERE id_veterinario = %s"
            execute_sql(query, [id_veterinario])
            messages.success(request, 'Veterinário excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir veterinário: {str(e)}')
    
    return redirect('veterinarios')

def obter_veterinario_edicao(request):
    """Retorna os dados de um veterinário para edição (usado pelo modal)"""
    if request.method == 'GET' and 'id' in request.GET:
        id_veterinario = request.GET.get('id')
        query = """
        SELECT id_veterinario, nome, crmv, especialidade, status, telefone, email, endereco
        FROM veterinario
        WHERE id_veterinario = %s
        """
        veterinario = execute_sql(query, [id_veterinario], fetchone=True)
    return veterinario

def atendimento_por_vet():
    query ="""
    SELECT 
        v.nome,
        COUNT(*)
    FROM atendimento a
    RIGHT JOIN veterinario v ON a.id_veterinario = v.id_veterinario
    WHERE DATE(a.dt_inicio_atendimento) >= CURRENT_DATE - INTERVAL '30 days'
    AND a.status = 'CONCLUIDO'
    GROUP BY v.nome
    """
    veterinario = execute_sql(query, [], fetchone=False)
    return veterinario