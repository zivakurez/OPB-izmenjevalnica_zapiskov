import psycopg2
import psycopg2.extensions
import psycopg2.extras
import os
from typing import List, Optional

from models import (
    Uporabnik, UporabnikDto, Zapisek, Komentar, Predmet, Profesor,
    Faks, Prenos, PredmetFaks, ProfesorFaks, ProfesorPredmet
)


psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

# Nastaviš povezavo do baze prek okolja ali ročno
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
        import auth  # datoteka z auth.py ali auth_public.py
        self.conn = psycopg2.connect(
            database=auth.db,
            host=auth.host,
            user=auth.user,
            password=auth.password,
            port=DB_PORT
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

   
    # Uporabniki

    def dobi_uporabnika(self, id_uporabnika: int) -> Optional[UporabnikDto]:
        self.cur.execute("""
            SELECT id_uporabnika, uporabnisko_ime, role
            FROM uporabnik
            WHERE id_uporabnika = %s
        """, (id_uporabnika,))
        row = self.cur.fetchone()
        return UporabnikDto.from_dict(row) if row else None

    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT INTO uporabnik (id_uporabnika, role, uporabnisko_ime, geslo, id_faksa)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            uporabnik.id_uporabnika,
            uporabnik.role,
            uporabnik.uporabnisko_ime,
            uporabnik.geslo,
            uporabnik.id_faksa
        ))
        self.conn.commit()


    # Zapiski
    def dobi_zapiske(self) -> List[Zapisek]:
        self.cur.execute("""
            SELECT * FROM zapisek
        """)
        return [Zapisek.from_dict(row) for row in self.cur.fetchall()]

    def dodaj_zapisek(self, z: Zapisek):
        self.cur.execute("""
            INSERT INTO zapisek (id_zapiska, stevilo_strani, vrsta_dokumenta, naslov, jezik, download_link, id_predmeta, id_uporabnika)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            z.id_zapiska, z.stevilo_strani, z.vrsta_dokumenta, z.naslov,
            z.jezik, z.download_link, z.id_predmeta, z.id_uporabnika
        ))
        self.conn.commit()


    # Komentarji

    def dobi_komentarje(self, id_zapiska: int) -> List[Komentar]:
        self.cur.execute("""
            SELECT * FROM komentar WHERE id_zapiska = %s
        """, (id_zapiska,))
        return [Komentar.from_dict(row) for row in self.cur.fetchall()]

    def dodaj_komentar(self, k: Komentar):
        self.cur.execute("""
            INSERT INTO komentar (id_komentarja, vsebina, id_zapiska, id_uporabnika)
            VALUES (%s, %s, %s, %s)
        """, (
            k.id_komentarja, k.vsebina, k.id_zapiska, k.id_uporabnika
        ))
        self.conn.commit()


    # Prenosi

    def dodaj_prenos(self, p: Prenos):
        self.cur.execute("""
            INSERT INTO prenosi (id_uporabnika, id_zapiska)
            VALUES (%s, %s)
        """, (p.id_uporabnika, p.id_zapiska))
        self.conn.commit()

    def dobi_prenose_uporabnika(self, id_uporabnika: int) -> List[Prenos]:
        self.cur.execute("""
            SELECT * FROM prenosi WHERE id_uporabnika = %s
        """, (id_uporabnika,))
        return [Prenos.from_dict(row) for row in self.cur.fetchall()]



    # Fakultete, predmeti, profesorji (po potrebi)

    def dobi_predmete(self) -> List[Predmet]:
        self.cur.execute("SELECT * FROM predmet")
        return [Predmet.from_dict(row) for row in self.cur.fetchall()]

    def dobi_profesorje(self) -> List[Profesor]:
        self.cur.execute("SELECT * FROM profesor")
        return [Profesor.from_dict(row) for row in self.cur.fetchall()]

    def dobi_fakse(self) -> List[Faks]:
        self.cur.execute("SELECT * FROM faks")
        return [Faks.from_dict(row) for row in self.cur.fetchall()]

    # zapri povezavo
    def zapri(self):
        self.cur.close()
        self.conn.close()