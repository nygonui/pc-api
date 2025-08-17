# Documentação da API - Pioneiros da Colina

Esta documentação descreve os endpoints da API necessários para alimentar o sistema de gerenciamento do clube Pioneiros da Colina.

## 1. Tesouraria

Endpoints para o gerenciamento financeiro completo do clube, incluindo fluxo de caixa, mensalidades, eventos e relatórios.

### 1.1. Visão Geral

* **`GET /tesouraria/visao-geral`**
    * **Descrição:** Retorna um resumo financeiro consolidado do mês atual, ideal para os cards de destaque.
    * **Uso:** Alimenta a aba "Visão Geral".
    * **Resposta (Exemplo):**
        ```json
        {
          "receitasMes": 2450.00,
          "despesasMes": 1850.00,
          "saldoAtual": 600.00,
          "orcamentoUtilizadoPercentual": 75
        }
        ```

### 1.2. Fluxo de Caixa

* **`GET /caixa/lancamentos`**
    * **Descrição:** Retorna uma lista de todos os lançamentos do fluxo de caixa, podendo ser filtrado por período.
    * **Query Params (Opcionais):** `?data_inicio=YYYY-MM-DD&data_fim=YYYY-MM-DD`
    * **Uso:** Alimenta a lista de "Últimos Lançamentos" na aba "Fluxo de Caixa".

* **`POST /caixa/lancamentos`**
    * **Descrição:** Registra um novo lançamento (entrada ou saída) no caixa.
    * **Uso:** Formulário "Registrar Lançamento no Caixa".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "tipo": "saida",
          "descricao": "Compra de material de limpeza",
          "valor": 80.00,
          "data": "2025-01-16",
          "metodo": "Pix",
          "categoria": "Geral"
        }
        ```

### 1.3. Mensalidades

* **`GET /mensalidades`**
    * **Descrição:** Retorna a lista de todos os meses de mensalidade já criados.
    * **Uso:** Card "Gerenciar Mensalidades" e dropdown de seleção de mês.

* **`POST /mensalidades`**
    * **Descrição:** Cria um novo mês de mensalidade.
    * **Uso:** Formulário "Criar Novo Mês".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "mes": "Março 2025",
          "valor": 50.00
        }
        ```

* **`PUT /mensalidades/{id}`**
    * **Descrição:** Edita o nome ou o valor de uma mensalidade.
    * **Uso:** Botão "Editar" no card "Gerenciar Mensalidades".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "mes": "Janeiro 2025 Editado",
          "valor": 55.00
        }
        ```

* **`GET /mensalidades/{id}/pagamentos`**
    * **Descrição:** Retorna a lista de todos os membros e o status de pagamento da mensalidade do mês selecionado.
    * **Uso:** Card "Controle de Pagamentos" ao selecionar um mês.

* **`PUT /mensalidades/{id}/pagamentos`**
    * **Descrição:** Atualiza o status de pagamento de um membro para uma mensalidade.
    * **Uso:** Botões de ação na lista de membros em "Controle de Pagamentos".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "codigo_sgc": "67890",
          "status": "pago",
          "metodo": "Cartão/Dinheiro"
        }
        ```

### 1.4. Eventos

* **`GET /eventos`**
    * **Descrição:** Retorna a lista de todos os eventos criados.
    * **Uso:** Abastece o card "Gerenciar Eventos" e os dropdowns de seleção de evento.

* **`POST /eventos`**
    * **Descrição:** Cria um novo evento.
    * **Uso:** Formulário "Criar Novo Evento".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "nome": "Caminhada Ecológica",
          "valorDesbravador": 25.00,
          "valorDiretoria": 10.00
        }
        ```

* **`PUT /eventos/{id}`**
    * **Descrição:** Atualiza os detalhes de um evento existente.
    * **Uso:** Botão "Editar" no card "Gerenciar Eventos".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "nome": "Acampamento de Verão 2025",
          "valorDesbravador": 160.00,
          "valorDiretoria": 80.00
        }
        ```

* **`GET /eventos/{id}/pagamentos`**
    * **Descrição:** Retorna a lista de membros inscritos em um evento e o status de pagamento de cada um.
    * **Uso:** Card "Controle de Pagamentos de Eventos" ao selecionar um evento.

