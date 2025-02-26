from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
from typing import List, Optional

from pathlib import Path
import shutil

router = APIRouter()

# Endpoint para criação de um serviço (Encarregado)
@router.post("/servicos/", response_model=schemas.Servico)
def create_servico(
    servico: schemas.ServicoCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):

    # Verificar se não é Encarregado nem Admin e lança um erro
    if current_user.tipo_usuario != "Encarregado" and current_user.tipo_usuario != "Admin":
        raise HTTPException(status_code=403, detail="Operação permitida apenas para Encarregados")
    
    # Verifica se as fotos foram passadas e lança um erro
    if not servico.fotos_urls or len(servico.fotos_urls) == 0:
        raise HTTPException(status_code=400, detail="Pelo menos uma foto deve ser enviada")
    
    # Registro novo servoço
    novo_servico = models.Servico(
        encarregado_id=servico.encarregado_id,
        sala_id=servico.sala_id,
        tipo_servico=servico.tipo_servico,
        observacoes=servico.observacoes,
        status="Pendente"
    )

    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    # Percorre fotos
    for url in servico.fotos_urls:

        # Registro nova foto
        nova_foto = models.FotoServico(servico_id=novo_servico.id, url_foto=url)
        db.add(nova_foto)

    db.commit()

    return novo_servico

# Endpoint para atualizar o status do serviço (Gerente ou Admin)
@router.put("/servicos/{servico_id}", response_model=schemas.Servico)
def update_servico(
    servico_id: int,
    servico_update: schemas.ServicoUpdate,
    #historico: schemas.HistoricoStatusCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Buscar serviço no banco
    servico = db.query(models.Servico).filter(models.Servico.id == servico_id).first()

    # Verifica a existencia do serviço e lança um erro
    if not servico:
        
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    # Validação de permição por tipo de usuário

    # Admin: Só pode atualizar para Concluído, Em Análise e Recusado
    if current_user.tipo_usuario == "Admin":

        if servico_update.status and servico_update.status not in ["Concluído", "Em Análise", "Recusado"]:

            raise HTTPException(status_code=400, detail="Status inválido para Admin")
        
        servico.status = servico_update.status

    # Gerente: Só pode atualizar para Aprovado ou Recusado
    elif current_user.tipo_usuario == "Gerente":
    
        if servico_update.status and servico_update.status not in ["Aprovado", "Recusado"]:

            raise HTTPException(status_code=400, detail="Status inválido para Gerente")
                
        servico.status = servico_update.status

    # Encarregado: Só pode atualizar Observacoes e fotos
    elif current_user.tipo_usuario == "Encarregado":

        if servico_update.status:

            raise HTTPException(status_code=403, detail="Status inválido para Encarregado")

        if servico_update.observacoes:

            servico.observacoes = servico_update.observacoes

        if servico_update.fotos_urls:

            # Deletar fotos antigas e adicionar novas
            db.query(models.FotoServico).filter(models.FotoServico.servico_id == servico_id).delete()
            
            for url in servico_update.fotos_urls:

                nova_foto = models.FotoServico(servico_id=servico.id, url_foto=url)
                db.add(nova_foto)

        servico.status = "Pendente"

    # Representante: Não pode modificar nada
    else:

        raise HTTPException(status_code=403, detail="Operação não permitida")
    
    if servico_update.status:

        novo_historico = models.HistoricoStatus(
            servico_id=servico.id,
            usuario_id=current_user.id,
            status=servico.status,
            observacoes=servico_update.observacoes
        )

        db.add(novo_historico)
        db.commit()
        db.refresh(servico)

    else:

        novo_historico = models.HistoricoStatus(
            servico_id=servico.id,
            usuario_id=current_user.id,
            status="Pendente",
            observacoes=servico_update.observacoes
        )

        db.add(novo_historico)
        db.commit()
        db.refresh(servico)

    return servico

# Endpoint para listar serviços (filtrados conforme o tipo de usuário)
@router.get("/servicos/", response_model=list[schemas.Servico])
def read_servicos(skip: int = 0, limit: int = 10,
                  db: Session = Depends(database.get_db),
                  current_user: models.Usuario = Depends(auth.get_current_user)):
    if current_user.tipo_usuario == "Encarregado":
        servicos = db.query(models.Servico).filter(models.Servico.encarregado_id == current_user.id)
    elif current_user.tipo_usuario == "Gerente":
        servicos = db.query(models.Servico).join(models.Sala).join(models.Cinema).filter(models.Cinema.id == current_user.cinema_id)
    elif current_user.tipo_usuario == "Representante":
        servicos = db.query(models.Servico).join(models.Sala).join(models.Cinema).filter(models.Cinema.empresa_id == current_user.empresa_id)
    else:
        servicos = db.query(models.Servico)
    return servicos.offset(skip).limit(limit).all()
