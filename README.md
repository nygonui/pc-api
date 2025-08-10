# pc-api

## Descrição

Este projeto é a API do Pioneiros da Colina, desenvolvida para fornecer funcionalidades essenciais para o gerenciamento de desbravadores. Ela foi construída com foco em performance, segurança e manutenibilidade.

## Dependencias

O projeto utiliza um conjunto de dependencias modernas e eficientes para garantir alta performance e escalabilidade:

*   **FastAPI**: Um framework web de alta performance para construir APIs com Python 3.7+ (utilizando tipagem padrão do Python), que oferece excelente documentação automática (Swagger UI e ReDoc).
*   **Uvicorn**: Um servidor ASGI ultrarrápido, essencial para servir as aplicações FastAPI em produção e desenvolvimento.
*   **python-decouple**: Uma biblioteca simples para gerenciar configurações e variáveis de ambiente, promovendo a separação de configurações sensíveis do código.
*   **secure**: Um middleware para adicionar cabeçalhos de segurança HTTP importantes às respostas da aplicação, aumentando a proteção contra vulnerabilidades comuns.
*   **ORJSON**: Uma biblioteca JSON ultrarrápida para Python, oferecendo serialização e deserialização de dados com alta performance.

## Pré-requisitos

Para configurar e executar este projeto, certifique-se de ter os seguintes softwares instalados em sua máquina:

*   **Python 3.13** ou superior.
*   **UV**: Gerenciador de pacotes Python moderno e rápido.

## Instalação

Siga os passos abaixo para preparar seu ambiente de desenvolvimento e instalar as dependências necessárias:

1.  **Clone o repositório**:
    ```bash
    git clone <repository-url>
    cd pc-api
    ```

2.  **Crie e ative um ambiente virtual e instale as dependências**:
    ```bash
    uv sync
    ```

## Configuração

O projeto faz uso de variáveis de ambiente para gerenciar suas configurações. É necessário criar um arquivo `.env` na raiz do projeto, baseado no `.env.example`, e preenchê-lo com os valores apropriados para o seu ambiente.

```env
LOCAL=True
LOG_LEVEL=info
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

*   `LOCAL`: Define o modo de execução. Defina como `True` para ativar o modo de desenvolvimento (que inclui documentação interativa e recarregamento automático do servidor), ou `False` para o modo de produção.
*   `LOG_LEVEL`: Nível mínimo de log para a aplicação (opções: `debug`, `info`, `warning`, `error`, `critical`).
*   `SERVER_HOST`: O host onde a API será acessível (ex: `0.0.0.0` para acesso externo, `127.0.0.1` para acesso local).
*   `SERVER_PORT`: A porta em que a API irá escutar as requisições (ex: `8000`).

## Execução

Para iniciar o servidor da API, certifique-se de que seu ambiente virtual esteja ativado e execute o seguinte comando no terminal:

```bash
python app/main.py
```

Após a execução, a API estará disponível no endereço configurado em seu `.env`, por exemplo: `http://0.0.0.0:8000`. Se estiver no modo `LOCAL=True`, você pode acessar a documentação interativa em `/docs` (Swagger UI).

## Endpoints da API

A API oferece diversos endpoints para interagir com o sistema de gerenciamento de desbravadores. (Desenvolvimento)

### Health Check

Este endpoint é utilizado para verificar a saúde e o status de funcionamento da aplicação.

*   **GET** `/health`
*   **Resposta esperada (sucesso)**:
    ```json
    {
      "status": "ok"
    }
    ```

## Tratamento de Erros

A API implementa um tratamento de erros padronizado para garantir que as respostas de erro sejam consistentes e informativas. Todos os erros são retornados em formato JSON, utilizando a classe `APIError`.

**Estrutura de erro padrão**:

```json
{
  "message": "Mensagem de erro resumida",
  "detail": "Detalhes adicionais sobre o erro",
  "fields": [
    {
      "name": "nome_do_campo",
      "detail": "Detalhe específico do erro no campo"
    }
  ],
  "status_code": 400
}
```

**Códigos de status HTTP comuns e suas implicações**:

*   `400 Bad Request`: Indica que a requisição não pôde ser entendida ou processada devido a sintaxe inválida, validação de dados falha, ou parâmetros ausentes/incorretos.
*   `401 Unauthorized`: Ocorre quando a requisição requer autenticação, mas esta não foi fornecida, é inválida ou expirou.
*   `403 Forbidden`: A autenticação foi bem-sucedida, mas o usuário autenticado não tem permissão para acessar o recurso solicitado.
*   `404 Not Found`: O recurso solicitado não existe no servidor.
*   `409 Conflict`: A requisição não pôde ser concluída devido a um conflito com o estado atual do recurso (ex: tentativa de criar um recurso que já existe).
*   `500 Internal Server Error`: Um erro inesperado ocorreu no servidor, indicando um problema que precisa ser investigado pela equipe de desenvolvimento.

## Segurança

A aplicação FastAPI é configurada com um middleware de segurança (`secure`) que adiciona automaticamente cabeçalhos de segurança HTTP cruciais às respostas da API. Isso ajuda a mitigar uma série de vulnerabilidades comuns da web, como ataques de clickjacking, injeção de scripts e outros. Alguns dos cabeçalhos incluídos são:

*   `X-Content-Type-Options`: Previne ataques de "MIME-sniffing".
*   `X-Frame-Options`: Impede que a página seja incorporada em um `<iframe>` ou `frame`.
*   `Strict-Transport-Security`: Força o uso de HTTPS para comunicações futuras.
*   Outros cabeçalhos relacionados a políticas de segurança de conteúdo (CSP) podem ser configurados.

## Estrutura do Projeto

```
pc-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── settings.py          # Configurações da aplicação
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py        # Rotas da API
│   │   ├── schemas.py       # Schemas Pydantic
│   │   ├── secure.py        # Middleware de segurança
│   │   ├── utils.py         # Utilitários gerais
│   │   └── exc/
│   │       ├── __init__.py
│   │       ├── exceptions.py # Exceções customizadas
│   │       └── handler.py    # Handlers de exceções
│   └── tests/
│       ├── __init__.py
│       └── test_health.py   # Testes da aplicação
├── .env.example             # Exemplo de variáveis de ambiente
├── pyproject.toml          # Configurações do projeto e dependências
├── uv.lock                 # Lock file das dependências
└── README.md               # Este arquivo
```

## Desenvolvimento

### Executando os Testes

Para executar os testes da aplicação:

```bash
uv run pytest
```

### Linting e Formatação

O projeto utiliza Ruff para linting e formatação:

```bash
# Verificar problemas de código
uv run ruff check

# Formatar código
uv run ruff format
```
