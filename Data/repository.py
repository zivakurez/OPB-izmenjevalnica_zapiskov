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
        self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)



    # Uporabniki

    def dobi_uporabnika(self, id_uporabnika: int) -> Optional[UporabnikDto]:
        self.cur.execute("""
            SELECT id_uporabnika, uporabnisko_ime, role
            FROM uporabnik
            WHERE id_uporabnika = %s
        """, (id_uporabnika,))
        row = self.cur.fetchone()
        return UporabnikDto.from_dict(row) if row else None
    
    def dobi_uporabnika_po_imenu(self, uporabnisko_ime: str) -> Optional[Uporabnik]:
        self.cur.execute("""
            SELECT id_uporabnika, role, uporabnisko_ime, geslo, id_faksa
            FROM uporabnik
            WHERE uporabnisko_ime = %s
        """, (uporabnisko_ime,))
        row = self.cur.fetchone()
        if row:
            return Uporabnik(**row)  
        return None


    def dodaj_uporabnika(self, uporabnik: Uporabnik):
        self.cur.execute("""
            INSERT INTO uporabnik (role, uporabnisko_ime, geslo, id_faksa)
            VALUES (%s, %s, %s, %s)
            RETURNING id_uporabnika
        """, (
            uporabnik.role,
            uporabnik.uporabnisko_ime,
            uporabnik.geslo,
            uporabnik.id_faksa
        ))
        uporabnik.id_uporabnika = self.cur.fetchone()["id_uporabnika"]
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


    def filtriraj_zapiske(self, predmet, fakulteta, program, profesor):
        query = """
            SELECT 
                z.naslov, 
                z.id_zapiska, 
                COALESCE(p.ime, 'Ni določeno') AS predmet, 
                COALESCE(f.ime, 'Ni določeno') AS fakulteta,
                COALESCE(p.izobrazevalni_program, 'Ni določeno') AS izobrazevalni_program,
                COALESCE(pr.ime || ' ' || pr.priimek, 'Ni določeno') AS profesor
            FROM zapisek z
            JOIN predmet p ON z.id_predmeta = p.id_predmeta
            LEFT JOIN predmet_faks pf ON p.id_predmeta = pf.id_predmeta
            LEFT JOIN faks f ON pf.id_faksa = f.id_faksa
            LEFT JOIN profesor_predmet pp ON p.id_predmeta = pp.id_predmeta
            LEFT JOIN profesor pr ON pp.id_profesorja = pr.id_profesorja
            WHERE 1=1
        """

        params = []

        if predmet:
            query += " AND LOWER(p.ime) LIKE LOWER(%s)"
            params.append(f"%{predmet}%")

        if fakulteta:
            query += " AND LOWER(f.ime) LIKE LOWER(%s)"
            params.append(f"%{fakulteta}%")

        if program:
            query += " AND LOWER(p.izobrazevalni_program) LIKE LOWER(%s)"
            params.append(f"%{program}%")

        if profesor:
            query += """
                AND (
                    LOWER(pr.ime) LIKE LOWER(%s) OR 
                    LOWER(pr.priimek) LIKE LOWER(%s)
                )
            """
            params.append(f"%{profesor}%")
            params.append(f"%{profesor}%")

        query += " ORDER BY z.datum_objave DESC"

        self.cur.execute(query, tuple(params))
        return [dict(row) for row in self.cur.fetchall()]

    def dobi_zapisek_s_podatki(self, id_zapiska: int) -> Optional[dict]:
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

            WHERE z.id_zapiska = %s
            GROUP BY z.id_zapiska, u.uporabnisko_ime, p.ime, p.izobrazevalni_program, f.ime, f.univerza
        """, (id_zapiska,))
        
        row = self.cur.fetchone()
        if row:
            return dict(row)
        return None

    # Komentarji

    def dobi_komentarje(self, id_zapiska: int) -> List[dict]:
        self.cur.execute("""
            SELECT 
                k.id_komentarja,
                k.vsebina AS besedilo,
                k.id_uporabnika,
                u.uporabnisko_ime AS avtor
            FROM komentar k
            JOIN uporabnik u ON k.id_uporabnika = u.id_uporabnika
            WHERE k.id_zapiska = %s
            ORDER BY k.id_komentarja ASC
        """, (id_zapiska,))
        return [dict(row) for row in self.cur.fetchall()]


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

    def dobi_komentar(self, id_komentarja: int) -> Optional[Komentar]:
        self.cur.execute("""
            SELECT * FROM komentar WHERE id_komentarja = %s
        """, (id_komentarja,))
        row = self.cur.fetchone()
        return Komentar.from_dict(row) if row else None
    
    def izbrisi_komentar(self, id_komentarja: int):
        self.cur.execute("""
            DELETE FROM komentar WHERE id_komentarja = %s
        """, (id_komentarja,))
        self.conn.commit()

    # Prenosi

    def dodaj_prenos(self, p: Prenos):
        self.cur.execute("""
            INSERT INTO prenosi (id_uporabnika, id_zapiska)
            VALUES (%s, %s)
        """, (p.id_uporabnika, p.id_zapiska))
        self.conn.commit()

    def dobi_prenose_uporabnika(self, id_uporabnika: int) -> List[dict]:
        self.cur.execute("""
            SELECT
                z.id_zapiska,
                z.naslov,
                z.datum_objave,
                z.vrsta_dokumenta,
                p.ime AS ime_predmeta,
                f.ime AS ime_fakultete,
                u.uporabnisko_ime AS avtor
            FROM prenosi pr
            JOIN zapisek z ON pr.id_zapiska = z.id_zapiska
            JOIN uporabnik u ON z.id_uporabnika = u.id_uporabnika
            JOIN predmet p ON z.id_predmeta = p.id_predmeta
            JOIN predmet_faks pf ON p.id_predmeta = pf.id_predmeta
            JOIN faks f ON pf.id_faksa = f.id_faksa
            WHERE pr.id_uporabnika = %s
        """, (id_uporabnika,))
        return [dict(row) for row in self.cur.fetchall()]


    def izbrisi_prenose_zapiska(self, id_zapiska: int):
        self.cur.execute("DELETE FROM prenosi WHERE id_zapiska = %s", (id_zapiska,))
        self.conn.commit()

# Predmeti, profesorji, faksi
    

    def dobi_faks_po_imenu(self, ime: str) -> Optional[Faks]:
        self.cur.execute("SELECT * FROM faks WHERE ime = %s", (ime,))
        row = self.cur.fetchone()
        return Faks.from_dict(row) if row else None
    
    def dobi_id_faksa_po_imenu(self, ime_faksa: str) -> Optional[int]:
        self.cur.execute("SELECT id_faksa FROM faks WHERE ime = %s", (ime_faksa,))
        row = self.cur.fetchone()
        return row["id_faksa"] if row else None
    
    def dobi_fakultete(self) -> list[str]:
        self.cur.execute("""
            SELECT ime FROM faks
        """)
        return [row["ime"] for row in self.cur.fetchall()]


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

    #poizvedbe

    # Predmeti
    def vrni_vse_predmete(self) -> List[str]:
        self.cur.execute("SELECT DISTINCT ime FROM predmet ORDER BY ime")
        return [row["ime"] for row in self.cur.fetchall()]

    # Fakultete
    def vrni_vse_fakultete(self) -> List[str]:
        self.cur.execute("SELECT DISTINCT ime FROM faks ORDER BY ime")
        return [row["ime"] for row in self.cur.fetchall()]

    # Programi (iz atributa pri predmetu)
    def vrni_vse_programe(self) -> List[str]:
        self.cur.execute("SELECT DISTINCT izobrazevalni_program FROM predmet ORDER BY izobrazevalni_program")
        return [row["izobrazevalni_program"] for row in self.cur.fetchall()]

    # Imena profesorjev
    def vrni_vsa_imena_profesorjev(self) -> List[str]:
        self.cur.execute("SELECT DISTINCT ime FROM profesor ORDER BY ime")
        return [row["ime"] for row in self.cur.fetchall()]

    # Priimki profesorjev
    def vrni_vse_priimke_profesorjev(self) -> List[str]:
        self.cur.execute("SELECT DISTINCT priimek FROM profesor ORDER BY priimek")
        return [row["priimek"] for row in self.cur.fetchall()]


    #preveri če je admin
    def je_admin(self, id_uporabnika: int) -> bool:
        self.cur.execute("""
            SELECT role FROM uporabnik WHERE id_uporabnika = %s
        """, (id_uporabnika,))
        row = self.cur.fetchone()
        return row and row['role'] == 'admin'


    # zapri povezavo
    def zapri(self):
        self.cur.close()
        self.conn.close()