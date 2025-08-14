from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user, route
from Services.zapiski_service import ZapisekService
from Services.komentar_service import KomentarService
from Services.auth_service import AuthService
import os
from bottle import post, request, response, redirect, abort, static_file
from Data.models import Zapisek, Komentar
import uuid

service = ZapisekService()
komentar_service = KomentarService()
auth = AuthService()

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')

@get('/vsi_zapiski')
def index():
    zapiski = service.pridobi_vse_zapiske_za_prikaz()
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

    preneseni_zapiski = service.pridobi_prenesene_zapiske(int(user_id))
    return template('prenosi.html', prenosi=preneseni_zapiski)

@get('/')
def zacetna_stran():
    return template('prijava.html', napaka=None)

@get("/prijava")
def prijava_get():
    return template("prijava.html", napaka=None)


@post('/prijava')
def obdelaj_prijavo():
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')

    uporabnik = auth.prijavi_uporabnika(uporabnisko_ime, geslo)  # <-- uporabi auth_service

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

    uporabnik = auth.pridobi_uporabnika_po_id(int(user_id))
    zapiski = service.pridobi_zapiske_uporabnika_za_prikaz(int(user_id))
    prenosi = service.pridobi_prenesene_zapiske(int(user_id))

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

    zapiski = service.pridobi_zapiske_uporabnika_za_prikaz(int(user_id))
    return template('moji_zapiski.html', zapiski=zapiski)

def _ctx_dodaj_zapisek():
    return dict(
        predmeti=service.vrni_vse_predmete(),
        programi=service.vrni_vse_programe(),
        fakultete=service.vrni_vse_fakultete(),
        imena_profesorjev=service.vrni_vsa_imena_profesorjev(),
        priimki_profesorjev=service.vrni_vse_priimke_profesorjev(),
        napaka=None,
    )

@get('/dodaj-zapisek')
def prikazi_dodaj_zapisek():
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    predmeti = service.vrni_vse_predmete()
    programi = service.vrni_vse_programe()
    fakultete = service.vrni_vse_fakultete()
    imena_profesorjev = service.vrni_vsa_imena_profesorjev()
    priimki_profesorjev = service.vrni_vse_priimke_profesorjev()

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
        fl = request.files.get("datoteka")
        if not fl or not fl.filename:
            ctx = _ctx_dodaj_zapisek()
            ctx['napaka'] = "Niste izbrali datoteke."
            return template('dodaj_zapisek.html', **ctx)

        #ustvari unikatno ime (ohrani končnico)
        ext = os.path.splitext(fl.filename)[1]  #npr. '.pdf'
        unique_name = f"{uuid.uuid4()}{ext}"

        #shrani datoteko
        save_dir = os.path.join("Data", "zapiski")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, unique_name)
        fl.save(save_path)

        #sestavi objekt zapiska z novim imenom datoteke
        zapisek = Zapisek(
            naslov=request.forms.get('naslov'),
            stevilo_strani=int(request.forms.get('stevilo_strani')),
            vrsta_dokumenta=request.forms.get('vrsta_dokumenta'),
            jezik=request.forms.get('jezik'),
            download_link=unique_name
        )

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

    except Exception as e:
        ctx = _ctx_dodaj_zapisek()
        ctx['napaka'] = f"{e.__class__.__name__}: {e}"
        return template('dodaj_zapisek.html', **ctx)

    if uspeh:
        redirect('/profil')
    else:
        ctx = _ctx_dodaj_zapisek()
        ctx['napaka'] = "Napaka pri dodajanju zapiska."
        return template('dodaj_zapisek.html', **ctx)


  
@get('/zapisek/<id_zapiska:int>')
def prikazi_zapisek(id_zapiska):
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    uporabnik = auth.pridobi_uporabnika_po_id(user_id) if user_id else None

    zapisek = service.pridobi_zapisek_s_podatki(id_zapiska)
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

    komentar = komentar_service.dobi_komentar(id_komentarja)
    if komentar and (komentar.id_uporabnika == int(user_id) or service.repo.je_admin(user_id)):
        komentar_service.izbrisi_komentar(id_komentarja, int(user_id))

    redirect(f"/zapisek/{komentar.id_zapiska}")

@post('/izbrisi-zapisek/<id_zapiska:int>')
def izbrisi_zapisek(id_zapiska):
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')

    zapisek = service.pridobi_zapisek_po_id(id_zapiska)
    if not zapisek:
        return "Zapisek ne obstaja."

    if zapisek.id_uporabnika != int(user_id) and not service.repo.je_admin(user_id):
        return "Nimate dovoljenja za izbris tega zapiska."

    #najprej izbriše datoteko s strežnika
    if zapisek.download_link:
        pot = os.path.join("Data", "zapiski", zapisek.download_link)
        if os.path.exists(pot):
            os.remove(pot)

    #nato izbriše zapis iz baze
    service.izbrisi_zapisek(id_zapiska, int(user_id))

    redirect('/moji-zapiski')

 
@get("/registracija")
def registracija_get():
    fakultete = service.vrni_vse_fakultete()  
    return template("registracija", fakultete=fakultete)

@post("/registracija")
def registracija_post():
    uporabnisko_ime = request.forms.get("uporabnisko_ime")
    geslo1 = request.forms.get("geslo1")
    geslo2 = request.forms.get("geslo2")
    ime_faksa = request.forms.get("faks")

    if geslo1 != geslo2:
        return "Gesli se ne ujemata."

    if auth.obstaja_uporabnik(uporabnisko_ime):
        return "Uporabniško ime je že zasedeno."

    id_faksa = service.dobi_id_faksa_po_imenu(ime_faksa)
    if id_faksa is None:
        return "Izbran faks ne obstaja."

    auth.dodaj_uporabnika(uporabnisko_ime, "user", geslo1, id_faksa)
    redirect("/prijava")

@get('/prenesi/<id_zapiska:int>')
def prenesi_zapisek(id_zapiska):
    user_id = request.get_cookie("user_id", secret='skrivnost123')
    if not user_id:
        redirect('/prijava')
        
    z = service.pridobi_zapisek_po_id(id_zapiska)
    if not z or not z.download_link:
        abort(404, "Zapisek ali datoteka ne obstaja.")
        
    service.zabelezi_prenos(int(user_id), id_zapiska)

    root_dir = os.path.join(os.getcwd(), 'Data', 'zapiski')
    #vrni kot prenos
    return static_file(z.download_link, root=root_dir, download=z.download_link)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)



