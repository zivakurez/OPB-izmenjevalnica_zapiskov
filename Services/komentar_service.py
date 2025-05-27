from Data.repository import Repo
from Data.models import Komentar
from datetime import datetime
from typing import List, Optional


class KomentarService:
    def __init__(self):
        self.repo = Repo()

def dodaj_komentar(self, vsebina: str, id_zapiska: int, id_uporabnika: int) -> bool:
    komentar = Komentar(
        vsebina=vsebina,
        id_zapiska=id_zapiska,
        id_uporabnika=id_uporabnika,
        id_nadkomentarja=None
    )
    self.repo.dodaj_komentar(komentar)
    return True


    def odgovori_na_komentar(self, vsebina: str, id_nadkomentarja: int, id_uporabnika: int) -> bool:
        nadkomentar = self.repo.dobi_komentar(id_nadkomentarja)
        if not nadkomentar:
            return False

        komentar = Komentar(
            vsebina=vsebina,
            id_zapiska=nadkomentar.id_zapiska,
            id_uporabnika=id_uporabnika,
            id_nadkomentarja=id_nadkomentarja
        )
        self.repo.dodaj_komentar(komentar)
        return True

    def komentarji_za_zapisek(self, id_zapiska: int) -> List[Komentar]:
        # samo glavni komentarji (ne odgovori)
        komentarji = self.repo.dobi_komentarje(id_zapiska)
        return [k for k in komentarji if k.id_nadkomentarja is None]

    def poglej_odgovore_na_komentar(self, id_komentarja: int) -> List[Komentar]:
        return self.repo.dobi_odgovore(id_komentarja)

    def komentarji_uporabnika(self, id_uporabnika: int) -> List[Komentar]:
        return self.repo.dobi_komentarje_uporabnika(id_uporabnika)

    def izbrisi_komentar(self, id_komentarja: int, id_uporabnika: int) -> bool:
        komentar = self.repo.dobi_komentar(id_komentarja)
        if not komentar:
            return False

        prijavljeni = self.repo.dobi_uporabnika(id_uporabnika)
        if komentar.id_uporabnika == id_uporabnika or prijavljeni.role == 'admin':
            self.repo.izbrisi_komentar(id_komentarja)
            return True
        return False
