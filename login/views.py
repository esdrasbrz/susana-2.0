from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

"""
Redireciona para a página de login e seta o next na session
"""
def index(request):
    # recebe o next, parametro para a pagina pos login
    try:
        next = request.GET['next']
    except:
        next = '/' # default next

    # verifica se o usuario ja esta logado
    if request.user.is_authenticated():
        # redireciona para o next
        return HttpResponseRedirect(next)

    # seta o next na session
    request.session['next'] = next

    return render(request, 'login/index.html', {})

"""
Verifica se o login esta correto e loga
"""
def check_login(request):
    username = request.POST['username']
    password = request.POST['password']

    # recebe o next da session
    next = request.session['next']

    # checa o usuario
    user = authenticate(username=username, password=password)

    # verifica se pode logar
    if user is not None:
        if user.is_active:
            # realiza o login
            login(request, user)

            # adiciona mensagem
            messages.success(request, "Login efetuado com sucesso!")

            # redireciona para next
            return HttpResponseRedirect(next)
        else:
            # envia mensagem de usuário inativo
            messages.warning(request, "Usuário inativo!")
            return render(request, 'login/index.html', {})

    # retorna erro de usuario invalido
    messages.error(request, "Usuário ou senha inválidos!")
    return render(request, 'login/index.html', {})

"""
Desloga o usuário
"""
def logout_view(request):
    # recebe o next do get
    try:
        next = request.GET['next']
    except:
        next = '/' # next padrao

    request.session.flush()

    messages.success(request, "Logout efetuado com sucesso!")

    return HttpResponseRedirect(next)