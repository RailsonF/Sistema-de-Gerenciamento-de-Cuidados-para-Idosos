from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..dependencies import get_db

router = APIRouter(
    prefix="/responsaveis", # Todas as rotas aqui começarão com /medicamentos
    tags=["Responsáveis"],  # Agrupa na documentação do /docs
    #dependencies=[Depends(auth.get_current_user)] # PROTEGE TODAS AS ROTAS DESTE ARQUIVO
)

@router.post("/criar/", response_model=schemas.Responsavel)
def criar_novo_responsavel(responsavel: schemas.ResponsavelCreate, db: Session = Depends(get_db)):
    # (Opcional, mas boa prática) Verificar se o CPF já existe
    # db_idoso = crud.get_idoso_by_cpf(db, cpf=idoso.cpf)
    # if db_idoso:
    #     raise HTTPException(status_code=400, detail="CPF já cadastrado")
    return crud.create_responsavel(db=db, responsavel=responsavel)

@router.get("/listar/", response_model=List[schemas.Responsavel])
def ler_responsaveis(skip: int =0 , limit: int = 100, db: Session = Depends(get_db)):
    db_responsaveis = crud.get_responsaveis(db, skip= skip, limit=limit)
    return db_responsaveis

@router.put("/deletar/{responsavel_id}", response_model=schemas.Responsavel)
def atualizar_responsavel(
    responsavel_id: int, 
    responsavel_data: schemas.ResponsavelBase, 
    db: Session = Depends(get_db)
):
    db_responsavel = crud.update_responsavel(db, responsavel_id, responsavel_data)
    if db_responsavel is None:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    return db_responsavel

@router.delete("/excluir/{responsavel_id}")
def excluir_responsavel(
    responsavel_id: int, 
    db:Session = Depends(get_db)):
    deleted_responsavel  = crud.deleted_responsavel(db, responsavel_id)