CREATE TABLE zapisek (
  id_zapiska INTEGER PRIMARY KEY,
  stevilo_strani INTEGER,
  vrsta_dokumenta TEXT,
  naslov TEXT NOT NULL,
  datum_objave DATE DEFAULT CURRENT_DATE,
  jezik	TEXT NOT NULL,
  download_link	TEXT NOT NULL,
  id_predmeta INTEGER,
  id_uporabnika INTEGER,
  FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
  FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta)
);


INSERT INTO zapisek (id_zapiska, stevilo_strani, vrsta_dokumenta, naslov, jezik, download_link, id_predmeta, id_uporabnika)
values (3, 54, 'pdf','numerične metode 2- vaje 2024/25', 'slovenščina', '//', 1, 1);

CREATE TABLE predmet (
  id_predmeta INTEGER PRIMARY KEY,
  ime TEXT NOT NULL,
  izobrazevalni_program TEXT,
  letnik INTEGER
);

INSERT INTO predmet(id_predmeta, ime, izobrazevalni_program, letnik)
values (1, 'Numerične metode 1', 'Finančna matematika- dodiplomski', 2)


CREATE TABLE profesor (
  id_profesorja INTEGER PRIMARY KEY,
  ime TEXT NOT NULL,
  priimek TEXT NOT NULL
);

INSERT INTO profesor(id_profesorja, ime, priimek)
values(1, 'Ada',  'Šadl Praprotnik');

SELECT * FROM profesor


CREATE TABLE faks (
  id_faksa INTEGER PRIMARY KEY,
  ime TEXT NOT NULL,
  univerza TEXT 
);

INSERT INTO faks(id_faksa, ime, univerza)
values(1, 'Fakulteta za matematiko in fiziko', 'Univerza v Ljubljani');

SELECT * FROM faks

CREATE TABLE komentar (
  id_komentarja INTEGER PRIMARY KEY,
  vsebina TEXT NOT NULL,
  datum_objave TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  id_zapiska INTEGER,
  id_uporabnika INTEGER,
  FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
  FOREIGN KEY (id_zapiska) REFERENCES zapisek(id_zapiska)
);

INSERT INTO komentar(id_komentarja, vsebina, id_zapiska, id_uporabnika)
values(1, 'kvalitetni zapiski, malo napak', 2, 1)

SELECT * FROM komentar

CREATE TABLE uporabnik (
  id_uporabnika INTEGER PRIMARY KEY,
  role TEXT NOT NULL,
  uporabnisko_ime TEXT NOT NULL,
  geslo TEXT NOT NULL,
  id_faksa INTEGER,
  FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa),
  CONSTRAINT check_role CHECK (role IN ('admin','user'))
);

INSERT INTO uporabnik(id_uporabnika, role, uporabnisko_ime, geslo, id_faksa)
VALUES (1, 'user', 'j_novak', 'j_novak', 1);


CREATE TABLE prenosi (
    id_uporabnika INT,
    id_zapiska INT,
    PRIMARY KEY (id_uporabnika, id_zapiska),
    FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
    FOREIGN KEY (id_zapiska) REFERENCES zapisek(id_zapiska)
);

CREATE TABLE predmet_faks (
    id_predmeta INT,
    id_faksa INT,
    PRIMARY KEY (id_predmeta, id_faksa),
    FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta),
    FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa)
);

INSERT INTO predmet_faks(id_predmeta, id_faksa)
VALUES(1, 1)

CREATE TABLE profesor_faks (
    id_profesorja INT,
    id_faksa INT,
    PRIMARY KEY (id_profesorja, id_faksa),
    FOREIGN KEY (id_profesorja) REFERENCES profesor(id_profesorja),
    FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa)
);

INSERT INTO profesor_faks(id_profesorja, id_faksa)
VALUES(1, 1)


CREATE TABLE profesor_predmet (
    id_profesorja INT,
    id_predmeta INT,
    PRIMARY KEY (id_profesorja, id_predmeta),
    FOREIGN KEY (id_profesorja) REFERENCES profesor(id_profesorja),
    FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta)
);

INSERT INTO profesor_predmet(id_profesorja, id_predmeta)
VALUES(1, 1)
