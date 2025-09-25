from psqlService import *
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

# =================== Ping endpoint ===================

@app.get("/ping")
def ping():
    return {"message": "pong"}

# =================== Etudiant endpoints ===================

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

@app.get("/db/count-etudiants-actifs", response_model=dict)
async def get_count_etudiants_actifs():
    try:
        return {"count-etudiants-actifs": await service_get_count_etudiants_actifs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/db/etudiants/{id_etu}", response_model=dict)
async def delete_etudiant(id_etu: int):
    try:
        return await service_delete_etudiant(id_etu)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =================== Presence endpoints ===================

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
    
@app.get("/db/count-day", response_model=dict)
async def get_count_day():
    try:
        return {"count-day": await service_get_count_day()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/db/count-week", response_model=dict)
async def get_count_week():
    try:
        return {"count-week": await service_get_count_week()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
