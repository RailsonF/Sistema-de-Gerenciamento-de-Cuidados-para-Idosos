from pydantic import BaseModel
from datetime import datetime, date, time
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
        from_atributes = True

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
        from_atributes = True

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
    from_atributes = True

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
    from_atributes = True

class AdministracaoLogBase(BaseModel):
   id_prescricao: int
  
class AdministracaoLogcreate(AdministracaoLogBase):
   pass

class AdministracaoLog(AdministracaoLogBase):
   id: int
   data_hora_administracao: datetime

   class Config:
      from_atributes = True

# ---SCHEMAS PARA O MONITOR ---
class MonitorPrescricao(BaseModel):
   id_prescricao: int
   horario_prescrito: time
   dosagem: str
   nome_idoso: str
   quarto_idoso: str | None
   nome_medicamento: str

   class Config:
    from_atributes = True

# Descreve a estrutura final da resposta do endpoint /monitor
class MonitorData(BaseModel):
    proximos: List[MonitorPrescricao]
    na_hora: List[MonitorPrescricao]
    urgentes: List[MonitorPrescricao]

#Schemas para usuario
class UsuarioBase(BaseModel):
   nome_completo: str
   email: str

class UsuarioCreate(UsuarioBase):
   password: str

class Usuario(UsuarioBase):
   id: int
   is_active: bool
   class Config:
      from_atributes = True

class Token(BaseModel):
   access_token: str
   token_type: str

class TokenData(BaseModel):
   email: str | None = None