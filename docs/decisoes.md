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

---

## ADR 002 - Organização da Interface e Servidor Web Local
* **Data:** 02/11/2026
* **Status:** Aceito
* **Contexto:** O projeto necessita servir a interface visual do chat gerada no Google AI Studio / Google Stitch de forma independente, sem exigir runtime ou build de Node.js no ambiente de produção/avaliação local.
* **Decisão:**
  - Focar a tela exclusivamente na experiência do chat de atendimento do Ozzy no contexto da loja Empório da Música.
  - Implementar a camada web servida diretamente pelo FastAPI (`StaticFiles` e `templates/index.html`), com JavaScript vanilla e Web Audio API para simulação sonora dos timbres de instrumentos.
  - Manter os arquivos de assets visuais originais (avatar do Ozzy, fotos de instrumentos de alta fidelidade) em `src/emporio_ozzy/web/static/images/`.
* **Consequências:** Inicialização instantânea com `python scripts/run_dev.py` em `http://localhost:8000`, sem erros de dependências externas ou compiladores de JS no host.
