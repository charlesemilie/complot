from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from .database import Base

class PlayerDB(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    coins = Column(Integer, default=0)
    alive = Column(Boolean, default=True)
    # relation cartes, etc.

# Pydantic schemas
class Player(BaseModel):
    id: int
    name: str
    coins: int
    alive: bool

    class Config:
        orm_mode = True

class PlayerCreate(BaseModel):
    name: str