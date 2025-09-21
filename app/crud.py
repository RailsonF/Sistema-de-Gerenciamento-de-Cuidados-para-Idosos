# app/crud.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta
from . import models, schemas
from . import auth


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

# --- Funções CRUD para AdministracaoLog ---
def create_administracao_log(db: Session, id_prescricao: int, id_usuario: int):
    db_log = models.AdministracaoLog(id_prescricao=id_prescricao, id_usuario = id_usuario)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# --- LÓGICA DO MONITOR ---
def get_monitor_data(db: Session):
    agora = datetime.now().time()
    hoje = datetime.now().date()

    # 1. Encontra os IDs das prescrições administradas HOJE
    ids_administrados_hoje = db.query(models.AdministracaoLog.id_prescricao).filter(
        func.date(models.AdministracaoLog.data_hora_administracao) == hoje
    )

    # 2. Busca todas as prescrições pendentes (que não estão na lista de administradas hoje)
    #    e já carrega os dados do idoso e do medicamento (eager loading)
    prescricoes_pendentes = db.query(models.Prescricao).options(
        joinedload(models.Prescricao.idoso),
        joinedload(models.Prescricao.medicamento)
    ).filter(models.Prescricao.id.notin_(ids_administrados_hoje)).all()

    # 3. Classifica as prescrições pendentes
    proximos = []
    na_hora = []
    urgentes = []

    # Converte a hora atual para segundos para facilitar a comparação
    agora_em_segundos = agora.hour * 3600 + agora.minute * 60 + agora.second

    for p in prescricoes_pendentes:
        horario_em_segundos = p.horario_prescrito.hour * 3600 + p.horario_prescrito.minute * 60

        diferenca = horario_em_segundos - agora_em_segundos

        item_monitor = {
            "id_prescricao": p.id,
            "horario_prescrito": p.horario_prescrito,
            "dosagem": p.dosagem,
            "nome_idoso": p.idoso.nome_completo,
            "quarto_idoso": p.idoso.quarto,
            "nome_medicamento": p.medicamento.nome
        }

        # Lógica de classificação
        # "Urgente": mais de 20 minutos de atraso
        if diferenca < -1200: # 20 minutos * 60 segundos
            urgentes.append(item_monitor)
        # "Na Hora": entre 20 minutos de atraso e o horário exato
        elif -1200 <= diferenca <= 0:
            na_hora.append(item_monitor)
        # "Próximos": até 10 minutos antes do horário
        elif 0 < diferenca <= 600: # 10 minutos * 60 segundos
            proximos.append(item_monitor)

    return {"proximos": proximos, "na_hora": na_hora, "urgentes": urgentes}

# --- FUNÇÃO CRUD USUÁRIO ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()
def create_user(db: Session, usuario: schemas.UsuarioCreate):
    # Pega a senha do schema e a transforma em um hash
    hashed_password = auth.get_password_hash(usuario.password)
    # Cria o objeto do modelo, substituindo a senha pelo hash
    db_usuario = models.Usuario(
        email=usuario.email,
        nome_completo=usuario.nome_completo,
        senha_hash=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario