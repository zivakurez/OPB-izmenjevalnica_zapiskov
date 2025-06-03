from Data.repository import Repo
from Data.models import Zapisek, Prenos, Predmet
from datetime import datetime, date
from typing import List, Optional


class ZapisekService:
    def __init__(self):
        self.repo = Repo()

    def dodaj_zapisek(
        self,
        zapisek: Zapisek,
        id_uporabnika: int,
        ime_predmeta: str,
        ime_faksa: str,
        ime_profesorja: str,
        priimek_profesorja: str,
        letnik: int,
        izobrazevalni_program: str
    ) -> bool:
        user = self.repo.dobi_uporabnika(id_uporabnika)
        if not user:
            return False

        # Poišči faks
        faks = self.repo.dobi_faks_po_imenu(ime_faksa)
        if not faks:
            print("Napaka: Faks ne obstaja!")
            return False

        # Poišči predmet po imenu, programu, letniku in faksu
        predmet = self.repo.dobi_predmet_polno(
                ime_predmeta,
                izobrazevalni_program,
                letnik
                )

        if not predmet:
            # Predmet še ne obstaja → dodaj ga
            nov_predmet = Predmet(
                ime=ime_predmeta,
                izobrazevalni_program=izobrazevalni_program,
                letnik=letnik
            )
            
            # dodaj v bazo in pridobi ustvarjeni id
            id_predmeta = self.repo.dodaj_predmet(nov_predmet)

            # sestavi predmet objekt
            predmet = Predmet(
                id_predmeta=id_predmeta,
                ime=ime_predmeta,
                izobrazevalni_program=izobrazevalni_program,
                letnik=letnik
            )

            # poveži predmet in faks
            self.repo.dodaj_predmet_faks(predmet.id_predmeta, faks.id_faksa)


        # Preveri profesorja
        profesor = self.repo.dobi_profesor_po_imenu(ime_profesorja, priimek_profesorja)
        if not profesor:
            self.repo.dodaj_profesor(ime_profesorja, priimek_profesorja)
            profesor = self.repo.dobi_profesor_po_imenu(ime_profesorja, priimek_profesorja)

        # Poveži profesorja s predmetom
        self.repo.dodaj_profesor_predmet(profesor.id_profesorja, predmet.id_predmeta)
        self.repo.dodaj_profesor_faks(profesor.id_profesorja, faks.id_faksa)
        
        # Preveri, da so zahtevana polja v zapisku podana
        if zapisek.stevilo_strani is None or zapisek.stevilo_strani <= 0:
            print("Napaka: Število strani mora biti večje od 0.")
            return False
        if not zapisek.jezik:
            print("Napaka: Jezik je obvezen.")
            return False
        if not zapisek.vrsta_dokumenta:
            print("Napaka: Vrsta dokumenta je obvezna.")
            return False

        # Dodaj zapisek
        zapisek.id_predmeta = predmet.id_predmeta
        zapisek.id_uporabnika = id_uporabnika

        self.repo.dodaj_zapisek(zapisek)
        return True


    def prenesi_zapisek(self, id_uporabnika: int, id_zapiska: int) -> bool:
        zapisek = self.repo.dobi_zapisek_po_id(id_zapiska)
        if not zapisek:
            print("Zapisek ne obstaja.")
            return False

        prenosi = self.repo.dobi_prenose_uporabnika(id_uporabnika)
        if any(p.id_zapiska == id_zapiska for p in prenosi):
            print("Zapisek je že prenesen.")
            return False

        prenos = Prenos(id_uporabnika=id_uporabnika, id_zapiska=id_zapiska)
        self.repo.dodaj_prenos(prenos)
        return True


    def pridobi_vse_zapiske(self) -> List[Zapisek]:
        return self.repo.dobi_zapiske()

    def pridobi_prenesene_zapiske(self, id_uporabnika: int) -> List[Zapisek]:
        prenosi = self.repo.dobi_prenose_uporabnika(id_uporabnika)
        preneseni_idji = [p.id_zapiska for p in prenosi]
        return self.repo.dobi_zapiske_po_idjih(preneseni_idji)

    
    def izbrisi_zapisek(self, id_zapiska: int, id_uporabnika: int) -> bool:
        zapisek = self.repo.dobi_zapisek_po_id(id_zapiska)
        if not zapisek:
            print("Napaka: Zapisek ne obstaja!")
            return False

        uporabnik = self.repo.dobi_uporabnika(id_uporabnika)
        if not uporabnik:
            print("Napaka: Uporabnik ne obstaja!")
            return False

        if zapisek.id_uporabnika == id_uporabnika or uporabnik.role == "admin":
            self.repo.izbrisi_komentarje_zapiska(id_zapiska)
            self.repo.izbrisi_prenose_zapiska(id_zapiska)
            self.repo.izbrisi_zapisek(id_zapiska)
            return True

        print("Napaka: Nimate pravice za izbris tega zapiska.")
        return False
    
    def pridobi_zapiske_s_podatki(self) -> List[dict]:
        return self.repo.dobi_zapiske_za_prikaz()
    
    def filtriraj_zapiske(self, predmet, naslov, fakulteta, vrsta, profesor):
        return self.repo.filtriraj_zapiske(predmet, naslov, fakulteta, vrsta, profesor)

