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
    if current_user.tipo_usuario == "Gerente":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")

    return db.query(models.EmpresaCinema).all()

@router.put("/empresas/{empresa_id}", response_model=schemas.EmpresaCinema)
def update_empresa(
    empresa_id: int,
    empresa_update: schemas.EmpresaCinemaUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Somente Admins podem atualizar empresas
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=403, detail="Apenas Admin pode atualizar empresas.")

    # Buscar a empresa no banco de dados
    empresa = db.query(models.EmpresaCinema).filter(models.EmpresaCinema.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Atualizar apenas os campos fornecidos na requisição
    if empresa_update.nome is not None:
        empresa.nome = empresa_update.nome

    if empresa_update.cnpj is not None:
        empresa.cnpj = empresa_update.cnpj
        
    if empresa_update.contato is not None:
        empresa.contato = empresa_update.contato

    db.commit()
    db.refresh(empresa)
    return empresa

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

@router.put("/cinemas/{cinema_id}", response_model=schemas.Cinema)
def update_cinema(
    cinema_id: int,
    cinema_update: schemas.CinemaUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Apenas Admin pode atualizar cinemas
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=403, detail="Apenas Admin pode atualizar cinemas.")

    # Buscar o cinema no banco de dados
    cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()

    if not cinema:
        raise HTTPException(status_code=404, detail="Cinema não encontrado.")

    # Atualizar apenas os campos enviados
    if cinema_update.nome is not None:
        cinema.nome = cinema_update.nome
    if cinema_update.endereco is not None:
        cinema.endereco = cinema_update.endereco
    if cinema_update.empresa_id is not None:
        # Verificar se a empresa existe antes de atualizar
        empresa_existente = db.query(models.EmpresaCinema).filter(models.EmpresaCinema.id == cinema_update.empresa_id).first()
        if not empresa_existente:
            raise HTTPException(status_code=400, detail="Empresa associada não encontrada.")
        cinema.empresa_id = cinema_update.empresa_id

    db.commit()
    db.refresh(cinema)
    return cinema

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
    if current_user.tipo_usuario == "Representante":
        raise HTTPException(status_code=400, detail="Usuáio sem permissão")
    
    # return db.query(models.Sala).offset(skip).limit(limit).all()
    return db.query(models.Sala).all()

@router.put("/salas/{sala_id}", response_model=schemas.Sala)
def update_sala(
    sala_id: int,
    sala_update: schemas.SalaUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Buscar a sala no banco de dados
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()

    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")

    # Apenas Admins ou Gerentes podem atualizar salas
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=403, detail="Apenas Admins podem atualizar salas.")


    # Atualizar apenas os campos enviados
    if sala_update.nome is not None:
        sala.nome = sala_update.nome

    if sala_update.cinema_id is not None:
        # Verificar se o cinema existe antes de atualizar
        cinema_existente = db.query(models.Cinema).filter(models.Cinema.id == sala_update.cinema_id).first()
        
        if not cinema_existente:
            raise HTTPException(status_code=400, detail="Cinema associado não encontrado.")
        sala.cinema_id = sala_update.cinema_id

    db.commit()
    db.refresh(sala)
    return sala

@router.get("/imagens/", response_model=list[schemas.FotoServico])
def read_images(
    #skip: int = 0, 
    #limit: int = 20, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    #if current_user.tipo_usuario == "Representante":
        #raise HTTPException(status_code=400, detail="Usuáio sem permissão")
    
    # return db.query(models.Sala).offset(skip).limit(limit).all()
    return db.query(models.FotoServico).all()