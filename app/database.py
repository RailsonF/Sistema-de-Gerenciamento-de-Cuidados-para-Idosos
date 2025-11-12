import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()  # Carrega as variáveis do arquivo .env

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    # Se não encontrar no .env, use a URL antiga como fallback (ou mostre um erro)
    print("Aviso: DATABASE_URL não encontrada no .env, usando fallback.")
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sua_senha_local@localhost/monitor_medicamentos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()