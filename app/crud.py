# app/crud.py

from sqlalchemy.orm import Session, joinedload
from . import models, schemas

# --- Funções CRUD para Idoso ---
def get_idoso(db: Session, idoso_id: int):
    return db.query(models.Idoso).filter(models.Idoso.id == idoso_id).first()

def get_idosos(db: Session, skip: int, limit: int = 100):
    '''
    --> db.query(models.Idoso): Inicia uma consulta na tabela idosos.
    --> offset(skip).limit(limit): Comandos para paginação. Permitem que o front-end peça os dados em "pedaços" (ex:    pule os 10 primeiros e me dê os próximos 100").
    --> all(): Executa a consulta e retorna todos os resultados encontrados como uma lista.
    '''
    return db.query(models.Idoso).options(joinedload(models.Idoso.responsavel)).offset(skip).limit(limit).all()

def create_idoso(db: Session, idoso: schemas.IdosoCreate):
    # Cria um objeto do modelo SQLAlchemy a partir dos dados do schema Pydantic
    db_idoso = models.Idoso(
        nome_completo=idoso.nome_completo,
        cpf=idoso.cpf,
        data_nascimento=idoso.data_nascimento,
        quarto=idoso.quarto,
        id_responsavel=idoso.id_responsavel
    )
    db.add(db_idoso)  # Adiciona o objeto à sessão do banco
    db.commit()      # Confirma a transação, salvando no banco
    db.refresh(db_idoso) # Atualiza o objeto com os dados do banco (como o novo id)
    return db_idoso

# --- Funções CRUD para Responsavel ---
def get_responsavel_by_cpf(db: Session, cpf: str):
    return db.query(models.Responsavel).filter(models.Responsavel.cpf == cpf).first()

def get_responsaveis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Responsavel).offset(skip).limit(limit).all()

def create_responsavel(db: Session, responsavel: schemas.ResponsavelCreate):
    db_responsavel = models.Responsavel(
        nome_completo=responsavel.nome_completo,
        cpf=responsavel.cpf,
        telefone=responsavel.telefone,
        email=responsavel.email
    )
    db.add(db_responsavel)
    db.commit()
    db.refresh(db_responsavel)
    return db_responsavel

# --- Funções CRUD para Medicamento ---
def get_medicamento(db: Session, medicamento_id: int):
    return db.query(models.Medicamento).filter(models.Medicamento.id == medicamento_id).first()

def get_medicamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Medicamento).offset(skip).limit(limit).all()

def create_medicamento(db: Session, medicamento: schemas.MedicamentoCreate):
    db_medicamento = models.Medicamento(**medicamento.dict())
    db.add(db_medicamento)
    db.commit()
    db.refresh(db_medicamento)
    return db_medicamento

# --- Funções CRUD para Prescricao ---
def create_prescricao(db: Session, prescricao: schemas.PrescricaoCreate):
    db_prescricao = models.Prescricao(**prescricao.dict())
    db.add(db_prescricao)
    db.commit()
    db.refresh(db_prescricao)
    return db_prescricao