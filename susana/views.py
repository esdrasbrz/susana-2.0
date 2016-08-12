from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from disciplinas.models import Disciplinas

# retorna para a página principal
@login_required(login_url='/login/')
def index(request):
    # listagem de todos as disciplinas
    disciplinas = Disciplinas.objects.all()

    return render(request, 'susana/index.html', {'disciplinas': disciplinas})
