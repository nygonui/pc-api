# Bem-vindo à Documentação da API Pioneiros da Colina

Esta documentação detalha a API do projeto Pioneiros da Colina, uma solução robusta e eficiente para o gerenciamento de desbravadores. Desenvolvida com foco em performance, segurança e manutenibilidade, esta API serve como o backbone para todas as operações relacionadas aos dados dos desbravadores.

## Visão Geral do Projeto

O `pc-api` é uma API RESTful construída em Python, utilizando o framework FastAPI. Ele foi projetado para ser rápido, fácil de usar e com documentação automática, o que facilita tanto o desenvolvimento quanto o consumo por outras aplicações.

### Propósito

O principal objetivo desta API é fornecer um conjunto de funcionalidades essenciais para:
*   Gerenciamento de informações de desbravadores e convidados.
*   Controle de reuniões e eventos.
*   Integração com outros sistemas para otimizar a gestão.

### Tecnologias Utilizadas

A API `pc-api` é construída sobre uma base tecnológica moderna e performática:

*   **FastAPI**: Um framework web de alta performance para construir APIs com Python 3.7+ (utilizando tipagem padrão do Python). Oferece validação de dados automática, serialização e documentação interativa (Swagger UI e ReDoc) "out-of-the-box".
*   **Uvicorn**: Um servidor ASGI (Asynchronous Server Gateway Interface) ultrarrápido, otimizado para servir aplicações assíncronas como o FastAPI em ambientes de produção e desenvolvimento.
*   **python-decouple**: Uma biblioteca simples e eficaz para gerenciar configurações e variáveis de ambiente, garantindo que informações sensíveis sejam separadas do código-fonte e facilitando a configuração em diferentes ambientes (desenvolvimento, produção).
*   **secure**: Um middleware de segurança que adiciona automaticamente cabeçalhos de segurança HTTP importantes às respostas da aplicação. Isso ajuda a proteger a API contra vulnerabilidades comuns da web, como ataques de clickjacking, injeção de scripts e outros.
*   **ORJSON**: Uma biblioteca JSON de alta performance para Python, utilizada para serialização e deserialização de dados. Sua velocidade contribui significativamente para a performance geral da API.

## Configuração e Execução

Para configurar e executar o projeto localmente, siga os passos descritos no [README.md](../README.md). As configurações são gerenciadas através de um arquivo `.env`, permitindo flexibilidade para diferentes ambientes.

### Variáveis de Ambiente Essenciais:
*   `LOCAL`: Define o modo de execução (`True` para desenvolvimento com documentação interativa e recarregamento automático, `False` para produção).
*   `LOG_LEVEL`: Nível mínimo de log (`debug`, `info`, `warning`, `error`, `critical`).
*   `SERVER_HOST`: Host onde a API será acessível (ex: `0.0.0.0`).
*   `SERVER_PORT`: Porta em que a API irá escutar as requisições (ex: `8000`).

## Endpoints da API

A API oferece diversos endpoints para interagir com o sistema. A documentação interativa (Swagger UI) está disponível em `/docs` quando a API está em modo `LOCAL=True`.

### Exemplo de Endpoint: Health Check
*   **GET** `/health`
*   **Descrição**: Utilizado para verificar a saúde e o status de funcionamento da aplicação.
*   **Resposta de Sucesso**:
    ```json
    {
      "status": "ok"
    }
    ```

## Tratamento de Erros

A API implementa um tratamento de erros padronizado para garantir respostas consistentes e informativas. Todos os erros são retornados em formato JSON, utilizando a classe `APIError`.

### Estrutura de Erro Padrão:
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

### Códigos de Status HTTP Comuns:
*   `400 Bad Request`: Requisição inválida.
*   `401 Unauthorized`: Autenticação necessária ou inválida.
*   `403 Forbidden`: Acesso negado.
*   `404 Not Found`: Recurso não encontrado.
*   `409 Conflict`: Conflito com o estado atual do recurso.
*   `500 Internal Server Error`: Erro inesperado no servidor.

## Segurança

A segurança é uma prioridade no `pc-api`. Um middleware de segurança (`secure`) é configurado para adicionar automaticamente cabeçalhos HTTP cruciais, protegendo a aplicação contra diversas vulnerabilidades web.

### Cabeçalhos de Segurança Incluídos:
*   `X-Content-Type-Options`: Previne ataques de "MIME-sniffing".
*   `X-Frame-Options`: Impede que a página seja incorporada em `<iframe>` ou `frame`.
*   `Strict-Transport-Security`: Força o uso de HTTPS.
*   Outros cabeçalhos relacionados a políticas de segurança de conteúdo (CSP) podem ser configurados para maior proteção.

## Estrutura do Projeto

A organização do projeto segue uma estrutura modular para facilitar a manutenção e escalabilidade:

```
pc-api/
├── app/
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── settings.py          # Configurações da aplicação
│   ├── api/
│   │   ├── routes.py        # Rotas da API
│   │   ├── schemas.py       # Schemas Pydantic para validação de dados
│   │   ├── secure.py        # Middleware de segurança
│   │   └── exc/             # Módulo de tratamento de exceções
│   │       ├── exceptions.py # Definição de exceções customizadas
│   │       └── handler.py    # Handlers para exceções da API
│   ├── meetings/            # Módulo para funcionalidades de reuniões
│   │   ├── domain.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── guests/              # Módulo para funcionalidades de convidados
│       ├── domain.py
│       ├── routes.py
│       ├── schemas.py
│       ├── entities.py
│       ├── repository.py
│       ├── concepts.py
│       └── api.py
├── .env.example             # Exemplo de variáveis de ambiente
├── pyproject.toml          # Configurações do projeto e dependências
├── uv.lock                 # Lock file das dependências
└── README.md               # Visão geral do projeto
```

## Desenvolvimento e Testes

O projeto utiliza `uv` para gerenciamento de pacotes, `pytest` para testes unitários e de integração, e `ruff` para garantir a qualidade do código através de linting e formatação.

Para mais detalhes sobre como executar testes e ferramentas de qualidade de código, consulte o [README.md](../README.md).
