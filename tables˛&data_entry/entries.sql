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

INSERT INTO prenosi(id_uporabnika, id_zapiska)
VALUES (1, 2);


--vstavljanje vseh fakultet za univerzo v ljubljani
INSERT INTO faks(ime, univerza) VALUES
('Akademija za glasbo', 'Univerza v Ljubljani'),
('Akademija za gledališče, radio, film in televizijo', 'Univerza v Ljubljani'),
('Akademija za likovno umetnost in oblikovanje', 'Univerza v Ljubljani'),
('Biotehniška fakulteta', 'Univerza v Ljubljani'),
('Ekonomska fakulteta', 'Univerza v Ljubljani'),
('Fakulteta za arhitekturo', 'Univerza v Ljubljani'),
('Fakulteta za družbene vede', 'Univerza v Ljubljani'),
('Fakulteta za elektrotehniko', 'Univerza v Ljubljani'),
('Fakulteta za farmacijo', 'Univerza v Ljubljani'),
('Fakulteta za gradbeništvo in geodezijo', 'Univerza v Ljubljani'),
('Fakulteta za kemijo in kemijsko tehnologijo', 'Univerza v Ljubljani'),
('Fakulteta za pomorstvo in promet', 'Univerza v Ljubljani'),
('Fakulteta za računalništvo in informatiko', 'Univerza v Ljubljani'),
('Fakulteta za socialno delo', 'Univerza v Ljubljani'),
('Fakulteta za strojništvo', 'Univerza v Ljubljani'),
('Fakulteta za šport', 'Univerza v Ljubljani'),
('Fakulteta za upravo', 'Univerza v Ljubljani'),
('Filozofska fakulteta', 'Univerza v Ljubljani'),
('Medicinska fakulteta', 'Univerza v Ljubljani'),
('Naravoslovnotehniška fakulteta', 'Univerza v Ljubljani'),
('Pedagoška fakulteta', 'Univerza v Ljubljani'),
('Pravna fakulteta', 'Univerza v Ljubljani'),
('Teološka fakulteta', 'Univerza v Ljubljani'),
('Veterinarska fakulteta', 'Univerza v Ljubljani'),
('Zdravstvena fakulteta', 'Univerza v Ljubljani');

--dodajanje fakultet za univerzo v mariboru
INSERT INTO faks (ime, univerza) VALUES
('Ekonomsko-poslovna fakulteta', 'Univerza v Mariboru'),
('Fakulteta za elektrotehniko, računalništvo in informatiko', 'Univerza v Mariboru'),
('Fakulteta za energetiko', 'Univerza v Mariboru'),
('Fakulteta za gradbeništvo, prometno inženirstvo in arhitekturo', 'Univerza v Mariboru'),
('Fakulteta za kemijo in kemijsko tehnologijo', 'Univerza v Mariboru'),
('Fakulteta za kmetijstvo in biosistemske vede', 'Univerza v Mariboru'),
('Fakulteta za logistiko', 'Univerza v Mariboru'),
('Fakulteta za naravoslovje in matematiko', 'Univerza v Mariboru'),
('Fakulteta za organizacijske vede', 'Univerza v Mariboru'),
('Fakulteta za strojništvo', 'Univerza v Mariboru'),
('Fakulteta za turizem', 'Univerza v Mariboru'),
('Fakulteta za varnostne vede', 'Univerza v Mariboru'),
('Fakulteta za zdravstvene vede', 'Univerza v Mariboru'),
('Filozofska fakulteta', 'Univerza v Mariboru'),
('Medicinska fakulteta', 'Univerza v Mariboru'),
('Pedagoška fakulteta', 'Univerza v Mariboru'),
('Pravna fakulteta', 'Univerza v Mariboru');