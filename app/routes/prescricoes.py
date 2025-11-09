from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session #Importa a classe FastAPi
from ..dependencies import get_db
from ..auth import get_current_user
from .. import crud, models, schemas

router = APIRouter(
    prefix="/prescricoes", # Todas as rotas aqui começarão com /medicamentos
    tags=["Prescrições"],  # Agrupa na documentação do /docs
    #dependencies=[Depends(auth.get_current_user)] # PROTEGE TODAS AS ROTAS DESTE ARQUIVO
)


# --- ENDPOINTS PARA PRESCRIÇÕES ---
@router.post("/prescricoes/", response_model=schemas.Prescricao)
def criar_nova_prescricao(prescricao: schemas.PrescricaoCreate, db: Session = Depends(get_db)):
    # Validação: Verificar se o idoso e o medicamento existem antes de criar a prescrição
    db_idoso = crud.get_idoso(db, idoso_id=prescricao.id_idoso)
    if not db_idoso:
        raise HTTPException(status_code=404, detail="Idoso não encontrado")

    db_medicamento = crud.get_medicamento(db, medicamento_id=prescricao.id_medicamento)
    if not db_medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    return crud.create_prescricao(db=db, prescricao=prescricao)

@router.post("/prescricoes/{prescricao_id}/administrar", response_model=schemas.AdministracaoLog)
def registrar_administracao(
    prescricao_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_user)
    ):
    return crud.create_administracao_log(
        db=db, 
        id_prescricao=prescricao_id,
        id_usuario= current_user.id
        )