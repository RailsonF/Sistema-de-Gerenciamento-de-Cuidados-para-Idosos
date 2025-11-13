from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..dependencies import get_db

router = APIRouter(
    prefix="/idosos", # Todas as rotas aqui começarão com /medicamentos
    tags=["Idosos"],  # Agrupa na documentação do /docs
    #dependencies=[Depends(auth.get_current_user)] # PROTEGE TODAS AS ROTAS DESTE ARQUIVO
)

@router.post("/", response_model=schemas.Idoso)
def criar_novo_idoso(idoso: schemas.IdosoCreate, db: Session = Depends(get_db)):
    # (Opcional, mas boa prática) Verificar se o CPF já existe
    # db_idoso = crud.get_idoso_by_cpf(db, cpf=idoso.cpf)
    # if db_idoso:
    #     raise HTTPException(status_code=400, detail="CPF já cadastrado")
    return crud.create_idoso(db=db, idoso=idoso)

@router.get("/", response_model=List[schemas.Idoso])
def ler_idosos(skip: int =0 , limit: int = 100, db: Session = Depends(get_db)):
    idosos = crud.get_idosos(db, skip= skip, limit=limit)
    return idosos

@router.put("/{idoso_id}", response_model=schemas.Idoso)
def atualizar_idoso(
    idoso_id: int, 
    idoso_data: schemas.idosoBase, 
    db: Session = Depends(get_db)
):
    db_idoso = crud.update_idoso(db, idoso_id, idoso_data)
    if db_idoso is None:
        raise HTTPException(status_code=404, detail="Idoso não encontrado")
    return db_idoso

@router.delete("/{idoso_id}")
def excluir_idoso(
    idoso_id: int, 
    db:Session = Depends(get_db)):
    deleted_idoso  = crud.deleted_idoso