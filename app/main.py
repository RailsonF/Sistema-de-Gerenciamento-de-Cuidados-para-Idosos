from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, medicamentos, idosos, responsaveis, prescricoes, monitor, usuarios
 #Adicione esta linha temporariamente para apagar as tabelas
#models.Base.metadata.drop_all(bind=engine) 

#Cria as tabelas no banco de dados
#models.Base.metadata.create_all(bind=engine)

#Cria a instância da aplicação
app = FastAPI(title="Sistema de Monitoramento de Medicamentos")

#Configurando o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Incluindo os roteadores na aplicação 
app.include_router(auth_routes.router)
app.include_router(medicamentos.router)
app.include_router(idosos.router)
app.include_router(responsaveis.router)
app.include_router(prescricoes.router)
app.include_router(monitor.router)
app.include_router(usuarios.router)

#Criando um endpoint de teste
@app.get("/", tags=["Root"])
async def ler_raiz():
  return {"Status": "API OK"}

