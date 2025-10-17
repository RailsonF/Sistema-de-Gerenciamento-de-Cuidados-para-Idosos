# Sistema de Gerenciamento de Cuidados para Idosos - API Back-end API

## 📖 Descrição

Este repositório contém o código-fonte da API back-end para o **Sistema de Gerenciamento de Cuidados para Idosos**.

A API é responsável por toda a lógica de negócio, gerenciamento de dados e autenticação de usuários. Ela fornece um conjunto de endpoints RESTful para que as aplicações front-end (painel de administração, app do cuidador e monitor da TV) possam interagir com o sistema.

## ✨ Funcionalidades Principais

* **Autenticação de Usuários:** Sistema de login seguro baseado em Tokens JWT.
* **Gerenciamento Completo (CRUD):** Endpoints para criar, ler, atualizar e deletar dados de Idosos, Responsáveis, Usuários (cuidadores/admins), Medicamentos e Prescrições.
* **Lógica de Monitoramento:** Um endpoint (`GET /monitor`) que fornece dados em tempo real sobre as prescrições pendentes, já classificadas por urgência.
* **Rastreamento de Ações:** Endpoint para registrar a administração de medicamentos, vinculando a ação a um usuário e a uma prescrição específica.
* **Documentação Interativa:** Geração automática de documentação interativa com Swagger UI.

## 🛠️ Tecnologias Utilizadas

* **Framework:** FastAPI
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy com Alembic para migrações
* **Validação de Dados:** Pydantic
* **Autenticação:** JWT (JSON Web Tokens) e Passlib para hashing de senhas
* **Servidor ASGI:** Uvicorn

## 🚀 Guia de Instalação e Execução Local

Siga estes passos para configurar e rodar a API na sua máquina local, permitindo o desenvolvimento do front-end.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:
* [Git](https://git-scm.com/)
* [Python](https://www.python.org/downloads/) (versão 3.8 ou superior)
* [PostgreSQL](https://www.postgresql.org/download/) (banco de dados)

### Passos para Instalação

**1. Clonar o Repositório**
```bash
git clone <https://github.com/RailsonF/Sistema-de-Gerenciamento-de-Cuidados-para-Idosos.git>
cd <Sistema-de-Gerenciamento-de-Cuidados-para-Idosos>
```

**2. Criar o Arquivo de Dependências**
*Se o arquivo `requirements.txt` ainda não existir, o desenvolvedor back-end deve criá-lo com o comando:*
```bash
pip freeze > requirements.txt
```

**3. Criar e Ativar o Ambiente Virtual**
```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

**4. Instalar as Dependências**
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

**5. Configurar o Banco de Dados**
- Abra o pgAdmin ou use o `psql`.
- Crie um novo banco de dados com o nome `monitor_medicamentos`.

**6. Configurar as Variáveis de Ambiente**
A API precisa de um arquivo `.env` para carregar configurações sensíveis, como a senha do banco e a chave secreta JWT.
- Crie um arquivo chamado `.env` na raiz do projeto.
- Copie o conteúdo do arquivo `.env.example` (se existir) ou use o modelo abaixo e preencha com suas configurações locais:
```dotenv
# .env
DATABASE_URL="postgresql://postgres:SUA_SENHA_DO_POSTGRES@localhost/monitor_medicamentos"
SECRET_KEY="SUA_CHAVE_SECRETA_GERADA_COM_OPENSSL"
```

**7. Aplicar as Migrações do Banco de Dados**
Para garantir que o banco de dados tenha todas as tabelas mais recentes:
```bash
alembic upgrade head
```

**8. Executar a API**
Finalmente, inicie o servidor local:
```bash
uvicorn app.main:app --reload
```
A API estará rodando em `http://127.0.0.1:8000`.

##  penggunaan da API

### Documentação Interativa (Swagger UI)

A forma mais fácil de explorar e testar todos os endpoints é através da documentação interativa gerada automaticamente. Com o servidor rodando, acesse:

**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Lá você encontrará a lista completa de endpoints, os formatos de dados (schemas) que eles esperam e retornam, e poderá executar testes diretamente pelo navegador.

### Fluxo de Autenticação

Endpoints que envolvem a criação ou modificação de dados importantes são protegidos. Para acessá-los, siga este fluxo:

1.  **Faça o Login:** Envie uma requisição `POST` para o endpoint `/login` com o `username` (e-mail) e `password` do usuário.
2.  **Receba o Token:** A API retornará um `access_token`.
3.  **Envie o Token:** Para cada requisição a um endpoint protegido, inclua o token no cabeçalho (`header`) da requisição da seguinte forma:
    `Authorization: Bearer <seu_token_aqui>`

Na documentação `/docs`, você pode usar o botão "Authorize" no canto superior direito para adicionar o token e testar os endpoints protegidos facilmente.

### Endpoints Principais

| Método | Endpoint | Descrição | Autenticação? |
| :--- | :--- | :--- | :--- |
| `GET` | `/monitor/` | Retorna os dados em tempo real para a tela do monitor. | Não |
| `POST`| `/login` | Autentica um usuário e retorna um token JWT. | Não |
| `POST`| `/usuarios/` | Cadastra um novo usuário (cuidador/admin). | Não |
| `POST`| `/prescricoes/{id}/administrar` | Registra que um medicamento foi administrado. | **Sim** |
| `POST`| `/prescricoes/` | Cria uma nova prescrição de medicamento para um idoso. | **Sim** |

### Contrato de Dados (Schemas)

Para ver a estrutura detalhada de todos os objetos JSON (quais campos, tipos de dados e se são opcionais), consulte a seção **"Schemas"** no final da página da documentação interativa em `/docs`.
