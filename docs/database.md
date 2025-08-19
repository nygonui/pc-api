# Gerenciamento de Sessões de Banco de Dados

Este documento detalha como as conexões e sessões de banco de dados são gerenciadas dentro da aplicação, focando nas classes `DatabaseAdapter` e `SessionAdapter`, e sua integração com o FastAPI.

## Configuração

Os parâmetros de conexão do banco de dados são definidos em `app/infra/database/config.py`. A classe `ConnectionConfig` contém detalhes como host, usuário, senha, nome do banco de dados e porta. A classe `PoolConfig` configura as definições do pool de conexões, incluindo tamanho, estouro máximo (`max_overflow`) e tempo de reciclagem (`recycle`).

```python
#pc-api/app/infra/database/config.py#L9-28
class PoolConfig(BaseModel):
    size: int = 10
    max_overflow: int = 5
    recycle: int = 3600


class ConnectionConfig(BaseModel):
    host: str
    user: str
    password: str
    name: str
    port: int = 5432
    pool: PoolConfig = Field(default_factory=PoolConfig)


@dataclass
class DatabaseConfig:
    connection: ConnectionConfig

    @lazymethod
    def make_uri(self, *, is_asyncio: bool) -> URL:
        """Create a database URI."""
        scheme = "postgresql+asyncpg" if is_asyncio else "postgresql+psycopg"
        return URL.from_args(
            netloc_obj=Netloc.from_args(
                host=self.connection.host,
                port=self.connection.port,
                username=self.connection.user,
                password=self.connection.password,
            ),
            scheme=scheme,
            path=self.connection.name,
        )
```

A classe `DatabaseConfig` utiliza o método `make_uri` para construir a URI do banco de dados, suportando drivers síncronos e assíncronos.

## Adaptador de Banco de Dados

O `DatabaseAdapter` (definido em `app/infra/database/adapter.py`) é responsável por gerenciar o `AsyncEngine` do SQLAlchemy, que é o ponto de entrada para todas as operações de banco de dados.

```python
#pc-api/app/infra/database/adapter.py#L14-26
@dataclass
class DatabaseAdapter:
    config: DatabaseConfig
    debug: bool = False

    @lazyfield
    def engine(self) -> sa_async.AsyncEngine:
        return sa_async.create_async_engine(
            self.config.make_uri(is_asyncio=True).encode(),
            pool_size=self.config.connection.pool.size,
            echo=self.debug,
            pool_recycle=self.config.connection.pool.recycle,
            max_overflow=self.config.connection.pool.max_overflow,
        )
```

Os principais métodos em `DatabaseAdapter` incluem:

*   `engine`: Uma propriedade de carregamento "lazy" que cria o `AsyncEngine` do SQLAlchemy usando a URI do banco de dados e as configurações do pool.
*   `new()`: Estabelece uma nova conexão assíncrona (`AsyncConnection`) a partir do engine.
*   `release()`: Fecha uma `AsyncConnection`.
*   `aclose()`: Descarta o engine do banco de dados, fechando todas as conexões no pool.
*   `begin()`, `commit()`, `rollback()`: Métodos para gerenciar transações no nível da conexão.

## Adaptador de Sessão

O `SessionAdapter` (também em `app/infra/database/adapter.py`) se baseia no `DatabaseAdapter` para fornecer uma sessão assíncrona (`AsyncSession`) para operações ORM (Object-Relational Mapping). Esta é a interface principal para interagir com o banco de dados usando os recursos ORM do SQLAlchemy.

```python
#pc-api/app/infra/database/adapter.py#L86-101
@dataclass
class SessionAdapter:
    """
    Session adapter for SQLAlchemy.
    """

    provider: DatabaseAdapter
    debug: bool = False

    async def new(self) -> sa_async.AsyncSession:
        """
        Create a new session.
        """
        return sa_async.AsyncSession(bind=await self.provider.new())
```

Os principais métodos em `SessionAdapter` incluem:

