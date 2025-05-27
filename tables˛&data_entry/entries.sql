INSERT INTO faks(ime, univerza)
VALUES ('Fakulteta za matematiko in fiziko', 'Univerza v Ljubljani');

INSERT INTO uporabnik(role, uporabnisko_ime, geslo, id_faksa)
VALUES ('user', 'j_novak', 'j_novak', 1);

INSERT INTO predmet(ime, izobrazevalni_program, letnik)
VALUES ('Numerične metode 1', 'Finančna matematika- dodiplomski', 2);

INSERT INTO predmet(ime, izobrazevalni_program, letnik)
VALUES ('Numerične metode 2', 'Finančna matematika- dodiplomski', 2);

INSERT INTO profesor(ime, priimek)
VALUES ('Ada', 'Šadl Praprotnik');

INSERT INTO zapisek (stevilo_strani, vrsta_dokumenta, naslov, jezik, download_link, id_predmeta, id_uporabnika)
VALUES (54, 'pdf', 'numerične metode 2- vaje 2024/25', 'slovenščina', '//', 1, 1);

INSERT INTO zapisek (stevilo_strani, vrsta_dokumenta, naslov, jezik, download_link, id_predmeta, id_uporabnika)
VALUES (56, 'pdf', 'numerične metode 1- predavanja 2024/25', 'slovenščina', '//', 1, 1);

INSERT INTO komentar(vsebina, id_zapiska, id_uporabnika)
VALUES ('kvalitetni zapiski, malo napak', 2, 1);

INSERT INTO predmet_faks(id_predmeta, id_faksa)
VALUES (1, 1);

INSERT INTO profesor_faks(id_profesorja, id_faksa)
VALUES (1, 1);

INSERT INTO profesor_predmet(id_profesorja, id_predmeta)
VALUES (1, 1);