from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session #Importa a classe FastAPi
from ..dependencies import get_db
from ..auth import get_current_user
from .. import crud, models, schemas
from typing import List

router = APIRouter(
    prefix="/usuarios", # Todas as rotas aqui começarão com /medicamentos
    tags=["Funcionários"],  # Agrupa na documentação do /docs
    #dependencies=[Depends(auth.get_current_user)] # PROTEGE TODAS AS ROTAS DESTE ARQUIVO
)

@router.get("/", response_model=List[schemas.Usuario])
def ler_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    funcionarios = crud.get_funcionarios(db, skip=skip, limit=limit)
    return funcionarios