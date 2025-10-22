from pydantic import BaseModel 
from typing import List
from datetime import datetime

class EtudiantCreate(BaseModel):
    nom_etu: str
    prenom_etu: str
    anne_etu: str
    td_etu: (str|None) = None
    tp_etu: (str|None) = None
    id_carte_etu: int

class Etudiant(BaseModel):
    id_etu: int
    nom_etu: str
    prenom_etu: str
    anne_etu: str
    td_etu: (str|None) = None
    tp_etu: (str|None) = None
    id_carte_etu: int

class Presence(BaseModel):
    id_pres: int
    id_carte_etu: int
    datetime_pres: datetime
    type_pres: (str|None) = None

class EtudPres(BaseModel):
    id_etu: int
    nom_etu: str
    prenom_etu: str
    anne_etu: str
    td_etu: (str|None) = None
    tp_etu: (str|None) = None
    datetime_pres: (datetime|None) = None
    statut_presence: str