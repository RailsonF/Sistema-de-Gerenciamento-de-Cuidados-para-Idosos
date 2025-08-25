# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Responsavel(Base):
    __tablename__ = "responsaveis"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, index=True)
    cpf = Column(String(11), unique=True, index=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Esta linha cria a relação no lado do Python
    idosos = relationship("Idoso", back_populates="responsavel")

class Idoso(Base):
    __tablename__ = "idosos"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, index=True)
    cpf = Column(String, unique=True, index=True) # Novo campo
    data_nascimento = Column(Date)
    quarto = Column(String, nullable=True)

    # Campo para a Chave Estrangeira
    id_responsavel = Column(Integer, ForeignKey("responsaveis.id"), nullable=True)

    # Esta linha cria a relação no lado do Python
    responsavel = relationship("Responsavel", back_populates="idosos")