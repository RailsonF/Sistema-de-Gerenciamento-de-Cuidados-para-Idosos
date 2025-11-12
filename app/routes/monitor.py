from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session #Importa a classe FastAPi
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/monitor", # Todas as rotas aqui começarão com /medicamentos
    tags=["Monitor de dados"],  # Agrupa na documentação do /docs
    #dependencies=[Depends(auth.get_current_user)] # PROTEGE TODAS AS ROTAS DESTE ARQUIVO
)

# --- ENDPOINT DO MONITOR ---
@router.get("/", response_model=schemas.MonitorData)
def ler_dados_monitor(db: Session = Depends(get_db)):
    dados = crud.get_monitor_data(db)
    return dados