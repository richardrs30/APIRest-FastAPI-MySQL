#from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int = None
    name:str
    email:str
    password:str
    rol:str
    estado:int

    class Config:
        orm_mode =True

#Solo actualizaremos el nombre 
class UserUpdate(BaseModel):   
    name:str
    email:str
    password:str
    rol:str
   
    class Config:
        orm_mode =True

class Respuesta(BaseModel):   
    mensaje:str
   
 