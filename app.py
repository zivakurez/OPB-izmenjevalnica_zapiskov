from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.zapiski_service import ZapisekService
import os

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
