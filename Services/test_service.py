from datetime import date
from Data.models import Zapisek
from Services.zapiski_service import ZapisekService
from Services.komentar_service import KomentarService

zapisek_service = ZapisekService()
komentar_service = KomentarService()

# ID obstoječega uporabnika
id_uporabnika = 1

# -----------------------------
# 1. Dodaj zapisek
# -----------------------------
# zapisek = Zapisek(
#     stevilo_strani=10,
#     vrsta_dokumenta="PDF",
#     naslov="Zapiski predavanj Algebra 1 2022/23",
#     jezik="slovenščina",
#     download_link="http://primer.si/zapisek.pdf"
#     # datum_objave se ne podaja
# )

# uspesno = zapisek_service.dodaj_zapisek(
#     zapisek=zapisek,
#     id_uporabnika=id_uporabnika,
#     ime_predmeta="Algebra 1",
#     ime_faksa="Fakulteta za matematiko in fiziko",
#     ime_profesorja="Klemen",
#     priimek_profesorja="Šivic",
#     letnik=1,
#     izobrazevalni_program="Finančna matematika"
# )

# print("✅ Dodajanje zapiska:", "Uspelo" if uspesno else "Ni uspelo")

# -----------------------------
# 2. Najdi ta zapisek
# -----------------------------
zapiski = zapisek_service.pridobi_vse_zapiske()
zadnji = zapiski[-1]
# print("📝 Dodan zapisek:", zadnji.naslov, "| Datum objave:", zadnji.datum_objave)

# -----------------------------
# 3. Dodaj komentar na zapisek
# -----------------------------

uspesno_komentar = komentar_service.dodaj_komentar(
    vsebina="Zelo uporaben zapisek, hvala!",
    id_zapiska=zadnji.id_zapiska,
    id_uporabnika=id_uporabnika
)

print("✅ Dodajanje komentarja:", "Uspelo" if uspesno_komentar else "Ni uspelo")

# -----------------------------
# 4. Prikaži komentarje za zapisek
# -----------------------------
komentarji = komentar_service.komentarji_za_zapisek(zadnji.id_zapiska)
print(f"💬 Komentarji ({len(komentarji)}):")
for k in komentarji:
    print("-", k.vsebina)

# -----------------------------
# 5. Izbriši zapisek kot avtor
# -----------------------------
brisanje = zapisek_service.izbrisi_zapisek(zadnji.id_zapiska, id_uporabnika)
print("🗑️ Brisanje zapiska:", "Uspelo" if brisanje else "Ni uspelo")
