from Services.zapiski_service import ZapisekService


service = ZapisekService()

vsi = service.pridobi_vse_zapiske()



from Data.models import Zapisek
from Services.zapiski_service import ZapisekService

service = ZapisekService()

nov_zapisek = Zapisek(
    id_zapiska = 4,
    stevilo_strani = 30,
    naslov="Zapiski iz NUM",
    id_predmeta = 1,
    id_uporabnika = 1
)

id_uporabnika = 1

#vsi1 = service.dodaj_zapisek(nov_zapisek, id_uporabnika)

for zapisek in vsi:
   print(zapisek)