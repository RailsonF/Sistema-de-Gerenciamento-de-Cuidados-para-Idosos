# Gestão Guardião - API Back-end

## Descrição

Este repositório contém o código-fonte da API back-end para o **Gestão Guardião**.

A API é responsável por toda a lógica de negócio, gerenciamento de dados e autenticação de usuários. Ela fornece um conjunto de endpoints RESTful para que as aplicações front-end (painel de administração, app do cuidador e monitor da TV) possam interagir com o sistema.

##  Funcionalidades Principais

* **Autenticação de Usuários:** Sistema de login seguro baseado em Tokens JWT.
* **Gerenciamento Completo (CRUD):** Endpoints para criar, ler, atualizar e deletar dados de Idosos, Responsáveis, Usuários (cuidadores/admins), Medicamentos e Prescrições.
* **Lógica de Monitoramento:** Um endpoint (`GET /monitor`) que fornece dados em tempo real sobre as prescrições pendentes, já classificadas por urgência.
* **Rastreamento de Ações:** Endpoint para registrar a administração de medicamentos, vinculando a ação a um usuário e a uma prescrição específica.
* **Documentação Interativa:** Geração automática de documentação interativa com Swagger UI.

##  Tecnologias Utilizadas

* **Framework:** FastAPI
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy com Alembic para migrações
* **Validação de Dados:** Pydantic
* **Autenticação:** JWT (JSON Web Tokens) e Passlib para hashing de senhas
* **Servidor ASGI:** Uvicorn

