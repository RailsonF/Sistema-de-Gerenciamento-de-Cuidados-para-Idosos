from pydantic import BaseModel
from datetime import date, time
from typing import List

#---- Schemas para Medicamento ----#
class MedicamentoBase(BaseModel):
    nome: str
    unidade_medida: str

class MedicamentoCreate(MedicamentoBase):
    pass

class Medicamento(MedicamentoBase):
    id: int
    class Config:
        orm_mode = True

#---- Schemas para Prescricao ----#
class PrescricaoBase(BaseModel):
    dosagem: str
    horario_prescrito: time
    id_idoso: int
    id_medicamento: int

class PrescricaoCreate(PrescricaoBase):
    pass

class Prescricao(PrescricaoBase):
    id: int
    medicamento: Medicamento # Para aninhar os dados do medicamento
    class Config:
        orm_mode = True

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
  prescricoes: List[Prescricao] = [] #Um idoso pode ter varias prescrições

  class Config:
    #Permite ao Pydantic ler os dados diretamente de objetos SQLAlchemy.
    orm_mode = True