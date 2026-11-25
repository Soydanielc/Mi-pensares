import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()

app = FastAPI()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
mi_cliente: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class poesiaEntrantes(BaseModel):
    titulo: str
    contenido: str
    creado_en: str


class musicasEntrantes(BaseModel):
    titulo: str
    url: str
    creado_en: str


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)


@app.get("/poemas")
async def obtener_poemas_BD():
    try:
        response = mi_cliente.table("poemas").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/poemas")
async def RegPoemas(poema: poesiaEntrantes):
    try:
        datos = {
            "titulo": poema.titulo,
            "contenido": poema.contenido,
            "creado_en": poema.creado_en,
        }
        response = mi_cliente.table("poemas").insert(datos).execute()
        return {"Mensaje": "Tu poema fue subido con exito", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=(500), detail=(e))


@app.get("/musicas")
async def musicaDB():
    try:
        response = mi_cliente.table("musicas").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/musicas")
async def RegMusica(musica: musicasEntrantes):
    try:
        datos = {
            "titulo": musica.titulo,
            "url": musica.url,
            "creado_en": musica.creado_en,
        }
        response = mi_cliente.table("musicas").insert(datos).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=(500), detail=str(e))
