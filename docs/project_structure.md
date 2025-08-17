# Estrutura do Projeto

Este documento detalha a estrutura de diretórios e arquivos do projeto `pc-api`, explicando o propósito de cada componente e como eles se encaixam para formar uma aplicação robusta e organizada. A arquitetura visa promover a modularidade, facilitar a manutenção e permitir a escalabilidade.

```
pc-api/
├── app/
│   ├── main.py              # Ponto de entrada principal da aplicação FastAPI.
│   ├── settings.py          # Gerencia as configurações da aplicação, carregando variáveis de ambiente.
│   ├── api/                 # Módulo principal para a API RESTful.
│   │   ├── routes.py        # Define as rotas globais da API e inclui rotas de outros módulos.
│   │   ├── schemas.py       # Contém os modelos Pydantic para validação de dados de entrada e saída.
│   │   ├── secure.py        # Implementa middlewares de segurança para proteção da API.
│   │   └── exc/             # Módulo para tratamento de exceções e erros.
│   │       ├── exceptions.py # Define exceções customizadas da aplicação.
│   │       └── handler.py    # Handlers para capturar e formatar respostas de erro da API.
│   └── meetings/            # Exemplo de módulo de domínio para funcionalidades de reuniões.
│       ├── domain.py        # Contém a lógica de negócio e modelos de domínio (DDD).
│       ├── routes.py        # Define as rotas específicas para o domínio de reuniões.
│       └── schemas.py       # Modelos Pydantic para o domínio de reuniões.
├── .env.example             # Arquivo de exemplo para variáveis de ambiente.
├── pyproject.toml          # Configurações do projeto, dependências e metadados (Poetry/Ruff).
├── uv.lock                 # Arquivo de lock de dependências gerado pelo `uv`.
└── README.md               # Documento principal com visão geral, configuração e execução do projeto.
```

## Detalhamento dos Módulos Principais

### `app/`
Este é o diretório raiz do código-fonte da aplicação.

*   **`main.py`**: É o coração da aplicação FastAPI. Aqui, a instância principal do FastAPI é criada, middlewares são aplicados (como o de segurança e tratamento de erros) e as rotas definidas em `app/api/routes.py` são incluídas. É o arquivo que o servidor Uvicorn executa para iniciar a API.

*   **`settings.py`**: Responsável por carregar e gerenciar as configurações da aplicação. Utiliza `python-decouple` para ler variáveis de ambiente (`.env`) de forma segura e organizada. Isso garante que configurações sensíveis (como chaves de API ou credenciais de banco de dados) não sejam hardcoded e possam ser facilmente alteradas entre ambientes (desenvolvimento, produção).

### `app/api/`
Este módulo agrupa os componentes centrais da API que não são específicos de um domínio de negócio, mas são fundamentais para o funcionamento geral.

*   **`routes.py`**: Atua como um agregador de rotas. Ele importa e inclui os `APIRouter` de outros módulos de domínio (como `meetings/routes.py`), centralizando a definição de todos os endpoints da API. Isso mantém o `main.py` limpo e focado na inicialização da aplicação.

*   **`schemas.py`**: Contém os modelos de dados Pydantic que definem a estrutura esperada para as requisições (payloads de entrada) e as respostas (dados de saída) da API. Pydantic oferece validação automática de dados, serialização e deserialização, garantindo que os dados estejam sempre no formato correto.

*   **`secure.py`**: Configura e aplica o middleware de segurança (`secure`). Este middleware adiciona cabeçalhos HTTP de segurança importantes às respostas da API, protegendo contra vulnerabilidades comuns como XSS, CSRF, clickjacking, e forçando o uso de HTTPS.

*   **`exc/`**: Dedicado ao tratamento de exceções.
    *   **`exceptions.py`**: Define classes de exceção customizadas para a aplicação (ex: `APIError`). Isso permite que a lógica de negócio levante erros específicos que podem ser capturados e tratados de forma padronizada pela API.
    *   **`handler.py`**: Contém os manipuladores de exceção que interceptam as exceções levantadas pela aplicação (incluindo as customizadas) e as transformam em respostas de erro JSON padronizadas, com mensagens claras e códigos de status HTTP apropriados.

### `app/meetings/` (Módulo de Domínio)
Este é um exemplo de como um domínio de negócio específico (neste caso, "reuniões") é estruturado dentro da arquitetura. Cada domínio deve ter sua própria pasta com componentes relacionados.

*   **`domain.py`**: Este é o coração do domínio. Contém a lógica de negócio pura, as entidades de domínio, agregados e, possivelmente, interfaces para repositórios. É onde as regras de negócio são implementadas, independentemente da camada de apresentação (API) ou de persistência (banco de dados).

*   **`routes.py`**: Define os endpoints da API específicos para o domínio de reuniões. Utiliza um `APIRouter` do FastAPI para agrupar todas as rotas relacionadas a reuniões (ex: criar reunião, listar reuniões, atualizar reunião). Essas rotas interagem com a lógica definida em `domain.py`.

*   **`schemas.py`**: Contém os modelos Pydantic específicos para o domínio de reuniões, usados para validar dados de entrada e saída relacionados a este domínio.

## Outros Arquivos Importantes

*   **`.env.example`**: Um modelo para o arquivo `.env`, que lista as variáveis de ambiente necessárias para configurar e executar a aplicação. Os desenvolvedores devem copiar este arquivo para `.env` e preencher com seus valores.

*   **`pyproject.toml`**: O arquivo de configuração principal do projeto. Gerenciado pelo Poetry, ele define as dependências do projeto, metadados, e configurações para ferramentas como `ruff` (linting e formatação) e `pytest` (testes).

*   **`uv.lock`**: Gerado pelo gerenciador de pacotes `uv`, este arquivo "trava" as versões exatas de todas as dependências do projeto, garantindo que todos os desenvolvedores e ambientes de produção utilizem as mesmas versões de pacotes, evitando problemas de compatibilidade.

*   **`README.md`**: O ponto de partida para qualquer pessoa que queira entender, configurar ou contribuir para o projeto. Contém informações essenciais sobre a visão geral, instalação, execução, testes e outras instruções importantes.