*   `new()`: Cria uma nova `AsyncSession` vinculada a uma `AsyncConnection` obtida do `DatabaseAdapter`.
*   `release()`: Libera a conexão subjacente associada à sessão.
*   `aclose()`: Fecha o engine de banco de dados subjacente através do `DatabaseAdapter`.
*   `begin()`, `commit()`, `rollback()`: Métodos para gerenciar transações no nível da sessão.

## Entidades ORM

A base para todas as entidades ORM é definida em `app/infra/database/entity.py`. Esta classe e seus mixins fornecem funcionalidades essenciais para mapear objetos Python para tabelas de banco de dados.

### Classe Base `Entity`

A classe `Entity` é a base para todos os modelos ORM. Ela estende `DeclarativeBase` do SQLAlchemy e define o comportamento padrão para suas entidades.

```python
#pc-api/app/infra/database/entity.py#L31-56
class Entity(DeclarativeBase):
    """Base class for all ORM entities, using shared metadata."""

    type_annotation_map: ClassVar[dict[Any, Any]] = {
        str: sa.String(255),
        Text: sa.Text(),
        datetime: sa.TIMESTAMP(timezone=True),
        TypeID: GUID(),
    }

    metadata: ClassVar[sa.MetaData] = metadata

    @declared_attr.directive
    def __tablename__(cls):
        # Automatically generate __tablename__ from class name
        return cls.__name__.lower().removesuffix("entity")

    id_: Mapped[TypeID] = mapped_column("id", primary_key=True, nullable=False)
```

*   **`type_annotation_map`**: Mapeia tipos Python para tipos de coluna SQLAlchemy, permitindo a definição concisa de colunas. Por exemplo, `Text` é mapeado para `sa.Text()`, e `TypeID` (um tipo customizado para identificadores únicos) é mapeado para `GUID()`.
*   **`metadata`**: Compartilha metadados entre todas as entidades, o que é crucial para operações como criação de tabelas.
*   **`__tablename__`**: Gerado automaticamente a partir do nome da classe, removendo o sufixo "entity" e convertendo para minúsculas (ex: `CarsEntity` se torna `cars`).
*   **`id_`**: Define uma coluna `id` como chave primária, utilizando o tipo `TypeID` para identificadores globalmente únicos.

### Mixin `TimestampMixin`

O `TimestampMixin` adiciona campos de timestamp comuns para controle de auditoria nas entidades.

```python
#pc-api/app/infra/database/entity.py#L59-66
class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(default=timezone.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=timezone.now,
        onupdate=timezone.now,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
```

*   **`created_at`**: Registra o momento da criação do registro.
*   **`updated_at`**: Atualizado automaticamente a cada modificação do registro.
*   **`deleted_at`**: Usado para "soft-delete", registrando o momento em que um registro foi marcado como excluído, em vez de ser removido fisicamente.

### Tipo Customizado `GUID`

O tipo `GUID` permite o uso de `TypeID` (identificadores únicos) como chaves primárias ou outros campos de identificação no banco de dados.

```python
#pc-api/app/infra/database/entity.py#L14-29
@final
class GUID(sa.types.TypeDecorator[TypeID]):
    """Custom GUID type for SQLAlchemy."""

    impl = sa.String(36)
    cache_ok = True

    @override
    def process_bind_param(
        self, value: TypeID | str | None, dialect: sa.engine.Dialect
    ) -> str | None:
        if value is None:
            return None
        return str(value)

    @override
    def process_result_value(
        self, value: str | None, dialect: sa.engine.Dialect
    ) -> TypeID | None:
        if value is None:
            return None
        return TypeID.from_string(value)
```

Ele lida com a conversão de `TypeID` para `str` ao salvar no banco e de `str` para `TypeID` ao recuperar.

## Definindo Entidades: Melhores Práticas

Ao definir suas entidades, você deve herdar de `Entity` e, se necessário, de `TimestampMixin` para incluir os campos de timestamp.

Considere o exemplo em `app/meetings/entities.py`:

