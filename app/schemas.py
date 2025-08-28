from pydantic import BaseModel
from datetime import date

#Schema base com campos comuns
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

  class Config:
    #Permite ao Pydantic ler os dados diretamente de objetos SQLAlchemy.
    orm_mode = True