from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import reportes
from app.database import Base, engine

app = FastAPI(title="Mi Proyecto API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])

@app.get("/")
def read_root():
    return {"message": "API de incidentes funcionando.."}