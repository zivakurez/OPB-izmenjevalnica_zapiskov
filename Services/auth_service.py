from repository import Repo
from models import Uporabnik, UporabnikDto
import bcrypt
from datetime import date
from typing import Optional


class AuthService:
    def __init__(self):
        self.repo = Repo()

    def dodaj_uporabnika(self, uporabnisko_ime: str, role: str, geslo: str, id_faksa: int) -> UporabnikDto:
        #kodiramo geslo v bajte
        geslo_bytes = geslo.encode('utf-8')

        #ustvarimo salt in hash
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(geslo_bytes, salt)

        #pripravimo objekt
        uporabnik = Uporabnik(
            id_uporabnika=0, 
            role=role,
            uporabnisko_ime=uporabnisko_ime,
            geslo=password_hash.decode('utf-8'),
            id_faksa=id_faksa
        )

        #shrani v bazo
        self.repo.dodaj_uporabnika(uporabnik)

        #vrni DTO
        return UporabnikDto(
            id_uporabnika=uporabnik.id_uporabnika,
            uporabnisko_ime=uporabnik.uporabnisko_ime,
            role=uporabnik.role
        )

    def obstaja_uporabnik(self, uporabnisko_ime: str) -> bool:
        user = self.repo.dobi_uporabnika_po_uporabniskem_imenu(uporabnisko_ime)
        return user is not None

    def prijavi_uporabnika(self, uporabnisko_ime: str, geslo: str) -> Optional[UporabnikDto]:
        user = self.repo.dobi_uporabnika_po_uporabniskem_imenu(uporabnisko_ime)
        if user is None:
            return None

        #preverimo geslo
        geslo_bytes = geslo.encode('utf-8')
        is_valid = bcrypt.checkpw(geslo_bytes, user.geslo.encode('utf-8'))

        if is_valid:
            return UporabnikDto(
                id_uporabnika=user.id_uporabnika,
                uporabnisko_ime=user.uporabnisko_ime,
                role=user.role
            )
        return None
