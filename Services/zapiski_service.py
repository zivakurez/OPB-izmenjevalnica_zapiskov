from Data.repository import Repo
from Data.models import Zapisek, Prenos
from datetime import datetime
from typing import List, Optional


class ZapisekService:
    def init(self):
        self.repo = Repo()

    def dodaj_zapisek(self, zapisek: Zapisek, id_uporabnika: int) -> bool:
        user = self.repo.dobi_uporabnika(id_uporabnika)
        if user is None or user.role != 'admin':
            return False

        if zapisek.datum_objave is None:
            zapisek.datum_objave = datetime.now()

        self.repo.dodaj_zapisek(zapisek)
        return True

    def prenesi_zapisek(self, id_uporabnika: int, id_zapiska: int) -> bool:
        zapiski = self.repo.dobi_zapiske()
        if not any(z.id_zapiska == id_zapiska for z in zapiski):
            return False

        prenosi = self.repo.dobi_prenose_uporabnika(id_uporabnika)
        if any(p.id_zapiska == id_zapiska for p in prenosi):
            return False

        prenos = Prenos(id_uporabnika=id_uporabnika, id_zapiska=id_zapiska)
        self.repo.dodaj_prenos(prenos)
        return True

    def pridobi_vse_zapiske(self) -> List[Zapisek]:
        return self.repo.dobi_zapiske()

    def pridobi_prenesene_zapiske(self, id_uporabnika: int) -> List[Zapisek]:
        prenosi = self.repo.dobi_prenose_uporabnika(id_uporabnika)
        preneseni_idji = [p.id_zapiska for p in prenosi]
        vsi_zapiski = self.repo.dobi_zapiske()
        return [z for z in vsi_zapiski if z.id_zapiska in preneseni_idji]