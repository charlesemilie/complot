from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router
from .database import Base, engine

# Crée les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complot en ligne")

origins = [
    "http://localhost:3000",
    "https://complot-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "alive"}

# Autoriser la méthode HEAD sur la racine pour éviter 405
@app.head("/")
def root_head():
    return {"status": "alive"}