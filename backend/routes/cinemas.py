from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter()

# Endpoints para Empresas de Cinema
@router.post("/empresas/", response_model=schemas.EmpresaCinema)
def create_empresa(
    empresa: schemas.EmpresaCinemaCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")

    db_empresa = db.query(models.EmpresaCinema).filter(models.EmpresaCinema.cnpj == empresa.cnpj).first()
    
    if db_empresa:
        raise HTTPException(status_code=400, detail="Empresa já cadastrada")
    
    nova_empresa = models.EmpresaCinema(**empresa.dict())
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa

@router.get("/empresas/", response_model=list[schemas.EmpresaCinema])
def read_empresas(
    #skip: int = 0, 
    #limit: int = 10, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo_usuario != "Admin" and current_user.tipo_usuario != "Encarregado":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")

    return db.query(models.EmpresaCinema).all()

# Endpoints para Cinemas
@router.post("/cinemas/", response_model=schemas.Cinema)
def create_cinema(
    cinema: schemas.CinemaCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")
    
    db_cinema = db.query(models.Cinema).filter(models.Cinema.nome == cinema.nome).first()
    
    if db_cinema:
        raise HTTPException(status_code=400, detail="Empresa já cadastrada")
    
    novo_cinema = models.Cinema(**cinema.dict())
    db.add(novo_cinema)
    db.commit()
    db.refresh(novo_cinema)
    return novo_cinema

@router.get("/cinemas/", response_model=list[schemas.Cinema])
def read_cinemas(
    #skip: int = 0, 
    #limit: int = 50, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo_usuario != "Admin" and current_user.tipo_usuario != "Encarregado":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")

    return db.query(models.Cinema).all()

# Endpoints para Salas
@router.post("/salas/", response_model=schemas.Sala)
def create_sala(
    sala: schemas.SalaCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")

    nova_sala = models.Sala(**sala.dict())
    db.add(nova_sala)
    db.commit()
    db.refresh(nova_sala)
    return nova_sala

@router.get("/salas/", response_model=list[schemas.Sala])
def read_salas(
    #skip: int = 0, 
    #limit: int = 20, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo_usuario != "Admin" and current_user.tipo_usuario != "Encarregado":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")
    
    # return db.query(models.Sala).offset(skip).limit(limit).all()
    return db.query(models.Sala).all()