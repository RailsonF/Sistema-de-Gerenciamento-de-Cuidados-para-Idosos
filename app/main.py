from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session #Importa a classe FastAPi
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine #Importa o "motor do banco"
from . import models #Importa os modelos
 

# Adicione esta linha temporariamente para apagar as tabelas
#models.Base.metadata.drop_all(bind=engine) 

#Cria as tabelas no banco de dados
#models.Base.metadata.create_all(bind=engine)

#Cria a instância da aplicação
app = FastAPI(title="Sistema de Monitoramento de Medicamentos")

#Criando um endpoint de teste
@app.get("/", tags=["Root"])
async def ler_raiz():
  return {"Status": "API conectada ao banco de dados "}


# Função "Dependency" para gerenciar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/idosos/", response_model=schemas.Idoso)
def criar_novo_idoso(idoso: schemas.IdosoCreate, db: Session = Depends(get_db)):
    # (Opcional, mas boa prática) Verificar se o CPF já existe
    # db_idoso = crud.get_idoso_by_cpf(db, cpf=idoso.cpf)
    # if db_idoso:
    #     raise HTTPException(status_code=400, detail="CPF já cadastrado")
    return crud.create_idoso(db=db, idoso=idoso)

@app.get("/idosos/", response_model=List[schemas.Idoso])
def ler_idosos(skip: int =0 , limit: int = 100, db: Session = Depends(get_db)):
    idosos = crud.get_idosos(db, skip= skip, limit=limit)
    return idosos

# --- ENDPOINTS PARA RESPONSAVEIS ---

@app.post("/responsaveis/", response_model=schemas.Responsavel)
def criar_novo_responsavel(responsavel: schemas.ResponsavelCreate, db: Session = Depends(get_db)):
    db_responsavel = crud.get_responsavel_by_cpf(db, cpf=responsavel.cpf)
    if db_responsavel:
        raise HTTPException(status_code=400, detail="CPF do responsável já cadastrado")
    return crud.create_responsavel(db=db, responsavel=responsavel)

@app.get("/responsaveis/", response_model=List[schemas.Responsavel])
def ler_responsaveis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    responsaveis = crud.get_responsaveis(db, skip=skip, limit=limit)
    return responsaveis

# app/main.py

# ... (todo o código anterior continua aqui) ...

# --- ENDPOINTS PARA MEDICAMENTOS ---

@app.post("/medicamentos/", response_model=schemas.Medicamento)
def criar_novo_medicamento(medicamento: schemas.MedicamentoCreate, db: Session = Depends(get_db)):
    return crud.create_medicamento(db=db, medicamento=medicamento)

@app.get("/medicamentos/", response_model=List[schemas.Medicamento])
def ler_medicamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicamentos = crud.get_medicamentos(db, skip=skip, limit=limit)
    return medicamentos

# --- ENDPOINTS PARA PRESCRIÇÕES ---

@app.post("/prescricoes/", response_model=schemas.Prescricao)
def criar_nova_prescricao(prescricao: schemas.PrescricaoCreate, db: Session = Depends(get_db)):
    # Validação: Verificar se o idoso e o medicamento existem antes de criar a prescrição
    db_idoso = crud.get_idoso(db, idoso_id=prescricao.id_idoso)
    if not db_idoso:
        raise HTTPException(status_code=404, detail="Idoso não encontrado")

    db_medicamento = crud.get_medicamento(db, medicamento_id=prescricao.id_medicamento)
    if not db_medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")

    return crud.create_prescricao(db=db, prescricao=prescricao)

@app.post("/prescricoes/{prescricao_id}/administrar")
def registrar_administracao(prescricao_id: int, db: Session = Depends(get_db)):
    return crud.create_administracao_log(db=db, id_prescricao=prescricao_id)

# --- ENDPOINT DO MONITOR ---
@app.get("/monitor/", response_model=schemas.MonitorData)
def ler_dados_monitor(db: Session = Depends(get_db)):
    dados = crud.get_monitor_data(db)
    return dados