#Función para crear un motor de base de datos, que gestiona la conexión a la BD.
from sqlalchemy import create_engine

#Función para crear una clase base que será utilizada para definir los modelos de la BD.
from sqlalchemy.ext.declarative import declarative_base

#Clase que genera un creador de sesiones. Las sesiones se utilizan para interactuar con la BD.
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/crudfastapi"

#Motor de BD:
engine = create_engine(DATABASE_URL)

#Crear sesión: objeto que administra las transacciones y las interacciones con la BD.
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

#Base: es usada como clase base para todos los modelos (tablas)
Base = declarative_base()

