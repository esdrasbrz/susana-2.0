from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from login.user_tests import *

"""
Lista todas as disciplinas para possíveis alterações
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def disciplinas(request):
    return render(request, 'labs/labs.html')