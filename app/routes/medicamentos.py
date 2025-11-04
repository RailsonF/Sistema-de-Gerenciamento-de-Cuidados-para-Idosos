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

@router.post("/", response_model=schemas.Medicamento, status_code=status.HTTP_201_CREATED)
def criar_novo_medicamento(medicamento: schemas.MedicamentoBase, db: Session = Depends(get_db)):
    # (Esta é a rota de criação que você provavelmente já tinha no main.py)
    # (Podemos movê-la para cá para organizar)
    return crud.create_medicamento(db=db, medicamento=medicamento)

@router.get("/", response_model=List[schemas.Medicamento])
def listar_todos_medicamentos(db: Session = Depends(get_db)):
    # (Esta é a rota de listagem que você provavelmente já tinha)
    return crud.get_medicamentos(db=db)

# --- NOVO ENDPOINT DE ATUALIZAÇÃO (PUT) ---
@router.put("/{medicamento_id}", response_model=schemas.Medicamento)
def atualizar_medicamento(
    medicamento_id: int, 
    medicamento_data: schemas.MedicamentoBase, 
    db: Session = Depends(get_db)
):
    db_medicamento = crud.update_medicamento(db, medicamento_id, medicamento_data)
    if db_medicamento is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return db_medicamento

# --- NOVO ENDPOINT DE EXCLUSÃO (DELETE) ---
@router.delete("/{medicamento_id}", response_model=schemas.Medicamento)
def deletar_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    deleted_medicamento = crud.delete_medicamento(db, medicamento_id)

    if deleted_medicamento is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    if deleted_medicamento == "CONFLITO":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail="Este medicamento não pode ser excluído pois está em uso em uma prescrição.")

    return deleted_medicamento