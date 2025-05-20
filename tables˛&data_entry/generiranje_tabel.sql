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


CREATE TABLE predmet (
  id_predmeta INTEGER PRIMARY KEY,
  ime TEXT NOT NULL,
  izobrazevalni_program TEXT,
  letnik INTEGER
);


CREATE TABLE profesor (
  id_profesorja INTEGER PRIMARY KEY,
  ime TEXT NOT NULL,
  priimek TEXT NOT NULL
);



CREATE TABLE faks (
  id_faksa INTEGER PRIMARY KEY,
  ime TEXT NOT NULL,
  univerza TEXT 
);


CREATE TABLE komentar (
  id_komentarja INTEGER PRIMARY KEY,
  vsebina TEXT NOT NULL,
  datum_objave TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  id_zapiska INTEGER,
  id_uporabnika INTEGER,
  FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
  FOREIGN KEY (id_zapiska) REFERENCES zapisek(id_zapiska)
);

ALTER TABLE komentar
ADD COLUMN id_nadkomentarja INTEGER REFERENCES komentar(id_komentarja);


CREATE TABLE uporabnik (
  id_uporabnika INTEGER PRIMARY KEY,
  role TEXT NOT NULL,
  uporabnisko_ime TEXT NOT NULL,
  geslo TEXT NOT NULL,
  id_faksa INTEGER,
  FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa),
  CONSTRAINT check_role CHECK (role IN ('admin','user'))
);


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

CREATE TABLE profesor_faks (
    id_profesorja INT,
    id_faksa INT,
    PRIMARY KEY (id_profesorja, id_faksa),
    FOREIGN KEY (id_profesorja) REFERENCES profesor(id_profesorja),
    FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa)
);



CREATE TABLE profesor_predmet (
    id_profesorja INT,
    id_predmeta INT,
    PRIMARY KEY (id_profesorja, id_predmeta),
    FOREIGN KEY (id_profesorja) REFERENCES profesor(id_profesorja),
    FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta)
);


