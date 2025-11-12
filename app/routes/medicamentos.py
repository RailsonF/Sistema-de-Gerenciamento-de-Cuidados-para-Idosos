# app/routes/medicamentos_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..dependencies import get_db

router = APIRouter(
    prefix="/medicamentos", # Todas as rotas aqui começarão com /medicamentos
    tags=["Medicamentos"],  # Agrupa na documentação do /docs
    #dependencies=[Depends(auth.get_current_user)] # PROTEGE TODAS AS ROTAS DESTE ARQUIVO
)



@router.post("/", response_model=schemas.Medicamento)
def criar_novo_medicamento(medicamento: schemas.MedicamentoCreate, db: Session = Depends(get_db)):
    return crud.create_medicamento(db=db, medicamento=medicamento)

@router.get("/", response_model=List[schemas.Medicamento])
def ler_medicamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicamentos = crud.get_medicamentos(db, skip=skip, limit=limit)
    return medicamentos

@router.patch("/{medicamento_id}", response_model=schemas.Medicamento)
def atualizar_medicamento(
    medicamento_id: int, 
    medicamento_data: schemas.MedicamentoUpdate, 
    db: Session = Depends(get_db)
):
    db_medicamento = crud.update_medicamento(db, medicamento_id, medicamento_data)
    if db_medicamento is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return db_medicamento

@router.delete("/{medicamento_id}", response_model=schemas.Medicamento)
def deletar_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    deleted_medicamento = crud.delete_medicamento(db, medicamento_id)

    if deleted_medicamento is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    if deleted_medicamento == "CONFLITO":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail="Este medicamento não pode ser excluído pois está em uso em uma prescrição.")
    return deleted_medicamento