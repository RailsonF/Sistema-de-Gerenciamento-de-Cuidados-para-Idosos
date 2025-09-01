from pydantic import BaseModel
from datetime import date
from typing import List

#---- Schemas para Responsável ----#
class ResponsavelBase(BaseModel):
  nome_completo: str
  cpf: str
  telefone: str | None = None
  email: str | None = None

class ResponsavelCreate(ResponsavelBase):
  pass

class Responsavel(ResponsavelBase):
  id: int
  class Config:
    orm_mode = True

#---- Schema para idoso ----#
class idosoBase(BaseModel):
  nome_completo: str
  cpf: str
  data_nascimento: date
  quarto: str | None = None #pode ser str ou None, com valor padrão None
  id_responsavel: int | None = None

# Schema para a criação de um novo idoso (o que recebemos na API)
class IdosoCreate(idosoBase):
  pass

#Schema completo para retornar os dados (o que enviamos da API)
class Idoso(idosoBase):
  id: int
  responsavel: Responsavel | None = None

  class Config:
    #Permite ao Pydantic ler os dados diretamente de objetos SQLAlchemy.
    orm_mode = True