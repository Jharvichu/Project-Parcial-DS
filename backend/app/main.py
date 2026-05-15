from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import reportes
from app.database import Base, engine

app = FastAPI(title="Mi Proyecto API")

# 1. Define qué orígenes (frontends) tienen permiso de conectarse
origins = [
    "http://localhost:5173",  # El puerto por defecto de Vite/React
    "http://127.0.0.1:5173",
]

# 2. Agrega el middleware a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite nuestro frontend
    allow_credentials=True,
    allow_methods=["*"],            # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],            # Permite todos los headers
)

# Rutas de incidentes
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])


@app.get("/")
def read_root():
    return {"message": "API de incidentes funcionando.."}