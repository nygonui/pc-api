# Documentação da API - Patrimônio

Endpoints para o gerenciamento completo do inventário de materiais do clube, incluindo o registro de itens, a solicitação por parte das unidades e a aprovação e controle por parte da diretoria.

## 1. Gerenciar Patrimônio (Inventário)

Endpoints para a diretoria visualizar, adicionar, editar e remover itens do inventário do clube.

* **`GET /patrimonio`**
    * **Descrição:** Retorna a lista completa de todos os itens do inventário.
    * **Uso:** Alimenta a tabela na aba "Gerenciar Patrimônio" e a lista de itens disponíveis na aba "Solicitar Materiais".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "id": 1,
            "nome": "Barraca Iglú 4 Pessoas",
            "quantidade": 5,
            "descricao": "Modelo Mor",
            "data_aquisicao": "2023-03-15"
          }
        ]
        ```

* **`POST /patrimonio`**
    * **Descrição:** Adiciona um novo item ao inventário do clube.
    * **Uso:** Formulário "Adicionar Item ao Patrimônio" na aba "Gerenciar Patrimônio".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "nome": "Lanterna de LED",
          "quantidade": 10,
          "descricao": "Modelo recarregável com bateria",
          "data_aquisicao": "2025-08-17"
        }
        ```

* **`PUT /patrimonio/{id}`**
    * **Descrição:** Atualiza as informações de um item existente no inventário.
    * **Uso:** Botão "Editar" na tabela de itens.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "nome": "Barraca Iglú para 4 Pessoas (Nova)",
          "quantidade": 6,
          "descricao": "Modelo Mor, revisada em 2025"
        }
        ```

* **`DELETE /patrimonio/{id}`**
    * **Descrição:** Remove um item do inventário.
    * **Uso:** Botão "Remover" na tabela de itens.

## 2. Solicitação de Materiais (Visão da Unidade)

Endpoints para as unidades do clube solicitarem materiais para suas reuniões e atividades.

* **`POST /solicitacoes`**
    * **Descrição:** Cria uma nova solicitação de materiais para uma reunião específica.
    * **Uso:** Botão "Salvar Solicitações" na aba "Solicitar Materiais".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "reuniaoId": 3,
          "itens": [
            { "itemId": 1, "quantidade": 4 },
            { "itemId": 2, "quantidade": 1 }
          ]
        }
        ```

* **`GET /solicitacoes/minhas`**
    * **Descrição:** Retorna o histórico de solicitações feitas pela unidade do usuário logado, incluindo o status e o motivo de reprovação.
    * **Uso:** Card "Minhas Solicitações" na aba "Solicitar Materiais".
    * **Resposta (Exemplo):**
        ```json
        [
            {
                "id": 102,
                "reuniao": "Acampamento de Unidade",
                "data": "2025-03-15",
                "status": "reprovado",
                "motivoReprovacao": "Quantidade de barracas indisponível para a data.",
                "itens": [
                    { "nome": "Barraca Iglú 4 Pessoas", "quantidade": 4 },
                    { "nome": "Corda de Sisal 10mm", "quantidade": 1 }
                ]
            }
        ]
        ```

## 3. Gerenciamento de Solicitações (Visão da Diretoria)

Endpoints para a diretoria do clube aprovar, reprovar e gerenciar o fluxo de entrega e devolução dos materiais solicitados.

* **`GET /solicitacoes`**
    * **Descrição:** Retorna todas as solicitações de materiais de todas as unidades, agrupadas por reunião.
    * **Uso:** Alimenta a aba "Solicitações de Materiais".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "reuniao": {
              "id": 1,
              "nome": "Acampamento de Unidade",
              "data": "2025-03-15"
            },
            "solicitacoes": [
              {
                "id": 1,
                "unidade": "Jaguar",
                "status": "pendente",
                "itens": [{ "nome": "Barraca Iglú 4 Pessoas", "quantidade": 2 }]
              }
            ]
          }
        ]
        ```
* **`PUT /solicitacoes/{id}/status`**
    * **Descrição:** Atualiza o status de uma solicitação específica (Aprovar, Reprovar, Marcar como Entregue, etc.).
    * **Uso:** Botões de ação na aba "Solicitações de Materiais".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "status": "reprovado",
          "motivoReprovacao": "Item indisponível na data solicitada."
        }
        ```