# Dicionário de Dados e Relatório de Perfilamento - Empório da Música

Este documento registra o perfilamento, tipos, chaves e regras de limpeza aplicadas aos dados tabulares (CSVs) da loja Empório da Música.

---

## 1. Resumo Geral das Tabelas Brutas

| Arquivo | Registros | Colunas | Linhas Duplicadas | Integridade Referencial |
| :--- | :--- | :--- | :--- | :--- |
| `categories.csv` | 9 | 3 | 0 | 100% válida |
| `customers.csv` | 50 | 5 | 0 | 1 e-mail duplicado (IDs 11 e 43) |
| `orders.csv` | 20 | 9 | 0 | 100% dos `customer_id` existem |
| `order_items.csv` | 22 | 3 | 0 | 100% dos `order_id` e `product_id` existem |
| `products.csv` | 65 | 9 | 0 | 100% dos `category_id` existem |
| `promotions.csv` | 25 | 5 | 0 | 100% dos `product_id` existem |

---

## 2. Detalhamento por Tabela

### 2.1. `categories.csv`
* **Descrição:** Categorias dos produtos (instrumentos de corda, áudio, percussão, etc.).
* **Chave Primária:** `category_id` (PK)

| Coluna | Tipo Inferido | Nulos (%) | Únicos | Descrição e Amostras |
| :--- | :--- | :--- | :--- | :--- |
| `category_id` | `INTEGER` | 0 (0.0%) | 9 | Identificador sequencial (1 a 9) |
| `name` | `VARCHAR(100)` | 0 (0.0%) | 9 | Nome da categoria (ex: "Guitarras", "Baixos") |
| `description` | `TEXT` | 0 (0.0%) | 9 | Descrição detalhada da categoria |

---

### 2.2. `customers.csv`
* **Descrição:** Clientes cadastrados na loja.
* **Chave Primária:** `customer_id` (PK)

| Coluna | Tipo Inferido | Nulos (%) | Únicos | Descrição e Amostras |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `INTEGER` | 0 (0.0%) | 50 | Identificador sequencial do cliente |
| `name` | `VARCHAR(150)` | 0 (0.0%) | 50 | Nome completo do cliente |
| `phone` | `VARCHAR(20)` | 0 (0.0%) | 50 | Telefone formatado com DDD: `(67) 99812-3456` |
| `email` | `VARCHAR(150)` | 0 (0.0%) | 49 | E-mail do cliente (1 duplicata encontrada) |
| `city` | `VARCHAR(100)` | 0 (0.0%) | 5 | Cidade do cliente (ex: "Campo Grande") |

* **Achado LGPD & Duplicidade:**
  - O e-mail `bruno.martins@jmail.com` pertence a:
    - `customer_id=11`: "Bruno Carvalho Martins" (possui o pedido `#10`).
    - `customer_id=43`: "Bruno Martins" (sem pedidos associados).

---

### 2.3. `orders.csv`
* **Descrição:** Pedidos de compra realizados na loja.
* **Chave Primária:** `order_id` (PK)
* **Chave Estrangeira:** `customer_id` $\rightarrow$ `customers.customer_id`

| Coluna | Tipo Inferido | Nulos (%) | Únicos | Descrição e Amostras |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `INTEGER` | 0 (0.0%) | 20 | Identificador do pedido |
| `customer_id` | `INTEGER` | 0 (0.0%) | 18 | ID do cliente associado |
| `order_date` | `DATE` | 0 (0.0%) | 20 | Data da compra (ISO: `YYYY-MM-DD`) |
| `status` | `VARCHAR(30)` | 0 (0.0%) | 5 | `delivered` (7), `cancelled` (4), `confirmed` (4), `pending` (4), `shipped` (1) |
| `total_brl` | `DECIMAL(10,2)`| 0 (0.0%) | 18 | Valor total do pedido em Reais |
| `payment_method`| `VARCHAR(50)` | 0 (0.0%) | 6 | `pix`, `credit_1x`, `credit_6x`, `credit_12x`, `boleto` |
| `tracking_code` | `VARCHAR(50)` | 12 (60.0%)| 8 | Código dos Correios/transportadora (ex: `BRAB1234567BR`) |
| `estimated_delivery`| `DATE` | 12 (60.0%)| 8 | Previsão de entrega (apenas pedidos enviados/entregues) |
| `notes` | `TEXT` | 16 (80.0%)| 4 | Motivo do cancelamento (apenas pedidos cancelados) |

* **Regra de Nulos:** Os 12 nulos em `tracking_code` e `estimated_delivery` são legítimos da regra de negócio: pedidos com status `cancelled`, `confirmed` e `pending` ainda não geraram remessa.

