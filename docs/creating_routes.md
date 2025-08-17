# Criando Novas Rotas no `pc-api`

Este documento serve como um guia passo a passo para criar novas rotas (endpoints) na API `pc-api`, seguindo a arquitetura orientada a domínio (DDD) e as melhores práticas do FastAPI.

## Pré-requisitos

Antes de começar, certifique-se de ter um entendimento básico de:

*   **Python**: Sintaxe e conceitos fundamentais.
*   **FastAPI**: Como funciona um `APIRouter`, decoradores de rota (`@app.get`, `@app.post`, etc.).
*   **Pydantic**: Criação de modelos para validação de dados.
*   **DDD**: Conceitos de Entidades, Objetos de Valor, Serviços de Domínio e Repositórios (conforme explicado em [Arquitetura DDD](domain_driven_design.md)).

## Fluxo de Criação de uma Nova Rota

A criação de uma nova rota geralmente envolve os seguintes passos, distribuídos entre as camadas da aplicação:

1.  **Identificar o Domínio**: Determine a qual domínio de negócio a nova rota pertence (ex: `meetings`, `scouts`, `users`). Se for um domínio novo, crie um novo diretório em `app/` para ele.
2.  **Definir o Modelo de Dados (Schemas)**: Crie ou atualize os modelos Pydantic em `app/<dominio>/schemas.py` para representar os dados de entrada (requisição) e saída (resposta) da sua rota.
3.  **Implementar a Lógica de Negócio (Domínio)**: No arquivo `app/<dominio>/domain.py`, implemente a lógica de negócio pura que a rota irá orquestrar. Isso pode envolver a criação de novas Entidades, Objetos de Valor, ou a implementação de um Serviço de Domínio.
4.  **Criar a Rota (API Router)**: No arquivo `app/<dominio>/routes.py`, defina o endpoint da API usando um `APIRouter`. Esta camada deve ser "fina", chamando a lógica de negócio do `domain.py`.
5.  **Incluir a Rota Principal**: No arquivo `app/api/routes.py`, inclua o `APIRouter` do seu novo domínio para que ele seja reconhecido pela aplicação principal.

## Exemplo Prático: Criando uma Rota para Gerenciar Convidados

Vamos supor que queremos adicionar funcionalidades para gerenciar convidados.

### Passo 1: Identificar o Domínio e Criar o Módulo

Como "convidados" é um novo domínio, criaremos um novo diretório:

```bash
mkdir -p app/guests
touch app/guests/__init__.py
touch app/guests/domain.py
touch app/guests/routes.py
touch app/guests/schemas.py
touch app/guests/entities.py
touch app/guests/repository.py
touch app/guests/concepts.py
touch app/guests/api.py
```

### Passo 2: Definir o Modelo de Dados (`app/guests/schemas.py`)

Vamos criar um schema para um convidado e um para a criação de um novo convidado.

```python
# app/guests/schemas.py

from datetime import datetime
from pydantic import BaseModel, field_validator

from app.guests.concepts import GuestStatus


class CreateGuestSchema(BaseModel):
    """Schema for creating a guest."""

    name: str
    email: str
    phone: str

    @field_validator("phone")
    @classmethod
    def force_only_digits(cls, value: str) -> str:
        """Ensure phone number contains only digits."""
        return "".join(filter(str.isdigit, value))


class Guest(CreateGuestSchema):
    """Schema for guest details."""

    id_: str
    invitation_code: str
    rsvp_status_first: GuestStatus
    rsvp_status_second: GuestStatus
    created_at: datetime
    updated_at: datetime
```

### Passo 3: Implementar a Lógica de Negócio (`app/guests/domain.py`)

Aqui, definiremos a entidade `Guest` e os casos de uso para operações básicas. Usaremos um repositório para persistência em banco de dados.

