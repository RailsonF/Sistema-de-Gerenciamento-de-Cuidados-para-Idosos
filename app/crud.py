# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

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

def get_idosos(db: Session, skip: int, limit: int = 100):
    '''
    --> db.query(models.Idoso): Inicia uma consulta na tabela idosos.
    --> offset(skip).limit(limit): Comandos para paginação. Permitem que o front-end peça os dados em "pedaços" (ex:    pule os 10 primeiros e me dê os próximos 100").
    --> all(): Executa a consulta e retorna todos os resultados encontrados como uma lista.
    '''
    return db.query(models.Idoso).offset(skip).limit(limit).all()