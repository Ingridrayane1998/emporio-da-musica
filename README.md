# Empório da Música & Ozzy

Instruções para configuração, preparação dos dados e execução local da aplicação.

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

