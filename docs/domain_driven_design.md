# Arquitetura Orientada a Domínio (DDD) no `pc-api`

Este documento explica como os princípios da Arquitetura Orientada a Domínio (Domain-Driven Design - DDD) são aplicados no projeto `pc-api`. O DDD é uma abordagem de desenvolvimento de software que foca na modelagem do software para refletir um domínio de negócio complexo, facilitando a comunicação entre especialistas de domínio e desenvolvedores.

## Conceitos Fundamentais do DDD

Antes de mergulharmos na implementação, é importante entender alguns conceitos chave do DDD:

*   **Domínio**: O assunto principal da aplicação, a área de conhecimento à qual a lógica de negócio se refere (ex: gerenciamento de convidados, reuniões).
*   **Modelo de Domínio**: Uma representação abstrata do domínio, focando nos conceitos, regras e comportamentos essenciais.
*   **Linguagem Ubíqua**: Uma linguagem comum e consistente usada por todos os membros da equipe (desenvolvedores, especialistas de domínio) para descrever o domínio. Isso evita ambiguidades e garante que todos estejam na mesma página.
*   **Entidades**: Objetos que possuem uma identidade única e contínua ao longo do tempo, mesmo que seus atributos mudem (ex: um `Convidado` com um ID único).
*   **Objetos de Valor**: Objetos que são definidos por seus atributos e não possuem uma identidade única. Eles são imutáveis e são comparados por seus valores (ex: um `Endereco` com rua, cidade, CEP).
*   **Agregados**: Um cluster de Entidades e Objetos de Valor que são tratados como uma única unidade transacional. Um Agregado tem uma raiz (Root) que é a única Entidade que pode ser acessada diretamente de fora do Agregado (ex: `Convidado` como raiz, contendo `RSVP` como Objeto de Valor).
*   **Serviços de Domínio**: Operações que não se encaixam naturalmente em uma Entidade ou Objeto de Valor, geralmente envolvendo múltiplas Entidades ou Agregados (ex: `RegistrarRSVP`).
*   **Repositórios**: Abstrações que fornecem uma forma de acessar e persistir Agregados. Eles isolam a lógica de persistência do modelo de domínio, permitindo que o domínio seja independente da tecnologia de banco de dados.
*   **Contextos Delimitados (Bounded Contexts)**: Uma fronteira explícita dentro da qual um modelo de domínio específico é definido e aplicável. Diferentes contextos delimitados podem ter modelos de domínio diferentes para o mesmo conceito, se o significado desse conceito variar entre os contextos.

## Aplicação do DDD no `pc-api`

O `pc-api` adota uma estrutura que reflete os princípios do DDD, organizando o código em módulos de domínio.

### Estrutura de Módulos de Domínio

Cada domínio de negócio (ex: `meetings`, `guests`, etc.) é encapsulado em seu próprio diretório dentro de `app/`. Por exemplo, o módulo `app/meetings/` é dedicado a todas as funcionalidades relacionadas a reuniões, e `app/guests/` para convidados.

```
app/
├── meetings/
│   ├── domain.py        # Lógica de negócio, entidades, objetos de valor, serviços de domínio.
│   ├── routes.py        # Camada de apresentação (FastAPI) para o domínio de reuniões.
│   └── schemas.py       # Modelos de dados (Pydantic) para o domínio de reuniões.
└── guests/
    ├── domain.py        # Lógica de negócio, entidades, objetos de valor, serviços de domínio.
    ├── routes.py        # Camada de apresentação (FastAPI) para o domínio de convidados.
    ├── schemas.py       # Modelos de dados (Pydantic) para o domínio de convidados.
    ├── entities.py      # Mapeamento de entidades para o banco de dados (SQLAlchemy).
    ├── repository.py    # Implementação do repositório para persistência de convidados.
    ├── concepts.py      # Definição de conceitos específicos do domínio (ex: enums).
    └── api.py           # Funções auxiliares para a camada de API (ex: injeção de dependência).
```

### Detalhamento dos Componentes DDD

*   **`domain.py`**:
    *   Este arquivo é o coração do Contexto Delimitado de "Reuniões" ou "Convidados".
    *   Contém as **Entidades** (ex: `Reuniao`, `Convidado`), **Objetos de Valor** (ex: `Periodo`, `Localizacao`, `GuestStatus`) e **Serviços de Domínio** (funções que orquestram a lógica de negócio complexa que envolve múltiplas entidades, como `CreateGuestUseCase`).
    *   A lógica de negócio é implementada aqui, de forma agnóstica à infraestrutura (banco de dados, API). Isso significa que as regras de negócio podem ser testadas isoladamente e são reutilizáveis.
    *   Pode conter interfaces (classes abstratas) para **Repositórios**, que seriam implementadas na camada de infraestrutura (como `repository.py` para `GuestRepository`).

*   **`routes.py`**:
    *   Representa a **Camada de Aplicação/Apresentação** para o domínio de reuniões ou convidados.
    *   Define os endpoints da API usando `FastAPI.APIRouter`.
    *   As rotas recebem as requisições HTTP, validam os dados de entrada usando os `schemas.py` e orquestram a chamada aos **Serviços de Domínio** (como `CreateGuestUseCase`) ou diretamente às **Entidades** para executar a lógica de negócio.
    *   É crucial que esta camada seja "fina", ou seja, que contenha o mínimo de lógica de negócio possível, delegando a maior parte do trabalho ao `domain.py`.

*   **`schemas.py`**:
    *   Contém os modelos Pydantic que servem como **DTOs (Data Transfer Objects)** para o domínio.
    *   Definem a estrutura dos dados que entram e saem da API, garantindo a validação e serialização/deserialização.
    *   Estes schemas são a "ponte" entre a camada de apresentação (API) e o modelo de domínio, traduzindo os dados do formato da requisição/resposta para o formato que o domínio entende e vice-versa (ex: `CreateGuestSchema`, `Guest`).

*   **`entities.py`**:
    *   Este arquivo é responsável pelo mapeamento das **Entidades** do domínio para o banco de dados, utilizando uma ORM como o SQLAlchemy.
    *   Define a estrutura da tabela no banco de dados e como os atributos da entidade se relacionam com as colunas da tabela.
    *   É parte da **Camada de Infraestrutura**, pois lida com detalhes de persistência.

*   **`repository.py`**:
    *   Contém a implementação concreta dos **Repositórios** definidos (ou implicitamente usados) na camada de domínio.
    *   É responsável por toda a lógica de persistência, como salvar, buscar, atualizar e deletar entidades no banco de dados.
    *   Traduz os objetos do domínio para o formato que o banco de dados entende (e vice-versa), utilizando as entidades definidas em `entities.py`.
    *   Também faz parte da **Camada de Infraestrutura**, isolando o domínio dos detalhes de como os dados são armazenados.

*   **`concepts.py`**:
    *   Este arquivo é dedicado à definição de conceitos e tipos específicos do domínio que são reutilizados em várias partes do módulo.
    *   Pode incluir enums (como `GuestStatus`), constantes, ou classes auxiliares que representam conceitos importantes para o domínio, mas que não são entidades ou objetos de valor por si só.
    *   Ajuda a manter a **Linguagem Ubíqua** consistente dentro do contexto delimitado.

*   **`api.py`**:
    *   Este arquivo contém funções auxiliares ou dependências que são específicas para a integração do domínio com a camada de API (FastAPI).
    *   Pode incluir funções para injeção de dependência (`Depends`), como `GuestContext` que busca um convidado com base em um código de convite.
    *   Embora esteja na pasta do domínio, sua função principal é facilitar a interação entre as rotas (`routes.py`) e a lógica de domínio, atuando como uma ponte para a camada de apresentação.

## Benefícios do DDD no `pc-api`

A adoção do DDD traz várias vantagens para o projeto:

1.  **Clareza do Domínio**: O código reflete diretamente o modelo de negócio, tornando-o mais fácil de entender para novos desenvolvedores e especialistas de domínio.
2.  **Manutenibilidade**: A separação clara de responsabilidades entre as camadas (domínio, aplicação, infraestrutura) facilita a localização e correção de bugs, bem como a adição de novas funcionalidades.
3.  **Testabilidade**: A lógica de negócio no `domain.py` é isolada, permitindo testes unitários mais eficazes e rápidos, sem a necessidade de configurar um banco de dados ou servidor web.
4.  **Escalabilidade**: Novos domínios podem ser adicionados como módulos independentes, minimizando o impacto nas partes existentes da aplicação.
5.  **Flexibilidade Tecnológica**: A camada de domínio é independente da tecnologia de persistência ou do framework web, permitindo que essas tecnologias sejam alteradas no futuro com menos esforço.
6.  **Linguagem Ubíqua**: Promove uma comunicação mais eficaz entre a equipe, pois todos usam os mesmos termos e conceitos definidos no modelo de domínio.

Ao seguir esta arquitetura, o `pc-api` se torna uma aplicação mais robusta, flexível e preparada para evoluir de acordo com as necessidades do negócio.
