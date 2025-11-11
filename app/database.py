# # database.py

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.settings import DATABASE_URL

# # Cria o "motor" de conexão com o banco
# engine = create_engine(DATABASE_URL)

# # Cria uma classe para gerenciar as "conversas" (sessões) com o banco
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Cria uma classe Base que usaremos para criar nossos modelos (tabelas)
# Base = declarative_base()

#Teste de url para render:
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # importante para carregar o .env

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
