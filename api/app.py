from psqlService import service_get_all_etudiants, service_get_all_presences, service_insert_etudiant, service_insert_presence
from fastapi import FastAPI, HTTPException
from psqlModel import Etudiant, Presence

app = FastAPI()

@app.get("/")
def home_root():
    return {"message": "Home page"}

@app.get("/db/etudiants", response_model=list[Etudiant])
async def get_all_etudiants():
    try:
        return await service_get_all_etudiants()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/presences", response_model=list[Presence])
async def get_all_presences():
    try:
        return await service_get_all_presences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/insert-etudiant", response_model=Etudiant)
async def insert_etudiant(etudiant: Etudiant):
    try:
        return await service_insert_etudiant(etudiant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/insert-presence", response_model=Presence)
async def insert_presence(presence: Presence):
    try:
        return await service_insert_presence(presence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
