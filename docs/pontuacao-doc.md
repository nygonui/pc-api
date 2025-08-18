# Documentação da API - Pontuação

Endpoints para exibir os rankings de desempenho das unidades e membros, e para permitir o lançamento de pontos bônus.

## 1. Ranking

Endpoints para buscar os dados de pontuação e exibir nos rankings. **Todos os endpoints de ranking agora aceitam os parâmetros `ano` e `semestre` para filtrar os resultados.**

* **`GET /ranking/unidades`**
    * **Descrição:** Retorna a pontuação total de cada unidade para o ranking geral, filtrada por ano e semestre.
    * **Uso:** Alimenta o card "Ranking Geral das Unidades" na aba "Ranking e Pontuação".
    * **Query Params (Opcionais):** `?ano=2025&semestre=1`
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "unidade": "Jaguar",
            "pontos": 250
          },
          {
            "unidade": "Gato do Mato",
            "pontos": 210
          }
        ]
        ```

* **`GET /ranking/unidades/categorias`**
    * **Descrição:** Retorna a pontuação de cada unidade, detalhada por cada categoria de pontuação, filtrada por ano e semestre.
    * **Uso:** Alimenta o card "Ranking de Unidades por Categoria".
    * **Query Params (Opcionais):** `?ano=2025&semestre=1`
    * **Resposta (Exemplo):**
        ```json
        {
          "presenca": [
            { "unidade": "Gato do Mato", "pontos": 19 },
            { "unidade": "Jaguar", "pontos": 18 }
          ],
          "pontualidade": [
            { "unidade": "Jaguar", "pontos": 20 },
            { "unidade": "Gato do Mato", "pontos": 18 }
          ]
        }
        ```

* **`GET /ranking/membros`**
    * **Descrição:** Retorna a pontuação detalhada de cada membro para a tabela de ranking individual, filtrada por ano, semestre e, opcionalmente, por cargo.
    * **Query Params (Opcionais):** `?ano=2025&semestre=1&cargo=Desbravador`
    * **Uso:** Alimenta a tabela "Ranking Individual de Membros".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "nome": "João Silva",
            "unidade": "Jaguar",
            "cargo": "Desbravador",
            "presenca": 10,
            "pontualidade": 10,
            "uniforme": 5,
            "modestia": 10,
            "bonus": 5,
            "total": 40
          }
        ]
        ```

## 2. Bônus

Endpoint para adicionar pontos de bônus.

* **`POST /pontuacao/bonus`**
    * **Descrição:** Lança um ponto bônus para uma unidade ou um membro específico.
    * **Uso:** Formulário na aba "Lançar Bônus".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "tipo": "unidade",
          "id": 1,
          "pontos": 50,
          "descricao": "Decoração da sala da unidade."
        }
        ```