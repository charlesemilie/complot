from fastapi import FastAPI
from .api import router
from .database import Base, engine

# Crée les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complot en ligne")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "alive"}