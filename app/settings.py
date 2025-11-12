# settings.py
# settings.py
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env para o ambiente (apenas em modo local)
load_dotenv()

# Pega a variável DATABASE_URL do ambiente (Render ou local)
#DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql://monitor_db_pdkk_user:ydMNzbR2xHwxbqu802fTbIZYwNdqjdQJ@dpg-d47uis6r433s739o32ug-a/monitor_db_pdkk"
# Caso esteja rodando localmente e não tenha variável configurada
if DATABASE_URL is None:
    DATABASE_URL = "postgresql://usuario:senha@localhost:5432/nome_do_banco"

# Corrige prefixo do Render (alguns vêm como postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
