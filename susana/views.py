from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# retorna para a página principal
@login_required(login_url='/login/')
def index(request):
    return render(request, 'susana/index.html', {})
