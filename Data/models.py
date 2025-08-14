from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from datetime import date
from typing import Optional

@dataclass_json
@dataclass
class Uporabnik:
    id_uporabnika: int = field(default=0)
    role: str = field(default="")
    uporabnisko_ime: str = field(default="")
    geslo: str = field(default="")
    id_faksa: int = field(default=0)

@dataclass_json
@dataclass
class UporabnikDto:
    id_uporabnika: int = field(default=0)
    uporabnisko_ime: str = field(default="")
    role: str = field(default="")


@dataclass_json
@dataclass
class Faks:
    id_faksa: int = field(default=0)
    ime: str = field(default="")
    univerza: str = field(default="")


@dataclass_json
@dataclass
class Zapisek:
    id_zapiska: int = field(default=0)
    stevilo_strani: int = field(default=0)
    vrsta_dokumenta: str = field(default="")
    naslov: str = field(default="")
    datum_objave: Optional[date] = field(default=None)
    jezik: str = field(default="")
    download_link: str = field(default="")
    id_predmeta: int = field(default=0)
    id_uporabnika: int = field(default=0)
    id_profesorja: int = field(default=0) 


@dataclass_json
@dataclass
class Predmet:
    id_predmeta: int = field(default=0)
    ime: str = field(default="")
    izobrazevalni_program: str = field(default="")
    letnik: int = field(default=0)


@dataclass_json
@dataclass
class Profesor:
    id_profesorja: int = field(default=0)
    ime: str = field(default="")
    priimek: str = field(default="")


@dataclass_json
@dataclass
class Komentar:
    id_komentarja: int = field(default=0)
    vsebina: str = field(default="")
    datum_objave: datetime = field(default_factory=datetime.now)
    id_zapiska: int = field(default=0)
    id_uporabnika: int = field(default=0)
    id_nadkomentarja: Optional[int] = field(default=None)


@dataclass_json
@dataclass
class Prenos:
    id_uporabnika: int = field(default=0)
    id_zapiska: int = field(default=0)


@dataclass_json
@dataclass
class PredmetFaks:
    id_predmeta: int = field(default=0)
    id_faksa: int = field(default=0)

@dataclass_json
@dataclass
class ProfesorFaks:
    id_profesorja: int = field(default=0)
    id_faksa: int = field(default=0)

