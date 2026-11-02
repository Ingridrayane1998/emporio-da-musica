# Arquitetura do Sistema - Ozzy (Empório da Música)

Este documento registra a arquitetura do agente Ozzy, seus fluxos de integração e decisões estruturais.

## Visão Geral

```
Usuário ► UI (Chat Front-end)
             │
             ▼
      FastAPI /chat (Localhost:8000)
             │
             ▼
       Orquestrador (Ozzy)
  Groq API + system prompt + guardrails
             │
             ├────────► Function Calling ───► acionar_atendente() ──► Ticket
             │
             ├────────► buscar_politicas() ──► RAG (ChromaDB local)
             │
             └────────► Ferramentas SQL seguras ──► SQLite (via SQLAlchemy)
```

## Componentes

1. **Front-end:** Interface exportada do Google AI Studio com chat interativo, áudios de demonstração e vitrine de instrumentos.
2. **Backend API:** FastAPI rodando localmente, expondo endpoints de chat, health check e catálogo.
3. **Orquestrador LLM:** Integração com Groq API executando modelo de alta performance com Function Calling.
4. **Base Relacional:** SQLite local para dados estruturados de clientes, pedidos, itens, produtos e promoções.
5. **Base Vetorial:** ChromaDB em disco para busca semântica em políticas e regulamentos da loja.

---

## Modelo de Dados Relacional (SQLite)

Diagrama de Entidade-Relacionamento (ER) implementado via SQLAlchemy em `src/emporio_ozzy/db/models.py`:

```mermaid
erDiagram
    CATEGORIES ||--o{ PRODUCTS : categorizes
    CUSTOMERS ||--o{ ORDERS : places
    CUSTOMERS ||--o{ TICKETS : opens
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
    PRODUCTS ||--o{ PROMOTIONS : has

    CATEGORIES {
        int category_id PK
        string name
        string description
    }
    CUSTOMERS {
        int customer_id PK
        string name
        string phone
        string email UK
        string city
        int is_active
    }
    PRODUCTS {
        int product_id PK
        string name
        int category_id FK
        float price_brl
        int stock_quantity
        string status
        string specs
        string description
        string created_at
    }
    ORDERS {
        int order_id PK
        int customer_id FK
        string order_date
        string status
        float total_brl
        string payment_method
        string tracking_code
        string estimated_delivery
        string notes
    }
    ORDER_ITEMS {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
    }
    PROMOTIONS {
        int promotion_id PK
        int product_id FK
        int discount_percent
        string description
        int is_active
    }
    TICKETS {
        string ticket_id PK
        int customer_id FK
        string reason
        string priority
        string status
        string conversation_summary
        string created_at
    }
```
