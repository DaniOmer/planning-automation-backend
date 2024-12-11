from typing import Optional

from pydantic import BaseModel


# Schéma pour la création d'une salle
class ClassroomCreate(BaseModel):
    name: str
    capacity: int

class ClassroomResponse(BaseModel):
    id: int
    name: str
    capacity: int

    class Config:
        orm_mode = True 
