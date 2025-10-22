from psqlService import *
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psqlModel import Etudiant, EtudiantCreate, Presence, EtudPres
from typing import Dict, Any
from fastapi import Body

app = FastAPI()

# ======================== CORS =======================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)

# =================== Home endpoint ===================

@app.get("/")
def home_root():
    """
    Endpoint racine de l'API.
    return: Message de bienvenue.
    """
    return {"message": "Home page"}

# =================== Ping endpoint ===================

@app.get("/ping")
def ping():
    """
    Vérification de la disponibilité de l'API.
    return: Message 'pong'.
    """
    return {"message": "pong"}

# =================== Etudiant endpoints ===================

@app.post("/db/etudiants", response_model=Etudiant)
async def insert_etudiant(etudiant: EtudiantCreate):
    """
    Insertion d'un nouvel étudiant dans la base de données.
    param etudiant: Données de l'étudiant à insérer (EtudiantCreate).
    return: L'étudiant inséré (Etudiant).
    """
    try:
        return await service_insert_etudiant(etudiant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/etudiants", response_model=list[Etudiant])
async def get_all_etudiants():
    """
    Récupère tous les étudiants présents dans la base de données.
    return: Liste d'objets Etudiant.
    """
    try:
        return await service_get_all_etudiants()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/db/etudiants/{id_etu}", response_model=Etudiant)
async def update_etudiant(id_etu: int, etudiant: EtudiantCreate):
    """
    Met à jour les informations d'un étudiant existant.
    param id_etu: ID de l'étudiant à modifier.
    param etudiant: Nouvelles données de l'étudiant (EtudiantCreate).
    return: L'étudiant mis à jour (Etudiant).
    """
    try:
        return await service_update_etudiant(id_etu, etudiant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/db/etudiants/{id_etu}", response_model=dict)
async def delete_etudiant(id_etu: int):
    """
    Supprime un étudiant selon son ID.
    param id_etu: ID de l'étudiant à supprimer.
    return: Message de confirmation.
    """
    try:
        return await service_delete_etudiant(id_etu)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/search-etudiants", response_model=list[EtudPres])
async def search_etudiants(params: Dict[str, Any] | None = Body(...)):
    """
    Recherche des étudiants selon des paramètres (dates, nom, groupe, etc).
    param params: Dictionnaire des filtres de recherche.
    return: Liste d'objets EtudPres correspondant aux critères.
    """
    try:
        return await service_search_etudiants(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/count-etudiants", response_model=dict)
async def get_count_etudiants():
    """
    Retourne le nombre total d'étudiants dans la base.
    return: Dictionnaire avec le nombre d'étudiants.
    """
    try:
        return {"count-etudiants": await service_get_count_etudiants()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/count-etudiants-actifs", response_model=dict)
async def get_count_etudiants_actifs():
    """
    Retourne le nombre d'étudiants actifs aujourd'hui (ayant badgé).
    return: Dictionnaire avec le nombre d'étudiants actifs.
    """
    try:
        return {"count-etudiants-actifs": await service_get_count_etudiants_actifs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/db/etudiants-presences", response_model=list[EtudPres])
async def get_etudiants_presences():
    """
    Récupère les présences associées à chaque étudiant.
    return: Liste d'objets EtudPres (étudiant + présence).
    """
    try:
        return await service_get_etudiants_presences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =================== Presence endpoints ===================

@app.get("/db/presences", response_model=list[Presence])
async def get_all_presences():
    """
    Récupère toutes les présences enregistrées.
    return: Liste d'objets Presence.
    """
    try:
        return await service_get_all_presences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/insert-presence", response_model=Presence)
async def insert_presence(presence: Presence):
    """
    Insère une nouvelle présence dans la base de données.
    param presence: Données de la présence à insérer (Presence).
    return: L'objet Presence inséré.
    """
    try:
        return await service_insert_presence(presence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/db/count-day", response_model=dict)
async def get_count_day():
    """
    Retourne le nombre de badges (présences) du jour.
    return: Dictionnaire avec le nombre de badges aujourd'hui.
    """
    try:
        return {"count-day": await service_get_count_day()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/db/count-week", response_model=dict)
async def get_count_week():
    """
    Retourne le nombre de badges (présences) de la semaine courante.
    return: Dictionnaire avec le nombre de badges cette semaine.
    """
    try:
        return {"count-week": await service_get_count_week()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