* **`PUT /eventos/{id}/pagamentos`**
    * **Descrição:** Atualiza o status de pagamento de um membro para um evento.
    * **Uso:** Botões de ação na lista de membros em "Controle de Pagamentos de Eventos".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "codigo_sgc": "67890",
          "status": "pago"
        }
        ```

* **`POST /eventos/{id}/inscricoes`**
    * **Descrição:** Inscreve um membro em um evento.
    * **Uso:** Card "Inscrever Membro em Evento".
    * **Corpo da Requisição (Body):**
        ```json
        {
          "codigo_sgc": "11122",
          "status": "Pendente"
        }
        ```

### 1.5. Relatórios

* **`GET /relatorios/mensal`**
    * **Descrição:** Retorna os dados para o relatório financeiro de um mês específico.
    * **Query Params:** `?ano=2025&mes=1`
    * **Uso:** Card "Relatório Mensal / Fechamento de Mês".

* **`GET /relatorios/eventos/{id}`**
    * **Descrição:** Retorna os dados financeiros e de inscrições para um evento específico.
    * **Uso:** Card "Relatório de Eventos".

## 2. Apoio Regional

Canal de comunicação e recursos entre o clube e a coordenação regional.

* **`GET /regional/posts`**
    * **Descrição:** Retorna a lista de posts e comunicados da regional.
    * **Uso:** Card "Posts da Regional".

* **`GET /regional/avaliacoes`**
    * **Descrição:** Retorna a lista de datas de avaliações.
    * **Uso:** Card "Datas das Avaliações".

* **`GET /regional/arquivos`**
    * **Descrição:** Retorna a lista de arquivos e manuais para download.
    * **Uso:** Card "Arquivos e Manuais".

* **`GET /regional/mensagens`**
    * **Descrição:** Retorna o histórico de mensagens enviadas pelo clube para a regional.
    * **Uso:** Card "Minhas Mensagens Enviadas".

* **`POST /regional/mensagens`**
    * **Descrição:** Envia uma nova mensagem do clube para a regional.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "assunto": "Dúvida sobre o Camporee",
          "mensagem": "Gostaríamos de confirmar se o local permanece o mesmo."
        }
        ```

## 3. Avaliação Regional

Endpoints para a liderança regional avaliar o progresso dos membros.

* **`GET /avaliacoes/classes`**
    * **Descrição:** Retorna todos os requisitos de classe pendentes de avaliação ou para refazer.
    * **Query Params:** `?unidade_id=int` (para filtrar).
    * **Uso:** Aba "Classes".

* **`PUT /avaliacoes/classes/{id_avaliacao}`**
    * **Descrição:** Atualiza o status de um requisito de classe para um membro.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "status": "Aprovado"
        }
        ```
    * **Uso:** Botões de ação na aba "Classes".

* **`GET /avaliacoes/especialidades`**
    * **Descrição:** Retorna todas as especialidades pendentes de avaliação ou para refazer.
    * **Query Params:** `?unidade_id=int` (para filtrar).
    * **Uso:** Aba "Especialidades".

* **`PUT /avaliacoes/especialidades/{id_avaliacao}`**
    * **Descrição:** Atualiza o status de uma especialidade para um membro.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "status": "Refazer"
        }
        ```
    * **Uso:** Botões de ação na aba "Especialidades".

## 4. Pontuação

Endpoints para exibir rankings de desempenho e gerenciar pontos bônus.

* **`GET /ranking/unidades`**
    * **Descrição:** Retorna a pontuação total de cada unidade para o ranking geral.
    * **Uso:** Card "Ranking Geral das Unidades".

* **`GET /ranking/unidades/categorias`**
    * **Descrição:** Retorna a pontuação de cada unidade, separada por categoria.
    * **Uso:** Card "Ranking de Unidades por Categoria".

* **`GET /ranking/membros`**
    * **Descrição:** Retorna a pontuação detalhada de cada membro.
    * **Query Params:** `?cargo=string` (para filtrar).
    * **Uso:** Tabela "Ranking Individual de Membros".

* **`POST /pontuacao/bonus`**
    * **Descrição:** Lança um ponto bônus para uma unidade ou membro.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "tipo": "unidade",
          "id": 1,
          "pontos": 50,
          "descricao": "Decoração da sala da unidade."
        }
        ```
    * **Uso:** Aba "Lançar Bônus".

## 5. Patrimônio

Endpoints para gerenciamento do inventário e das solicitações de materiais.

* **`GET /patrimonio`**
    * **Descrição:** Retorna todos os itens do inventário do clube.
    * **Uso:** Abas "Gerenciar Patrimônio" e "Solicitar Materiais".

* **`POST /patrimonio`**
    * **Descrição:** Adiciona um novo item ao inventário.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "nome": "Lanterna de LED",
          "quantidade": 10,
          "descricao": "Modelo recarregável",
          "data_aquisicao": "2025-08-17"
        }
        ```
    * **Uso:** Formulário na aba "Gerenciar Patrimônio".

* **`GET /solicitacoes`**
    * **Descrição:** Retorna todas as solicitações de materiais feitas pelas unidades (visão da diretoria).
    * **Uso:** Aba "Solicitações de Materiais".

* **`GET /solicitacoes/minhas`**
    * **Descrição:** Retorna as solicitações feitas pelo usuário/unidade logado.
    * **Uso:** Card "Minhas Solicitações" na aba "Solicitar Materiais".

* **`POST /solicitacoes`**
    * **Descrição:** Cria uma nova solicitação de material.
    * **Corpo da Requisição (Body):**
        ```json
        {
          "reuniaoId": 1,
          "itens": [
            { "itemId": 1, "quantidade": 2 },
            { "itemId": 2, "quantidade": 1 }
          ]
        }
        ```
    * **Uso:** Formulário na aba "Solicitar Materiais".

* **`PUT /solicitacoes/{id}/status`**
    * **Descrição:** Atualiza o status de uma solicitação (Aprovar, Reprovar, Entregue, etc.).
    * **Corpo da Requisição (Body):**
        ```json
        {
          "status": "reprovado",
          "motivoReprovacao": "Item indisponível na data solicitada."
        }
        ```