```python
# app/guests/domain.py

import string
from datetime import datetime

import nanoid
from typeid import TypeID

from app.api.exc.exceptions import FieldError, already_exists
from app.database import SessionContext, query
from app.guests.concepts import GuestStatus
from app.guests.repository import GuestRepository
from app.guests.schemas import CreateGuestSchema, Guest


def generate_invite_code() -> str:
    content = nanoid.generate(string.ascii_uppercase + string.digits, size=10)
    return "-".join((content[:5], content[5:]))


class CreateGuestUseCase:
    context: SessionContext
    payload: CreateGuestSchema

    @property
    def repository(self) -> GuestRepository:
        return GuestRepository(self.context)

    async def execute(self) -> Guest:
        async with self.context:
            await self._validate_guest()
            guest = Guest(
                id_=str(TypeID()),
                name=self.payload.name,
                email=self.payload.email,
                phone=self.payload.phone,
                invitation_code=generate_invite_code(),
                rsvp_status_first=GuestStatus.PENDING,
                rsvp_status_second=GuestStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            _ = await self.repository.create(guest)
            return guest

    async def _validate_guest(self):
        if await self.repository.exists(
            query.or_(
                query.Where("email", self.payload.email),
                query.Where("phone", self.payload.phone),
            )
        ):
            raise already_exists(
                "Guest",
                (
                    FieldError("email", self.payload.email),
                    FieldError("phone", self.payload.phone),
                ),
            )


class GetGuestUseCase:
    context: SessionContext
    clause: query.BindClause

    def repository(self) -> GuestRepository:
        return GuestRepository(self.context)
    
    async def execute(self) -> Guest:
        async with self.context:
            return await self.repository.get(self.clause)
```

### Passo 4: Criar a Rota (`app/guests/routes.py`)

Agora, vamos definir os endpoints da API para os convidados.

```python
# app/guests/routes.py

from fastapi import APIRouter, status

from app.database import SessionContext
from app.guests.api import GuestContext
from app.guests.domain import CreateGuestUseCase
from app.guests.schemas import CreateGuestSchema, Guest

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_guest(
    payload: CreateGuestSchema, context: SessionContext
) -> Guest:
    use_case = CreateGuestUseCase(context, payload)
    return await use_case.execute()


@router.get(
    "/me",
)
def get_my_guest(guest: GuestContext) -> Guest:
    return guest
```

### Passo 5: Incluir a Rota Principal (`app/api/routes.py`)

Finalmente, precisamos garantir que o `APIRouter` do domínio `guests` seja incluído na aplicação principal.

```python
# app/api/routes.py

from fastapi import APIRouter

from app.api.exc.handler import add_exception_handlers
from app.meetings.routes import router as meetings_router
from app.guests.routes import router as guests_router # Importe o novo router

api_router = APIRouter()

# Adiciona os handlers de exceção
add_exception_handlers(api_router)

# Inclui as rotas de cada módulo
api_router.include_router(meetings_router)
api_router.include_router(guests_router) # Inclua o novo router
```

## Considerações Adicionais

*   **Injeção de Dependência**: Para cenários mais complexos, especialmente com repositórios e serviços que dependem de outros componentes (como uma conexão de banco de dados), utilize o sistema de Injeção de Dependência do FastAPI. Isso permite que você passe instâncias de serviços ou repositórios para suas funções de rota de forma limpa e testável.
*   **Testes**: Após criar suas rotas, é fundamental escrever testes unitários e de integração para garantir que elas funcionem conforme o esperado e que a lógica de negócio esteja correta.
*   **Documentação Automática**: O FastAPI gera automaticamente a documentação interativa (Swagger UI e ReDoc) com base nos seus schemas Pydantic e nas docstrings das suas funções de rota. Certifique-se de escrever docstrings claras e descritivas.
*   **Tratamento de Erros**: Utilize as exceções customizadas (`app/api/exc/exceptions.py`) e os handlers (`app/api/exc/handler.py`) para retornar respostas de erro padronizadas e informativas.

Seguindo este guia, você poderá estender o `pc-api` com novas funcionalidades de forma organizada e consistente com a arquitetura do projeto.