#Importa a classe FastAPi
from fastapi import FastAPI

#Cria a instância da aplicação
app = FastAPI(title="Sistema de Monitoramento de Medicamentos")

#Criando um endpoint de teste
@app.get("/teste", tags=["Root"])
def ler_raiz():
  return {"mensagem": "Bem vindo à APi de monitoramento de Medicamentos "}