from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, database, auth
from typing import List


router = APIRouter()

@router.post("/usuarios/public/", response_model=schemas.Usuario)
def create_usuario_public(
    usuario: schemas.UsuarioCreate, 
    db: Session = Depends(database.get_db)
):
    """Cria um usuário APENAS se não houver um Admin no sistema"""

    # Verifica se já existe um Admin cadastrado
    admin_existente = db.query(models.Usuario).filter(models.Usuario.tipo_usuario == "Admin").first()
    
    if admin_existente:
        raise HTTPException(status_code=403, detail="Já existe um Admin cadastrado. Usuários devem ser criados por um Admin.")

    # Verifica se o e-mail já está cadastrado
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Criptografa a senha antes de salvar
    hashed_password = auth.get_password_hash(usuario.senha)

    # Criar o primeiro usuário (geralmente um Admin)
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hashed_password,
        tipo_usuario=usuario.tipo_usuario,  # Pode ser Admin, Gerente, etc.
        empresa_id=usuario.empresa_id,
        cinema_id=usuario.cinema_id
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@router.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(
    usuario: schemas.UsuarioCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    #if current_user.tipo_usuario != "Admin":
        #raise HTTPException(status_code=400, detail="Usuáio sem permissão")

    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed_password = auth.get_password_hash(usuario.senha)
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hashed_password,
        tipo_usuario=usuario.tipo_usuario,
        empresa_id=usuario.empresa_id,
        cinema_id=usuario.cinema_id
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/usuarios/me", response_model=schemas.Usuario)
def read_current_user(current_user: models.Usuario = Depends(auth.get_current_user)):
    #if current_user.tipo_usuario != "Admin":
       #raise HTTPException(status_code=400, detail="Usuáio sem permissão")
    
    return current_user

@router.put("/usuarios/{user_id}", response_model=schemas.Usuario)
def update_usuario(
    user_id: int,
    usuario_update: schemas.UsuarioUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Permitir que um Admin atualize qualquer usuário.
    if current_user.tipo_usuario != "Admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Operação não permitida")

    user_db = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario_update.nome is not None:
        user_db.nome = usuario_update.nome

    if usuario_update.email is not None:
        user_db.email = usuario_update.email

    if usuario_update.senha is not None:
        user_db.senha = auth.get_password_hash(usuario_update.senha)

    if usuario_update.tipo_usuario is not None:
        user_db.tipo_usuario = usuario_update.tipo_usuario

    if usuario_update.empresa_id is not None:
        user_db.empresa_id = usuario_update.empresa_id

    if usuario_update.cinema_id is not None:
        user_db.cinema_id = usuario_update.cinema_id

    db.commit()
    db.refresh(user_db)
    return user_db

@router.get("/usuarios/", response_model=List[schemas.Usuario])
def get_usuarios(
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Se for Admin, retorna todos os usuários
    if current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=403, detail="Operação não permitida")
    
    return db.query(models.Usuario).all()
