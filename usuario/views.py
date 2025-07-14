from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from db_utils import execute_sql
from django.contrib.auth import get_user_model

def sql_authenticate(username, password):
    # Consulta SQL direta para buscar o usuário
    query = """
    SELECT id_usuario,nome, email, senha 
    FROM usuario
    WHERE email = %s
    AND senha = %s
    """
    user_data = execute_sql(query, [username, password], True)
    if user_data:
        id, nome, email, senha = user_data
        if password == senha:
            return {
                'id': id,
                'nome': nome,
                'email': email
            }
    # Verifica a senha (Django armazena senhas com hash)
    return None

def login_view(request): #função inicial 
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')
        #Pega informações POST do formulario

        usuario = sql_authenticate(username, password)
        if usuario:  #verifica de Usuario Existe
            request.session['id_usuario'] = usuario['id']
            request.session['nome_usuario'] = usuario['nome']
            request.session['logado'] = True
            request.session.set_expiry(3600)
            return redirect('home')
        
        messages.error(request, "Credenciais inválidas") #caso não exista, manda mensagem e volta pra home
    
    return redirect('login')

def logout_view(request):
    request.session.flush()
    return redirect('home')