```python
#pc-api/app/meetings/entities.py#L4-8
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database.entity import Entity, TimestampMixin


class CarsEntity(Entity, TimestampMixin):
    brand: Mapped[str] = mapped_column(sa.Text, nullable=False)
    model: Mapped[str] = mapped_column(sa.Text, nullable=False)
    year: Mapped[int] = mapped_column(sa.SmallInteger, nullable=False)
```

Neste exemplo:

*   `CarsEntity` herda de `Entity` (para a estrutura básica da tabela e `id_`) e `TimestampMixin` (para `created_at`, `updated_at`, `deleted_at`).
*   As colunas `brand`, `model` e `year` são definidas usando `Mapped` e `mapped_column`, especificando o tipo SQLAlchemy (ex: `sa.Text`, `sa.SmallInteger`) e propriedades como `nullable`.

## Integração com FastAPI

A aplicação integra o gerenciamento de sessões de banco de dados com o FastAPI através de injeção de dependência.

*   `create_session_adapter`: Uma função assíncrona que cria e retorna uma nova `AsyncSession`. Esta função é destinada a ser usada como uma dependência em "route handlers" do FastAPI para fornecer uma sessão de banco de dados por requisição.

```python
#pc-api/app/infra/database/adapter.py#L162-168
async def create_session_adapter(
    provider: DatabaseAdapter,
) -> sa_async.AsyncSession:
    """
    Create a session adapter.
    """
    return await SessionAdapter(provider).new()
```

*   `get_session_adapter`: Recupera a instância de `DatabaseAdapter` armazenada no estado da aplicação FastAPI. Este adaptador tipicamente serve como um singleton durante todo o ciclo de vida da aplicação.

```python
#pc-api/app/infra/database/adapter.py#L170-176
def get_session_adapter(request: Request) -> DatabaseAdapter:
    """
    Get the session adapter.
    """
    return request.app.state.session_adapter
```

### Como usar no FastAPI:

Você pode injetar um `AsyncSession` em seus "route handlers" ou outras dependências usando `Depends`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infra.database.adapter import create_session_adapter
from app.meetings.entities import CarsEntity # Importe sua entidade

router = APIRouter()

@router.get("/cars/")
async def read_cars(db_session: AsyncSession = Depends(create_session_adapter)):
    # Exemplo de uso da sessão para operações ORM
    # Equivalente ao que você faria em um caso de uso (use case)
    cars = await db_session.execute(select(CarsEntity))
    return {"message": "Carros encontrados com sucesso", "data": cars.scalars().all()}
```

Este setup garante que cada requisição obtenha sua própria sessão de banco de dados, que é gerenciada adequadamente (criada e fechada) pelo sistema de dependências do FastAPI.

### Exemplo de Uso em Casos de Uso (Domain)

No seu código de domínio, como visto em `app/meetings/domain.py`, você injeta a `AsyncSession` para realizar operações de banco de dados.

```python
#pc-api/app/meetings/domain.py#L9-20
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text

from app.api.schemas import BaseResponseSchema

from .schemas import Meeting


@dataclass
class GetMeetingsUseCase:
    database_session: AsyncSession

    async def execute(self) -> BaseResponseSchema:
        result = await self.database_session.execute(
            text("select 'hello world'")
        )
        return BaseResponseSchema(
            status=200,
            message="Meetings fetched successfully",
            data=result.scalars().all(),
        )
```

Neste exemplo, o `GetMeetingsUseCase` recebe uma `AsyncSession` e a utiliza para executar uma consulta. Para operações ORM, você substituiria o `text("select 'hello world'")` por consultas usando as entidades ORM definidas, como:

```python
from sqlalchemy import select
# ...
class GetCarsUseCase:
    database_session: AsyncSession

    async def execute(self) -> BaseResponseSchema:
        # Exemplo de consulta ORM para CarsEntity
        cars = await self.database_session.execute(select(CarsEntity))
        return BaseResponseSchema(
            status=200,
            message="Carros recuperados com sucesso",
            data=cars.scalars().all(),
        )
```

Essa abordagem separa a lógica de negócio da gestão da sessão, mantendo o código limpo e testável.
