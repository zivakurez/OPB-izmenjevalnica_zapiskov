from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.zapiski_service import ZapisekService
import os
from bottle import post, request, response, redirect
from Data.repository import Repo

service = ZapisekService()

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

# Nastavi mapo s predlogami
from bottle import TEMPLATE_PATH
import os
#TEMPLATE_PATH.insert(0, os.path.abspath("Presentation/views"))

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

@get('/')
def index():
    zapiski = service.pridobi_zapiske_s_podatki()
    return template('zapiski.html', zapiski=zapiski)

@get('/moji-prenosi/<id_uporabnika:int>')
def moji_prenosi(id_uporabnika):
    preneseni_zapiski = service.pridobi_prenesene_zapiske(id_uporabnika)
    return template('prenosi.html', prenosi=preneseni_zapiski)

@get('/prijava')
def prikazi_prijavo():
    return template('prijava.html', napaka=None)


@post('/prijava')
def obdelaj_prijavo():
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')

    repo = Repo()
    uporabnik = repo.preveri_prijavo(uporabnisko_ime, geslo)

    if uporabnik:
        response.set_cookie("user_id", str(uporabnik.id_uporabnika), secret='skrivnost123')
        redirect('/profil')
    else:
        return template('prijava.html', napaka="Napačno uporabniško ime ali geslo")
    
@get('/profil')
def profil():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    repo = Repo()
    uporabnik = repo.dobi_uporabnika(int(user_id))
    zapiski = repo.dobi_zapiske_uporabnika_za_prikaz(int(user_id))
    prenosi = repo.dobi_prenose_uporabnika(int(user_id))

    return template('profil.html', uporabnik=uporabnik, zapiski=zapiski, prenosi=prenosi)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)





# from bottle import get, run, template, static_file, request
# from Services.zapiski_service import ZapisekService
# import os

# # Inicializacija servisa
# service = ZapisekService()

# from bottle import TEMPLATE_PATH
# TEMPLATE_PATH.insert(0, 'Presentation/views')

# # Privzete nastavitve
# SERVER_PORT = int(os.environ.get('BOTTLE_PORT', 8080))
# RELOADER = os.environ.get('BOTTLE_RELOADER', True)

# @get('/static/<filename:path>')
# def static(filename):
#     return static_file(filename, root='Presentation/static')

# @get('/')
# def index():
#     """
#     Domača stran z vsemi zapiski.
#     """
#     zapiski = service.pridobi_vse_zapiske()
#     return template('zapiski.html', zapiski=zapiski)

# @get('/moji-prenosi/<id_uporabnika:int>')
# def moji_prenosi(id_uporabnika):
#     """
#     Prikaz zapiskov, ki si jih je prenesel določen uporabnik.
#     """
#     preneseni_zapiski = service.pridobi_prenesene_zapiske(id_uporabnika)
#     return template('prenosi.html', prenosi=preneseni_zapiski)

# if __name__ == "__main__":
#     run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
