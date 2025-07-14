#from django.http import HttpResponse
from django.shortcuts import render, redirect
from tutores.views import listar_tutores, qtd_novos_tutores
from db_utils import execute_sql
from pets.views import listar_pets
from servicos.views import listar_servicos
from veterinarios.views import listar_veterinarios, obter_veterinario_edicao, atendimento_por_vet
from atendimentos.views import listar_atendimentos, listar_atendimnetos_hoje, atendimentos_essa_semana, faturamento, qtd_emergencia, obter_atendimento_edicao, dados_grafico

def Home(request):
    if not request.session.get('logado'):
        return redirect('login')
    return render(request, 'index.html',  {'nome_usuario': request.session.get('logado'), 'atendimentos': listar_atendimnetos_hoje, 'novos_clientes': qtd_novos_tutores, 'esta_semana': atendimentos_essa_semana, 'faturamento': faturamento, 'emergencias': qtd_emergencia, 'atendimento_vet': atendimento_por_vet, 'dados_grafico': dados_grafico})


def Login(request):
    return render(request, 'login.html')

def Tutores(request):
    tutores = listar_tutores(request)
    
    # Verifica se é uma ação de edição
    acao = request.GET.get('acao')
    tutor_edicao = None
    
    if acao == 'editar':
        tutor_id = request.GET.get('id')
        # Busca o tutor específico para edição
        query = """
        SELECT id_tutor, nome, cpf, email, telefone, data_nascimento, 
               endereco, tipo_conta, ativo
        FROM tutor
        WHERE id_tutor = %s
        """
        tutor_edicao = execute_sql(query, [tutor_id], fetchone=True)
    
    # Converte os tutores para lista de dicionários
    columns = ['id_tutor', 'nome', 'cpf', 'email', 'telefone', 
               'data_nascimento', 'endereco', 'tipo_conta', 'ativo']
    tutores_dict = [dict(zip(columns, tutor)) for tutor in tutores]
    
    return render(request, 'tutores.html', {
        'tutores': tutores_dict,
        'q': request.GET.get('q', ''),
        'status': request.GET.get('status', ''),
        'tutor_edicao': tutor_edicao,  # Dados do tutor para edição
        'acao': acao
    })


def Pets(request):
    pets = listar_pets()
    tutores = listar_tutores(request)
    acao = request.GET.get('acao')
    pet_edicao = None
    
    if acao == 'editar':
        id_pet = request.GET.get('id')
        # Busca o tutor específico para edição
        query = """
        SELECT id_pets, p.nome, tipo, raca, idade, peso, cuidados_especiais, descricao, t.nome, t.id_tutor
        FROM public.pets p
        INNER JOIN tutor t ON p.id_tutor = t.id_tutor
        WHERE id_pets = %s
        """
        pet_edicao = execute_sql(query, [id_pet], fetchone=True)
    return render(request, 'pets.html', {'pets': pets, 'tutores': tutores, 'pet_edicao': pet_edicao})

def Atendimentos(request):
    acao = request.GET.get('acao')
    edicao = None
    if acao == 'editar':
       edicao = obter_atendimento_edicao(request)
    return render(request, 'atendimentos.html', {'pets': listar_pets(), 'veterinarios': listar_veterinarios(request), 'atendimentos': listar_atendimentos(), 'atendimento_edicao': edicao })

def Servico(request):
    acao = request.GET.get('acao')
    id_servico = request.GET.get('id')
    servicos = listar_servicos()
    servicos_edicao = None

    if acao == 'editar':
        # Busca o tutor específico para edição
        query = """
        SELECT id_servico, nome, descricao, valor
        FROM servico
        WHERE id_servico = %s
        """
        servicos_edicao = execute_sql(query, [id_servico],True)
    return render(request, 'servicos.html', {'servicos': servicos, 'servico_edicao': servicos_edicao })

def Veterinario(request):
    acao = request.GET.get('acao')

    vet = None
    if acao == 'editar':
        vet = obter_veterinario_edicao(request)

    return render(request, 'veterinarios.html', {'servicos': listar_servicos, 'veterinarios': listar_veterinarios(request), 'veterinario_edicao': vet })

def Financeiro(request):
    return render(request, 'financeiro.html')

