-- Tabela faks
CREATE TABLE faks (
  id_faksa SERIAL PRIMARY KEY,
  ime TEXT NOT NULL,
  univerza TEXT NOT NULL
);

-- Tabela uporabnik
CREATE TABLE uporabnik (
  id_uporabnika SERIAL PRIMARY KEY,
  role TEXT NOT NULL,
  uporabnisko_ime TEXT NOT NULL,
  geslo TEXT NOT NULL,
  id_faksa INTEGER,
  FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa),
  CONSTRAINT check_role CHECK (role IN ('admin','user'))
);

-- Tabela predmet
CREATE TABLE predmet (
  id_predmeta SERIAL PRIMARY KEY,
  ime TEXT NOT NULL,
  izobrazevalni_program TEXT NOT NULL,
  letnik INTEGER NOT NULL
);

-- Tabela profesor
CREATE TABLE profesor (
  id_profesorja SERIAL PRIMARY KEY,
  ime TEXT NOT NULL,
  priimek TEXT NOT NULL
);

-- Tabela zapisek
CREATE TABLE zapisek (
  id_zapiska SERIAL PRIMARY KEY,
  stevilo_strani INTEGER,
  vrsta_dokumenta TEXT,
  naslov TEXT NOT NULL,
  datum_objave DATE DEFAULT CURRENT_DATE,
  jezik TEXT NOT NULL,
  download_link TEXT NOT NULL,
  id_predmeta INTEGER,
  id_uporabnika INTEGER,
  FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
  FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta)
);

-- Tabela komentar
CREATE TABLE komentar (
  id_komentarja SERIAL PRIMARY KEY,
  vsebina TEXT NOT NULL,
  datum_objave TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  id_zapiska INTEGER NOT NULL,
  id_uporabnika INTEGER NOT NULL,
  id_nadkomentarja INTEGER REFERENCES komentar(id_komentarja),
  FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
  FOREIGN KEY (id_zapiska) REFERENCES zapisek(id_zapiska)
);



-- Povezovalne tabele (relacijske)

-- Tabela prenosi
CREATE TABLE prenosi (
  id_uporabnika INT NOT NULL,
  id_zapiska INT NOT NULL,
  PRIMARY KEY (id_uporabnika, id_zapiska),
  FOREIGN KEY (id_uporabnika) REFERENCES uporabnik(id_uporabnika),
  FOREIGN KEY (id_zapiska) REFERENCES zapisek(id_zapiska)
);

-- Tabela predmet_faks
CREATE TABLE predmet_faks (
  id_predmeta INT NOT NULL,
  id_faksa INT NOT NULL,
  PRIMARY KEY (id_predmeta, id_faksa),
  FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta),
  FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa)
);

-- Tabela profesor_faks
CREATE TABLE profesor_faks (
  id_profesorja INT NOT NULL,
  id_faksa INT NOT NULL,
  PRIMARY KEY (id_profesorja, id_faksa),
  FOREIGN KEY (id_profesorja) REFERENCES profesor(id_profesorja),
  FOREIGN KEY (id_faksa) REFERENCES faks(id_faksa)
);

-- Tabela profesor_predmet
CREATE TABLE profesor_predmet (
  id_profesorja INT NOT NULL,
  id_predmeta INT NOT NULL,
  PRIMARY KEY (id_profesorja, id_predmeta),
  FOREIGN KEY (id_profesorja) REFERENCES profesor(id_profesorja),
  FOREIGN KEY (id_predmeta) REFERENCES predmet(id_predmeta)
);