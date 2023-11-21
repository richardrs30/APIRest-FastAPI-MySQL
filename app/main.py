from typing import List
from fastapi import FastAPI
from fastapi.params import Depends#
from starlette.responses import RedirectResponse
from . import models, schemas
from .Conexion import SessionLocal, engine #
from sqlalchemy.orm import Session# 
import bcrypt

 

#Crea todas las tablas en la BD definidas en el modelo
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get('/usuarios/', response_model=List[schemas.User])
def show_users(db:Session=Depends(get_db)):#abre sesion
    usuarios = db.query(models.User).all()#trae todos los usuarios de la BD 
    return usuarios


@app.post('/usuarios/', response_model=schemas.User)#solo el último usuario
def create_users(entrada:schemas.User, db:Session=Depends(get_db)):

    # Cifra la contraseña antes de almacenarla
    hashed_password = bcrypt.hashpw(entrada.password.encode('utf-8'), bcrypt.gensalt())

    usuario = models.User(name = entrada.name, email=entrada.email, password=hashed_password.decode('utf-8'), rol=entrada.rol, estado=entrada.estado)

    db.add(usuario) #Agregar el usuario a la sesión (no a la BD aún)
    db.commit() #Confirmar la transacción, guarda los cambios en la BD
    db.refresh(usuario) #Actualizar el objeto de usuario con los cambios hechos en la BD
    return usuario

#UPDATE
@app.put('/usuarios/{usuario_id}', response_model=schemas.User)
def update_users(usuario_id:int, entrada:schemas.UserUpdate,db:Session=Depends(get_db)):

    usuario = db.query(models.User).filter_by(id=usuario_id).first()

    # Actualiza los campos de usuario excepto la contraseña
    usuario.name=entrada.name
    usuario.email=entrada.email
    usuario.rol=entrada.rol

    # Verifica si la contraseña se actualiza
    if entrada.password:
        # Cifra la nueva contraseña antes de almacenarla
        hashed_password = bcrypt.hashpw(entrada.password.encode('utf-8'), bcrypt.gensalt())
        usuario.password = hashed_password.decode('utf-8')
        
    db.commit()
    db.refresh(usuario)
    return usuario


@app.delete('/usuarios/{usuario_id}',response_model=schemas.Respuesta)
def delete_users(usuario_id:int, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=usuario_id).first()

    db.delete(usuario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta