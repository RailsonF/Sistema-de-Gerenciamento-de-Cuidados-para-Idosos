# settings.py
import os
from dotenv import load_dotenv

#carrega as variáveis do .env para o ambiente
load_dotenv()

# Pega a variável DATABASE_URL do ambiente
DATABASE_URL = os.getenv("DATABASE_URL")