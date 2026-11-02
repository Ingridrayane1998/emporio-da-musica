# Log de Decisões Técnicas (ADR) - Ozzy

Registro das decisões arquiteturais e técnicas tomadas durante o desenvolvimento do agente Ozzy.

---

## ADR 001 - Setup e Estrutura Inicial do Projeto
* **Data:** 02/11/2026
* **Status:** Aceito
* **Contexto:** Necessidade de estruturar o projeto com separação clara entre código fonte (`src/emporio_ozzy`), dados brutos protegidos por LGPD (`data/raw`), documentação (`docs/`) e suíte de testes (`tests/`).
* **Decisão:**
  - Isolamento estrito de dados brutos de clientes em `data/raw/` com inclusão no `.gitignore`.
  - Configurações centralizadas via `pydantic-settings` lendo `.env`.
  - Padrão de branches por etapa (`feat/etapa-XX-...`) e commits semânticos aprovados pelo desenvolvedor.
* **Consequências:** Conformidade com a LGPD, ambiente reproduzível e organização modular para testes automatizados.

