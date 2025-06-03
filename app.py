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

@get('/vsi_zapiski')
def index():
    zapiski = service.pridobi_zapiske_s_podatki()
    return template('zapiski.html', zapiski=zapiski)

@get('/moji-prenosi/<id_uporabnika:int>')
def moji_prenosi(id_uporabnika):
    preneseni_zapiski = service.pridobi_prenesene_zapiske(id_uporabnika)
    return template('prenosi.html', prenosi=preneseni_zapiski)

@get('/')
def zacetna_stran():
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

@get('/isci-zapiske')
def isci_zapiske():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    predmet = request.query.get('predmet') or None
    naslov = request.query.get('naslov') or None
    fakulteta = request.query.get('fakulteta') or None
    vrsta = request.query.get('vrsta') or None
    profesor = request.query.get('profesor') or None

    zapiski = service.filtriraj_zapiske(predmet, naslov, fakulteta, vrsta, profesor)

    return template('iskanje_zapiskov.html', zapiski=zapiski)


@get('/moji-zapiski')
def moji_zapiski():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    repo = Repo()
    zapiski = repo.dobi_zapiske_uporabnika_za_prikaz(int(user_id))
    return template('moji_zapiski.html', zapiski=zapiski)


if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)


