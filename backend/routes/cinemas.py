from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

# Endpoints para Empresas de Cinema
@router.post("/empresas/", response_model=schemas.EmpresaCinema)
def create_empresa(empresa: schemas.EmpresaCinemaCreate, db: Session = Depends(database.get_db)):
    db_empresa = db.query(models.EmpresaCinema).filter(models.EmpresaCinema.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="Empresa já cadastrada")
    nova_empresa = models.EmpresaCinema(**empresa.dict())
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa

@router.get("/empresas/", response_model=list[schemas.EmpresaCinema])
def read_empresas(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return db.query(models.EmpresaCinema).offset(skip).limit(limit).all()

# Endpoints para Cinemas
@router.post("/cinemas/", response_model=schemas.Cinema)
def create_cinema(cinema: schemas.CinemaCreate, db: Session = Depends(database.get_db)):
    novo_cinema = models.Cinema(**cinema.dict())
    db.add(novo_cinema)
    db.commit()
    db.refresh(novo_cinema)
    return novo_cinema

@router.get("/cinemas/", response_model=list[schemas.Cinema])
def read_cinemas(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return db.query(models.Cinema).offset(skip).limit(limit).all()

# Endpoints para Salas
@router.post("/salas/", response_model=schemas.Sala)
def create_sala(sala: schemas.SalaCreate, db: Session = Depends(database.get_db)):
    nova_sala = models.Sala(**sala.dict())
    db.add(nova_sala)
    db.commit()
    db.refresh(nova_sala)
    return nova_sala

@router.get("/salas/", response_model=list[schemas.Sala])
def read_salas(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return db.query(models.Sala).offset(skip).limit(limit).all()
