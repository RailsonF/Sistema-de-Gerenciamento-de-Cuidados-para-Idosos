from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session #Importa a classe FastAPi

from . import crud, models, schemas
from .database import SessionLocal, engine #Importa o "motor do banco"
from . import models #Importa os modelos
 
#Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

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