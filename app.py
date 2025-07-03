from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.zapiski_service import ZapisekService
from Services.komentar_service import KomentarService
import os
from bottle import post, request, response, redirect
from Data.repository import Repo
from Data.models import Zapisek, Komentar

service = ZapisekService()
komentar_service = KomentarService()


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

@get('/moji-prenosi')
def moji_prenosi():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    repo = Repo()
    preneseni_zapiski = repo.dobi_prenose_uporabnika(int(user_id))
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
    

@get('/odjava')
def odjava():
    response.delete_cookie("user_id")
    redirect('/')


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
    fakulteta = request.query.get('fakulteta') or None
    program = request.query.get('program') or None
    profesor = request.query.get('profesor') or None

    zapiski = service.filtriraj_zapiske(predmet, fakulteta, program, profesor)

    return template('iskanje_zapiskov.html', zapiski=zapiski)


@get('/moji-zapiski')
def moji_zapiski():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    repo = Repo()
    zapiski = repo.dobi_zapiske_uporabnika_za_prikaz(int(user_id))
    return template('moji_zapiski.html', zapiski=zapiski)


@get('/dodaj-zapisek')
def prikazi_dodaj_zapisek():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    predmeti = service.repo.vrni_vse_predmete()
    programi = service.repo.vrni_vse_programe()
    fakultete = service.repo.vrni_vse_fakultete()
    imena_profesorjev = service.repo.vrni_vsa_imena_profesorjev()
    priimki_profesorjev = service.repo.vrni_vse_priimke_profesorjev()

    return template('dodaj_zapisek.html',
                    predmeti=predmeti,
                    programi=programi,
                    fakultete=fakultete,
                    imena_profesorjev=imena_profesorjev,
                    priimki_profesorjev=priimki_profesorjev,
                    napaka=None)

@post('/dodaj-zapisek')
def shrani_zapisek():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    try:
        zapisek = Zapisek(
            naslov=request.forms.get('naslov'),
            stevilo_strani=int(request.forms.get('stevilo_strani')),
            vrsta_dokumenta=request.forms.get('vrsta_dokumenta'),
            jezik=request.forms.get('jezik'),
            download_link=request.forms.get('download_link')
        )
        
        fl = request.files.get("datoteka")
        
        fl.save(f"Data/zapiski/{fl.filename}")
        predmet = request.forms.get('predmet')
        faks = request.forms.get('faks')
        program = request.forms.get('program')
        letnik = int(request.forms.get('letnik'))

        ime_profesorja = request.forms.get('ime_profesorja')
        priimek_profesorja = request.forms.get('priimek_profesorja')

        uspeh = service.dodaj_zapisek(
            zapisek,
            int(user_id),
            predmet.strip().lower().capitalize(),
            faks.strip().lower().capitalize(),
            ime_profesorja.strip().lower().capitalize(),
            priimek_profesorja.strip().lower().capitalize(),
            letnik,
            program.strip().lower().capitalize()
        )

        if uspeh:
            redirect('/profil')
        else:
            return template('dodaj_zapisek.html', napaka="Napaka pri dodajanju zapiska.")
    except Exception as e:
        return template('dodaj_zapisek.html', napaka=f"Napaka: {str(e)}")
    
@get('/zapisek/<id_zapiska:int>')
def prikazi_zapisek(id_zapiska):
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    uporabnik = service.repo.dobi_uporabnika(user_id) if user_id else None

    zapisek = service.repo.dobi_zapisek_s_podatki(id_zapiska)
    komentarji = service.repo.dobi_komentarje(id_zapiska)

    return template('zapisek.html',
                    zapisek=zapisek,
                    komentarji=komentarji,
                    uporabnik=uporabnik,
                    napaka=None)

@post('/dodaj-komentar/<id_zapiska:int>')
def dodaj_komentar(id_zapiska):
    uporabnik = request.get_cookie("user_id", secret='skrivnost123')
    if not uporabnik:
        redirect('/prijava')

    besedilo = request.forms.get('besedilo')

    komentar_service.dodaj_komentar(besedilo, id_zapiska, uporabnik)

    redirect(f'/zapisek/{id_zapiska}')


@post('/izbrisi-komentar/<id_komentarja:int>')
def izbrisi_komentar(id_komentarja):
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    komentar = service.repo.dobi_komentar(id_komentarja)
    if komentar and (komentar.id_uporabnika == int(user_id) or service.repo.je_admin(user_id)):
        service.repo.izbrisi_komentar(id_komentarja)

    redirect(f"/zapisek/{komentar.id_zapiska}")

@post('/izbrisi-zapisek/<id_zapiska:int>')
def izbrisi_zapisek(id_zapiska):
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    zapisek = service.repo.dobi_zapisek_po_id(id_zapiska)
    if not zapisek:
        return "Zapisek ne obstaja."

    if zapisek.id_uporabnika != int(user_id) and not service.repo.je_admin(user_id):
        return "Nimate dovoljenja za izbris tega zapiska."

    service.repo.izbrisi_zapisek(id_zapiska)
    redirect('/moji-zapiski')

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)