---

### 2.4. `order_items.csv`
* **Descrição:** Itens individuais contidos em cada pedido.
* **Chaves Estrangeiras:**
  - `order_id` $\rightarrow$ `orders.order_id`
  - `product_id` $\rightarrow$ `products.product_id`

| Coluna | Tipo Inferido | Nulos (%) | Únicos | Descrição e Amostras |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `INTEGER` | 0 (0.0%) | 20 | Pedido de referência |
| `product_id` | `INTEGER` | 0 (0.0%) | 17 | Produto adquirido |
| `quantity` | `INTEGER` | 0 (0.0%) | 2 | Quantidade de unidades (1 ou 2) |

---

### 2.5. `products.csv`
* **Descrição:** Catálogo de instrumentos e acessórios musicais.
* **Chave Primária:** `product_id` (PK)
* **Chave Estrangeira:** `category_id` $\rightarrow$ `categories.category_id`

| Coluna | Tipo Inferido | Nulos (%) | Únicos | Descrição e Amostras |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | `INTEGER` | 0 (0.0%) | 65 | ID do produto |
| `name` | `VARCHAR(200)`| 0 (0.0%) | 65 | Nome do instrumento/acessório |
| `category_id` | `INTEGER` | 0 (0.0%) | 6 | Categoria do produto |
| `price_brl` | `DECIMAL(10,2)`| 0 (0.0%) | 58 | Preço regular em Reais |
| `stock_quantity`| `INTEGER` | 0 (0.0%) | 16 | Quantidade em estoque (0 a 30) |
| `status` | `VARCHAR(30)` | 0 (0.0%) | 3 | `active` (62), `discontinued` (2), `coming_soon` (1) |
| `specs` | `JSON / TEXT` | 0 (0.0%) | 58 | Especificações técnicas em formato JSON |
| `description` | `TEXT` | 0 (0.0%) | 65 | Descrição comercial e características sonoras |
| `created_at` | `DATE` | 0 (0.0%) | 55 | Data de cadastro |

---

### 2.6. `promotions.csv`
* **Descrição:** Campanhas e descontos vinculados a produtos.
* **Chave Primária:** `promotion_id` (PK)
* **Chave Estrangeira:** `product_id` $\rightarrow$ `products.product_id`

| Coluna | Tipo Inferido | Nulos (%) | Únicos | Descrição e Amostras |
| :--- | :--- | :--- | :--- | :--- |
| `promotion_id` | `INTEGER` | 0 (0.0%) | 25 | ID da promoção |
| `product_id` | `INTEGER` | 0 (0.0%) | 22 | Produto associado |
| `discount_percent`| `INTEGER` | 0 (0.0%) | 13 | Percentual de desconto (5% a 30%) |
| `description` | `VARCHAR(150)`| 0 (0.0%) | 8 | Campanha (ex: "Black Friday", "Liquidação") |
| `is_active` | `BOOLEAN / INT`| 0 (0.0%) | 2 | `1` (ativa: 4 produtos) ou `0` (encerrada: 21 produtos) |

---

## 3. Decisões de Limpeza e Normalização Propostas

1. **Normalização de Nomes e Colunas:**
   - Todos os nomes de colunas já estão em `snake_case` e serão mantidos.
   - Na tabela `order_items`, adicionar a coluna `order_item_id` sequencial (PK) para garantir chave primária simples na modelagem relacional SQLAlchemy.
2. **Tratamento de Nulos:**
   - Em `orders`, manter `tracking_code`, `estimated_delivery` e `notes` como nulos (NULL) quando não aplicáveis, pois refletem o estado legítimo do ciclo de vida do pedido.
3. **Tratamento da Duplicata de E-mail (`customers`):**
   - O e-mail `bruno.martins@jmail.com` possuía 2 clientes cadastrados.
   - **Decisão aprovada:** Priorizar o cliente cadastrado primeiro (`customer_id=11`, ativo com pedido `#10`), e desativar o cadastro posterior (`customer_id=43`, sem pedidos) com a flag `is_active=0` e e-mail `bruno.martins+desativado43@jmail.com`, garantindo 100% de unicidade na base de clientes.
4. **Campo `specs` em `products`:**
   - Validar que todo `specs` é um JSON sintaticamente válido.
5. **Geração de Amostras (`data/sample/`):**
   - Gerar cópia de 5 a 10 registros de cada tabela com nomes, telefones e e-mails fictícios gerados proceduralmente para compor o versionamento do GitHub em total conformidade com a LGPD.
