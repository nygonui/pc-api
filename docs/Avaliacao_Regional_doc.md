# Documentação da API - Avaliação Regional

Endpoints destinados à liderança regional para avaliar e aprovar o progresso dos membros em classes e especialidades, garantindo a conformidade com os padrões estabelecidos.

## 1. Avaliação de Classes

Endpoints para visualizar e avaliar os requisitos de classes enviados pelos clubes.

* **`GET /avaliacoes/classes?unidade_id=<ID_UNIDADE>`**
    * **Descrição:** Retorna todos os requisitos de classe que estão aguardando avaliação ou que foram marcados para refazer, para uma unidade específica.
    * **Query Params (Obrigatório):** `?unidade_id=int`
    * **Uso:** Alimenta a aba "Classes" após a seleção de uma unidade.
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "membro": {
              "codigo_sgc": "12345",
              "nome": "João Silva"
            },
            "requisitos": [
              {
                "id_avaliacao": 12,
                "id_requisito": 102,
                "texto": "Memorizar Voto e Lei.",
                "status": "Avaliação"
              }
            ]
          }
        ]
        ```

* **`PUT /avaliacoes/requisitos/{id_avaliacao}`**
    * **Descrição:** Atualiza o status de um requisito específico para um membro (Aprovar/Refazer).
    * **Uso:** Botões "Aprovar" e "Refazer" ao lado de cada requisito na aba "Classes".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "status": "Aprovado"
        }
        ```

## 2. Avaliação de Especialidades

Endpoints para visualizar e avaliar as especialidades concluídas pelos membros.

* **`GET /avaliacoes/especialidades?unidade_id=<ID_UNIDADE>`**
    * **Descrição:** Retorna uma lista de todas as especialidades que estão aguardando avaliação ou que foram marcadas para refazer, para uma unidade específica.
    * **Query Params (Obrigatório):** `?unidade_id=int`
    * **Uso:** Alimenta a aba "Especialidades" após a seleção de uma unidade.
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "membro": {
              "codigo_sgc": "54321",
              "nome": "Maria Santos"
            },
            "especialidades": [
              {
                "id_avaliacao": 25,
                "codigo_especialidade": "PS-001",
                "nome": "Primeiros Socorros",
                "status": "Refazer"
              }
            ]
          }
        ]
        ```

* **`PUT /avaliacoes/especialidades/{id_avaliacao}`**
    * **Descrição:** Atualiza o status de uma especialidade para um membro (Aprovar/Refazer).
    * **Uso:** Botões de ação na aba "Especialidades".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "status": "Aprovado"
        }
        ```

## 3. Sentinelas da Colina

Endpoints para a aprovação final de membros que completaram todos os requisitos de uma classe ou especialidade, tornando-os "Sentinelas".

* **`GET /sentinelas?tipo=<TIPO>&codigo=<CODIGO_CLASSE/ESPECIALIDADE>`**
    * **Descrição:** Retorna uma lista de membros que estão aguardando a aprovação final para uma classe ou especialidade específica.
    * **Query Params:** `?tipo=classe|especialidade`, `&codigo=AM-001|AP-034`
    * **Uso:** Alimenta a aba "Sentinelas da Colina" ao selecionar uma classe ou especialidade no dropdown.
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "codigo_sgc": "12345",
            "nome": "João Silva",
            "status": "Avaliação"
          },
          {
            "codigo_sgc": "67890",
            "nome": "Pedro Costa",
            "status": "Refazer"
          }
        ]
        ```

* **`PUT /sentinelas/{codigo_sgc}`**
    * **Descrição:** Realiza a aprovação final (ou marca para refazer) de um membro em uma classe ou especialidade.
    * **Uso:** Botões "Aprovar" e "Refazer" na aba "Sentinelas da Colina".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "tipo": "classe",
          "codigo": "AM-001",
          "status": "Aprovado"
        }
        ```
