from fastapi import FastAPI #Importa a classe FastAPi
from . import models #Importa os modelos
from .database import engine #Importa o "motor do banco" 

#Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

#Cria a instância da aplicação
app = FastAPI(title="Sistema de Monitoramento de Medicamentos")

#Criando um endpoint de teste
@app.get("/", tags=["Root"])
async def ler_raiz():
  return {"Status": "API conectada ao banco de dados "}