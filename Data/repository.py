import psycopg2
import psycopg2.extensions
import psycopg2.extras
import os
from typing import List, Optional

from Data.models import (
    Uporabnik, UporabnikDto, Zapisek, Komentar, Predmet, Profesor,
    Faks, Prenos, PredmetFaks, ProfesorFaks, ProfesorPredmet
)

import Data.auth_public as auth


psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

# Nastaviš povezavo do baze prek okolja ali ročno
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self):
          # datoteka z auth.py ali auth_public.py
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
    
    def dobi_zapisek_po_id(self, id_zapiska: int) -> Optional[Zapisek]:
        self.cur.execute("SELECT * FROM zapisek WHERE id_zapiska = %s", (id_zapiska,))
        row = self.cur.fetchone()
        return Zapisek.from_dict(row) if row else None
    
    def dobi_zapiske_po_idjih(self, idji: List[int]) -> List[Zapisek]:
        if not idji:
            return []
        sql = "SELECT * FROM zapisek WHERE id_zapiska = ANY(%s)"
        self.cur.execute(sql, (idji,))
        rows = self.cur.fetchall()
        return [Zapisek.from_dict(row) for row in rows]


    def dodaj_zapisek(self, z: Zapisek):
        self.cur.execute("""
            INSERT INTO zapisek (
                stevilo_strani, vrsta_dokumenta, naslov,
                jezik, download_link, id_predmeta, id_uporabnika
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            z.stevilo_strani, z.vrsta_dokumenta, z.naslov,
            z.jezik, z.download_link, z.id_predmeta, z.id_uporabnika
        ))
        self.conn.commit()
        
    def izbrisi_zapisek(self, id_zapiska: int):
        self.cur.execute("DELETE FROM zapisek WHERE id_zapiska = %s", (id_zapiska,))
        self.conn.commit()
        
    def dobi_zapiske_za_prikaz(self) -> List[dict]:
        self.cur.execute("""
            SELECT 
                z.id_zapiska,
                z.naslov,
                z.datum_objave,
                z.stevilo_strani,
                z.vrsta_dokumenta,
                z.jezik,
                z.download_link,

                u.uporabnisko_ime AS ime_uporabnika,
                p.ime AS ime_predmeta,
                p.izobrazevalni_program,
                f.ime AS ime_fakultete,
                f.univerza,
                string_agg(DISTINCT pr.ime || ' ' || pr.priimek, ', ') AS profesorji

            FROM zapisek z
            JOIN uporabnik u ON z.id_uporabnika = u.id_uporabnika
            JOIN predmet p ON z.id_predmeta = p.id_predmeta
            JOIN predmet_faks pf ON p.id_predmeta = pf.id_predmeta
            JOIN faks f ON pf.id_faksa = f.id_faksa
            LEFT JOIN profesor_predmet pp ON p.id_predmeta = pp.id_predmeta
            LEFT JOIN profesor pr ON pp.id_profesorja = pr.id_profesorja

            GROUP BY z.id_zapiska, u.uporabnisko_ime, p.ime, p.izobrazevalni_program, f.ime, f.univerza
            ORDER BY z.datum_objave DESC;

        """)
        return [dict(row) for row in self.cur.fetchall()]

    def dobi_zapiske_uporabnika_za_prikaz(self, id_uporabnika: int) -> List[dict]:
        self.cur.execute("""
            SELECT
                z.id_zapiska,
                z.naslov,
                z.datum_objave,
                z.stevilo_strani,
                z.vrsta_dokumenta,
                z.jezik,
                z.download_link,
                u.uporabnisko_ime AS ime_uporabnika,
                p.ime AS ime_predmeta,
                p.izobrazevalni_program,
                f.ime AS ime_fakultete,
                f.univerza,
                string_agg(DISTINCT pr.ime || ' ' || pr.priimek, ', ') AS profesorji
            FROM zapisek z
            JOIN uporabnik u ON z.id_uporabnika = u.id_uporabnika
            JOIN predmet p ON z.id_predmeta = p.id_predmeta
            JOIN predmet_faks pf ON p.id_predmeta = pf.id_predmeta
            JOIN faks f ON pf.id_faksa = f.id_faksa
            LEFT JOIN profesor_predmet pp ON p.id_predmeta = pp.id_predmeta
            LEFT JOIN profesor pr ON pp.id_profesorja = pr.id_profesorja
            WHERE z.id_uporabnika = %s
            GROUP BY z.id_zapiska, u.uporabnisko_ime, p.ime, p.izobrazevalni_program, f.ime, f.univerza
            ORDER BY z.datum_objave DESC
        """, (id_uporabnika,))
        return [dict(row) for row in self.cur.fetchall()]


    # Komentarji

    def dobi_komentarje(self, id_zapiska: int) -> List[Komentar]:
        self.cur.execute("""
            SELECT * FROM komentar WHERE id_zapiska = %s
        """, (id_zapiska,))
        return [Komentar.from_dict(row) for row in self.cur.fetchall()]

    def dodaj_komentar(self, k: Komentar):
        self.cur.execute("""
            INSERT INTO komentar (vsebina, id_zapiska, id_uporabnika, id_nadkomentarja)
            VALUES (%s, %s, %s, %s)
        """, (
            k.vsebina, k.id_zapiska, k.id_uporabnika, k.id_nadkomentarja
        ))
        self.conn.commit()

        
    def izbrisi_komentarje_zapiska(self, id_zapiska: int):
        # Najprej izbriši odgovore (tiste z nadkomentarjem)
        self.cur.execute("""
            DELETE FROM komentar
            WHERE id_zapiska = %s AND id_nadkomentarja IS NOT NULL
        """, (id_zapiska,))
        
        # Nato še osnovne komentarje
        self.cur.execute("""
            DELETE FROM komentar
            WHERE id_zapiska = %s AND id_nadkomentarja IS NULL
        """, (id_zapiska,))
        
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

    def izbrisi_prenose_zapiska(self, id_zapiska: int):
        self.cur.execute("DELETE FROM prenosi WHERE id_zapiska = %s", (id_zapiska,))
        self.conn.commit()

# Predmeti, profesorji, faksi
    

    def dobi_faks_po_imenu(self, ime: str) -> Optional[Faks]:
        self.cur.execute("SELECT * FROM faks WHERE ime = %s", (ime,))
        row = self.cur.fetchone()
        return Faks.from_dict(row) if row else None

    def dobi_profesor_po_imenu(self, ime: str, priimek: str) -> Optional[Profesor]:
        self.cur.execute("SELECT * FROM profesor WHERE ime = %s AND priimek = %s", (ime, priimek))
        row = self.cur.fetchone()
        return Profesor.from_dict(row) if row else None

    def dodaj_profesor(self, ime: str, priimek: str):
        self.cur.execute("INSERT INTO profesor (ime, priimek) VALUES (%s, %s)", (ime, priimek))
        self.conn.commit()

    def dodaj_profesor_predmet(self, id_profesorja: int, id_predmeta: int):
        self.cur.execute("""
            INSERT INTO profesor_predmet (id_profesorja, id_predmeta)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (id_profesorja, id_predmeta))
        self.conn.commit()
        
    def dodaj_predmet(self, predmet: Predmet) -> int:
        self.cur.execute("""
            INSERT INTO predmet (ime, izobrazevalni_program, letnik)
            VALUES (%s, %s, %s)
            RETURNING id_predmeta
        """, (predmet.ime, predmet.izobrazevalni_program, predmet.letnik))
        
        id_predmeta = self.cur.fetchone()[0]
        self.conn.commit()
        return id_predmeta


    def dobi_predmet_polno(self, ime: str, izobrazevalni_program: str, letnik: int) -> Optional[Predmet]:
        self.cur.execute("""
            SELECT *
            FROM predmet
            WHERE ime = %s AND izobrazevalni_program = %s AND letnik = %s
        """, (ime, izobrazevalni_program, letnik))
        row = self.cur.fetchone()
        return Predmet.from_dict(row) if row else None

    def dodaj_predmet_faks(self, id_predmeta: int, id_faksa: int):
        self.cur.execute("""
            INSERT INTO predmet_faks (id_predmeta, id_faksa)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (id_predmeta, id_faksa))
        self.conn.commit()
        
    def dodaj_profesor_faks(self, id_profesorja: int, id_faksa: int):
        self.cur.execute("""
            INSERT INTO profesor_faks (id_profesorja, id_faksa)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (id_profesorja, id_faksa))
        self.conn.commit()
        
    #prijava
    def preveri_prijavo(self, uporabnisko_ime, geslo):
        self.cur.execute("""
            SELECT * FROM uporabnik
            WHERE uporabnisko_ime = %s AND geslo = %s
        """, (uporabnisko_ime, geslo))
        row = self.cur.fetchone()
        return Uporabnik.from_dict(row) if row else None



    # zapri povezavo
    def zapri(self):
        self.cur.close()
        self.conn.close()