# Empório da Música - Ozzy, o agente de atendimento

### Justificativa e escolhas durante o desenvolvimento do agente:
O projeto foi desenvolvido utilizando o Google Antigravity como ferramenta principal para o desenvolvimento do código.

Meu workflow de desenvolvimento consiste nos seguintes passos:

1- Criar um plano de desenvolvimento passo a passo no Claude para utilizar no assistente de código;

2- Desenvolver o prototipo da identidade visual no Google Stich;

3- Subir os prototipos visuais no Google AI Studio e levar para o Github (Frontend)

4- Se necessário refinar ou alterar o plano de desenvolvimento no Gemini;

5- Conectar o repositorio do Github no Google Antigravity, anexar o plano de desenvolvimento gerado no Claude e iniciar o desenvolvimento passo a passo do backend, e após a conexão com o frontend gerado. 

6 - Modelagem e padronização dos dados - No CSV de clientes percebi uma duplicidade de e-mails em dois clientes, então priorizei o cliente que havia criado o cadastro primeiro e desativei o segundo, pois o mesmo não tinha nenhum pedido.

---

• Abordagem Escolhida — Arquitetura Híbrida com Function Calling
Para que o agente consiguisse transitar de forma precisa por diferentes fontes de informação, textos não estruturados e tabelas relacionais, estruturei uma arquitetura híbrida.

Modelei um banco de dados relacional (SQLite) a partir das planilhas em CSV e um banco vetorial (ChromaDB) com os dados extraídos do PDF. Essa escolha foi motivada por uma experiência anterior no desenvolvimento de agentes, na qual o principal gargalo foi a ausência de busca semântica, pois o modelo frequentemente dizia ter encontrado a resposta apenas por haver palavras coincidentes entre a pergunta e o texto, gerando alucinações.

Por isso, adotei o Function Calling como mecanismo orquestrador central para acionar o RAG e o SQL:

RAG: O PDF de políticas foi segmentado em chunks semânticos com sobreposição e indexado no banco vetorial, sendo consultado via ferramenta buscar_politicas.

SQL: Consultas estruturadas de produtos, estoque e pedidos foram transformados em funções (buscar_produtos, consultar_pedido, etc), eliminando riscos de injeção ou alucinação.

Implementei uma camada de Guardrails pré-LLM para avaliação de sentimento/insatisfação e interceptação imediata de assuntos fora de contexto, enquanto o padrão ReAct rege o loop de decisão e resposta final do agente.

Provedor LLM: Groq openai (gpt-oss-120b)

* Limitações:
Para os próximos eu pensaria em melhorar a interface do Chat e experiencia do usuário final (UX), como por exemplo: Implementar o circulo verde, como se o agente estivesse online, melhorar a disposição do chat no navegador e desenvolver uma interface mobile também.

---


## Exemplos de interações com o agente:

* Consulta de status do pedido:
<img width="1365" height="767" alt="teste1_consulta_de_pedido" src="https://github.com/user-attachments/assets/676e2343-7a1f-44a0-8d06-226510394b09" />



* Perguntando ao agente se posso consultar o pedido de outra pessoa:
<img width="1364" height="767" alt="teste2_tentando_consultar_pedido_de_outra_pessoa" src="https://github.com/user-attachments/assets/1a3cd2ea-0b50-4cc2-9dfd-bebbe41cd677" />



* Consulta de status do pedido com dados incorretos:
<img width="1365" height="767" alt="teste3_informando_pedido_incorreto" src="https://github.com/user-attachments/assets/1b7f6182-633d-4dfa-b2e2-10c4c6d1831a" />



* Desvio de assunto:
<img width="1365" height="766" alt="teste4_desvio_de_assunto" src="https://github.com/user-attachments/assets/c97c6798-54b7-4dc5-b87b-15ffae7f9bbb" />



* Consulta de política de devolução:
<img width="1363" height="767" alt="teste5_consulta_politica_de_devolucao" src="https://github.com/user-attachments/assets/2b875aba-4038-460a-9b3e-7ac5017c552c" />





---

# Instruções para configuração, preparação dos dados e execução local da aplicação.

---

## 1. Pré-requisitos

* **Python 3.10+** instalado
* Chave de API do **Groq** ([obtenha gratuitamente no console do Groq](https://console.groq.com))

---

## 2. Configuração do Ambiente

### 2.1 Clonar o repositório e acessar a pasta
```bash
git clone https://github.com/Ingridrayane1998/emporio-da-musica.git
cd emporio-da-musica
```

### 2.2 Criar e ativar o ambiente virtual

* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

* **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 2.3 Instalar as dependências
```bash
pip install -r requirements.txt
```
*(ou `pip install -e ".[dev]"`)*

---

## 3. Variáveis de Ambiente e Provedor do Modelo

Copie o arquivo de exemplo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e configure sua chave da API Groq e o modelo desejado:

```env
# Chave de API do Groq
GROQ_API_KEY=gsk_sua_chave_groq_aqui

# Modelo LLM utilizado (ex.: openai/gpt-oss-120b ou llama-3.3-70b-versatile)
GROQ_MODEL=openai/gpt-oss-120b

# Caminhos locais de dados (padrão)
DB_PATH=data/emporio.db
CHROMA_PATH=data/chroma

# Servidor FastAPI
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=INFO
```

---

## 4. Comandos de Preparação dos Bancos de Dados

Antes de iniciar a aplicação, popule o banco relacional SQLite e o banco vetorial ChromaDB:

### 4.1 Construir o banco relacional SQLite (ETL e catálogo)
```bash
python scripts/build_db.py
```
> Executa o perfilamento, limpeza dos dados brutos e gera o banco SQLite em `data/emporio.db`.

### 4.2 Construir o índice vetorial ChromaDB (RAG das políticas)
```bash
python scripts/build_vectorstore.py
```
> Extrai o texto de `data/raw/politicas_da_loja.pdf`, gera os chunks semânticos com embeddings e persiste o índice em `data/chroma/`.

---

## 5. Execução da Aplicação

Inicie o servidor de desenvolvimento local:

```bash
python scripts/run_dev.py
```

* **Interface Web do Chat:** [http://localhost:8000](http://localhost:8000)
* **Status / Health check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)
* **Documentação interativa Swagger (FastAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 6. Execução de Testes e Qualidade de Código

Para rodar a suíte de testes automatizados:

```bash
pytest
```

Para verificar o padrão de formatação e linting:

```bash
ruff check src tests scripts
```

