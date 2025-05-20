--začetni insert za vsako tabelo

INSERT INTO zapisek (id_zapiska, stevilo_strani, vrsta_dokumenta, naslov, jezik, download_link, id_predmeta, id_uporabnika)
values (3, 54, 'pdf','numerične metode 2- vaje 2024/25', 'slovenščina', '//', 1, 1);

INSERT INTO predmet(id_predmeta, ime, izobrazevalni_program, letnik)
values (1, 'Numerične metode 1', 'Finančna matematika- dodiplomski', 2)


INSERT INTO profesor(id_profesorja, ime, priimek)
values(1, 'Ada',  'Šadl Praprotnik');

INSERT INTO faks(id_faksa, ime, univerza)
values(1, 'Fakulteta za matematiko in fiziko', 'Univerza v Ljubljani');

INSERT INTO komentar(id_komentarja, vsebina, id_zapiska, id_uporabnika)
values(1, 'kvalitetni zapiski, malo napak', 2, 1)

INSERT INTO uporabnik(id_uporabnika, role, uporabnisko_ime, geslo, id_faksa)
VALUES (1, 'user', 'j_novak', 'j_novak', 1);

INSERT INTO predmet_faks(id_predmeta, id_faksa)
VALUES(1, 1)

INSERT INTO profesor_faks(id_profesorja, id_faksa)
VALUES(1, 1)

INSERT INTO profesor_predmet(id_profesorja, id_predmeta)
VALUES(1, 1)