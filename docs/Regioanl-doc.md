# Documentação da API - Apoio Regional

Endpoints para a comunicação e gestão de recursos entre a coordenação regional e a diretoria dos clubes. A seção é dividida em duas visões: a do clube (consumo de informações) e a da regional (gerenciamento).

## 1. Visão do Clube (Informações e Recursos)

Endpoints para os membros da diretoria do clube visualizarem comunicados, datas e arquivos, além de enviarem mensagens para a regional.

* **`GET /regional/posts`**
    * **Descrição:** Retorna a lista de todos os posts e comunicados publicados pela regional.
    * **Uso:** Alimenta o card "Posts da Regional" na aba "Informações e Recursos".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "id": 1,
            "titulo": "Ajustes no Calendário de Eventos",
            "autor": "Pastor Regional",
            "data": "2025-08-10",
            "conteudo": "Atenção, diretoria! O Camporee Regional foi adiantado em uma semana."
          }
        ]
        ```

* **`GET /regional/avaliacoes`**
    * **Descrição:** Retorna a lista das próximas datas de avaliação definidas pela regional.
    * **Uso:** Alimenta o card "Datas das Avaliações".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "id": 1,
            "nome": "Avaliação de Classes Regulares",
            "data": "2025-09-15"
          }
        ]
        ```

* **`GET /regional/arquivos`**
    * **Descrição:** Retorna a lista de arquivos e manuais disponíveis para download.
    * **Uso:** Alimenta o card "Arquivos e Manuais".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "id": 1,
            "nome": "Regulamento de Uniformes 2025",
            "tipo": "PDF",
            "tamanho": "1.8MB",
            "url": "/path/to/downloadable/file.pdf"
          }
        ]
        ```

* **`POST /regional/mensagens`**
    * **Descrição:** Envia uma nova mensagem da diretoria do clube para a regional.
    * **Uso:** Formulário no card "Mensagem para a Regional".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "assunto": "Dúvida sobre o Camporee",
          "mensagem": "Gostaríamos de confirmar se o local permanece o mesmo."
        }
        ```

* **`GET /regional/mensagens/enviadas`**
    * **Descrição:** Retorna o histórico de mensagens que o clube enviou para a regional, incluindo as respostas.
    * **Uso:** Alimenta o card "Minhas Mensagens Enviadas".
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "id": 1,
            "assunto": "Dúvida sobre o Camporee",
            "mensagem": "Gostaríamos de confirmar se o local permanece o mesmo.",
            "dataEnvio": "2025-08-11",
            "resposta": {
              "autorResposta": "Pastor Regional",
              "dataResposta": "2025-08-12",
              "conteudo": "Sim, o local está confirmado! Abraços."
            }
          }
        ]
        ```

## 2. Visão da Regional (Gerenciamento)

Endpoints para a equipe regional criar, editar e gerenciar o conteúdo que será exibido para os clubes.

* **`POST /regional/gerenciar/posts`**
    * **Descrição:** Cria um novo post ou comunicado para os clubes.
    * **Uso:** Formulário no card "Criar/Editar Post".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "titulo": "Novo Regulamento de Uniformes",
          "conteudo": "O novo manual de uniformes já está disponível para download."
        }
        ```

* **`PUT /regional/gerenciar/posts/{id}`**
    * **Descrição:** Atualiza o título ou conteúdo de um post existente.
    * **Uso:** Formulário no card "Criar/Editar Post" ao selecionar um post para editar.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "titulo": "ATUALIZADO: Novo Regulamento de Uniformes",
          "conteudo": "A implementação é imediata a partir de hoje."
        }
        ```

* **`POST /regional/gerenciar/avaliacoes`**
    * **Descrição:** Adiciona uma nova data de avaliação ao calendário.
    * **Uso:** Formulário no card "Gerenciar Datas de Avaliação".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "nome": "Avaliação de Especialidades (Artes Manuais)",
          "data": "2025-09-22"
        }
        ```
* **`DELETE /regional/gerenciar/avaliacoes/{id}`**
    * **Descrição:** Remove uma data de avaliação.
    * **Uso:** Botão de remover em uma data de avaliação existente.

* **`GET /regional/gerenciar/mensagens`**
    * **Descrição:** Retorna todas as mensagens recebidas de todos os clubes.
    * **Uso:** Alimenta a "Caixa de Entrada" da regional.
    * **Resposta (Exemplo):**
        ```json
        [
          {
            "id": 1,
            "assunto": "Dúvida sobre o Camporee",
            "autor": "Maria Santos (Diretora Jaguar)",
            "data": "2025-08-11",
            "mensagem": "Olá, Pastor! Gostaríamos de confirmar se o local do Camporee permanece o mesmo."
          }
        ]
        ```

* **`POST /regional/gerenciar/mensagens/{id}/responder`**
    * **Descrição:** Envia uma resposta para uma mensagem recebida de um clube.
    * **Uso:** Campo de resposta na "Caixa de Entrada".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "resposta": "Sim, o local está confirmado! Abraços."
        }
        ```
```