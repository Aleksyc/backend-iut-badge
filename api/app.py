from psqlService import service_get_all_etudiants, service_get_count_etudiants, service_get_all_presences, service_insert_etudiant, service_insert_presence
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psqlModel import Etudiant, Presence


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home_root():
    return {"message": "Home page"}

# Ping endpoint

@app.get("/ping")
def ping():
    return {"message": "pong"}

# Etudiant endpoints

@app.get("/db/etudiants", response_model=list[Etudiant])
async def get_all_etudiants():
    try:
        return await service_get_all_etudiants()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/count-etudiants", response_model=dict)
async def get_count_etudiants():
    try:
        return {"count-etudiants": await service_get_count_etudiants()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/db/insert-etudiant", response_model=Etudiant)
async def insert_etudiant(etudiant: Etudiant):
    try:
        return await service_insert_etudiant(etudiant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Presence endpoints

@app.get("/db/presences", response_model=list[Presence])
async def get_all_presences():
    try:
        return await service_get_all_presences()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/insert-presence", response_model=Presence)
async def insert_presence(presence: Presence):
    try:
        return await service_insert_presence(presence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
