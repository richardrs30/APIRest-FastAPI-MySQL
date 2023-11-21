from sqlalchemy import Column, Integer, String
from .Conexion import Base

#Clase Base: permite la creación de tablas en la BD
class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    email = Column(String(200))
    password = Column(String(200))
    rol = Column(String(20))
    estado = Column(Integer)

