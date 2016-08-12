from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

"""
Renderiza o template para cadastrar um novo usuário
"""
def cadastro(request):
    return render(request, 'login/cadastro.html')

"""
Salva um novo usuário
"""
def salvar_usuario(request):
    user = User()

    # recebe os dados
    user.first_name = request.POST['nome']
    user.last_name = request.POST['sobrenome']
    user.email = request.POST['email']
    user.username = request.POST['usuario']
    user.password = request.POST['senha']
    senha_confirmacao = request.POST['senha_confirmacao']

    # verifica se as senhas não são equivalentes
    if user.password != senha_confirmacao:
        # renderiza com mensagem de erro a tela de cadastro
        messages.error(request, 'As senhas não são equivalentes!')
        return render(request, 'login/cadastro.html', {'user': user})
    else:
        try:
            # cria o usuário
            user = User.objects.create_user(user.username, user.email, user.password, first_name=user.first_name, last_name=user.last_name)
            user.save()

            messages.success(request, 'Usuário salvo com sucesso!')
            return index(request)
        except:
            messages.warning(request, "Nome de usuário indisponível!")
            return render(request, 'login/cadastro.html', {'user': user})

"""
Renderiza a tela para alterar login
"""
@login_required(login_url='/login/')
def alterar_login(request):
    return render(request, 'login/alterarLogin.html')

"""
Salva o novo login
"""
@login_required(login_url='/login/')
def salvar_login(request):
    user = User()

    # recebe os dados
    user.first_name = request.POST['nome']
    user.last_name = request.POST['sobrenome']
    user.email = request.POST['email']
    user.username = request.POST['usuario']
    user.password = request.POST['senha']
    senha_confirmacao = request.POST['senha_confirmacao']

    # verifica se deseja alterar senha
    if 'alterar_senha' in request.POST:
        # verifica se os campos não foram preenchidos
        if not user.password or not senha_confirmacao:
            messages.warning(request, "Os campos de acesso devem ser preenchidos!")
        elif senha_confirmacao != user.password: # senhas não condizentes
            messages.error(request, 'As senhas não são equivalentes!')
            return render(request, 'login/alterarLogin.html', {'user': user, 'alterar_senha': True})
        else:
            # altera o usuário
            request.user.first_name = user.first_name
            request.user.last_name = user.last_name
            request.user.email = user.email

            # seta a nova senha
            request.user.set_password(user.password)

            # salva o usuario
            request.user.save()

            messages.success(request, "Usuário salvo com sucesso!")

        return render(request, 'login/alterarLogin.html', {'user': user, 'alterar_senha': True})
    else:
        # seta os novos campos no usuário da session
        request.user.first_name = user.first_name
        request.user.last_name = user.last_name
        request.user.email = user.email

        # salva o usuário e renderiza com sucesso
        request.user.save()

        messages.success(request, "Usuário salvo com sucesso!")
        return render(request, 'login/alterarLogin.html')