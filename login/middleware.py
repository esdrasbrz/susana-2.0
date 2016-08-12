from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth

# classe responsavel por dar logout automatico em usuarios inativos
class AutoLogout:
    def process_request(self, request):
        # verifica se o usuario esta logado
        if request.user.is_authenticated():
            try:
                # verifica se ultrapassou o limite de tempo
                if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                    # desloga o usuario
                    auth.logout(request)

                    del request.session['last_touch']
                    return
            except KeyError:
                pass

        # atualiza a ultima submissao
        request.session['last_touch'] = datetime.now()