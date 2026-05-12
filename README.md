# 🎮 SentinelLog — Monitor de Preços de Jogos

> Pipeline ETL em Python que monitora preços de jogos em tempo real via API REST, detecta variações automaticamente e envia alertas por email quando encontra promoções.

---

## 📌 Sobre o Projeto

O SentinelLog nasceu da ideia de não perder promoções de jogos. Ele consulta a [CheapShark API](https://www.cheapshark.com/), compara os preços com o histórico salvo no banco de dados e, quando detecta uma queda de preço, dispara um email de alerta automaticamente via N8N.

O projeto foi construído com foco em escalabilidade e boas práticas — separação de responsabilidades em camadas, logging estruturado com rotação diária, e automação de ponta a ponta sem intervenção manual.

---

## 🚀 Tecnologias

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| FastAPI + Uvicorn | API para expor o monitor como serviço |
| PostgreSQL | Persistência do histórico de preços |
| psycopg2 | Conector Python → PostgreSQL |
| Streamlit | Dashboard interativo de visualização |
| N8N | Orquestração e envio de emails |
| Docker + Docker Compose | Containerização dos serviços |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| Requests | Consumo da API externa |

---

## 🏗️ Arquitetura

```
N8N Schedule Trigger
      ↓
HTTP POST /executar (FastAPI)
      ↓
sentinel_price.py — busca e compara preços
      ↓
CheapShark API (preços em tempo real)
      ↓
PostgreSQL — salva apenas quando o preço muda
      ↓
Retorna promoções → N8N envia email
      ↓
Streamlit — Dashboard com histórico e gráficos
```

---

## ⚙️ Como Rodar

### Pré-requisitos
- Python 3.10+
- PostgreSQL instalado e rodando
- N8N instalado (local ou cloud)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Wellington-Roveder/SentinelLog-game-price-monitor.git
cd SentinelLog-game-price-monitor

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz com:

```
DB_NAME=sentinel_log
CHEAPSHARK_URL=https://www.cheapshark.com/api/1.0
USER=seu_usuario
SENHA=sua_senha
HOST=localhost
PORT=5432
```

> ⚠️ Crie o banco `sentinel_log` no PostgreSQL antes de rodar o projeto.

### Executando

```bash
# Rodar o monitor manualmente (teste local)
python main.py

# Subir a API (para uso com N8N)
uvicorn api.my_api:app --reload --port 8001

# Rodar o dashboard
streamlit run dashboard/app.py
```

### Com Docker

```bash
docker-compose up --build
```

---

## 🧠 Decisões Técnicas

**Por que PostgreSQL?**
Migrado do SQLite para suportar múltiplos usuários simultâneos, volume maior de dados e deploy em produção. A camada de banco ficou isolada no `db_manager.py`, tornando a migração transparente para o restante do sistema.

**Por que salvar só quando o preço muda?**
A lógica de comparação antes de inserir evita duplicatas desnecessárias no banco. Se o preço não mudou, nenhuma linha nova é criada — o banco só cresce quando há informação nova de verdade.

**Por que FastAPI como entrypoint?**
Permite que o N8N consuma o monitor via HTTP POST, desacoplando a execução do agendamento. O endpoint retorna as promoções encontradas, permitindo que o N8N decida se envia o email ou não baseado na resposta.

**Por que N8N para os emails?**
Separar a orquestração do código Python deixa cada parte com sua responsabilidade. O Python monitora e detecta, o N8N decide e notifica.

**Por que Docker?**
Garante que o ambiente seja reproduzível em qualquer máquina — sem problemas de dependências ou configuração manual do banco.

---

## 📊 Dashboard

O dashboard Streamlit exibe:
- Total de jogos monitorados
- Gráfico de variação de preço por jogo
- Tabela com todos os registros salvos

```bash
streamlit run dashboard/app.py
```

---

## 🐛 Dificuldades e Aprendizados

**Logger com rotação diária** — configurar o `TimedRotatingFileHandler` corretamente, evitar handlers duplicados com o guard `if not logger.handlers`, e entender que o arquivo fica travado enquanto o processo está rodando foram os principais desafios.

**Design do banco de dados** — a decisão entre usar `UNIQUE` com upsert versus inserção simples com validação na camada de serviço. Optei por manter a lógica no `sentinel_price.py` e deixar o banco responsável apenas por persistir, o que ficou mais limpo e escalável.

**Integração N8N + FastAPI** — entender o fluxo de dados entre o Schedule Trigger, o HTTP Request e o IF node para evitar spam de emails foi um aprendizado importante sobre orquestração de workflows.

**Migração SQLite → PostgreSQL** — adaptar o `db_manager.py` trocando `sqlite3` por `psycopg2`, ajustando placeholders de `?` para `%s`, e `AUTOINCREMENT` para `SERIAL`. A camada de serviço não precisou de nenhuma alteração.

---

## 🔮 Melhorias Futuras

- [x] Migração de SQLite para PostgreSQL
- [x] Containerização com Docker
- [ ] Substituir N8N por Celery + Redis para tarefas assíncronas
- [ ] Retry automático em caso de falha na requisição
- [ ] Endpoint `GET /historico/{jogo}` para consultar preços via API
- [ ] Adicionar jogos via endpoint sem editar o `jogos.json` manualmente
- [ ] Notificação via Telegram além do email
- [ ] Deploy em produção (Railway ou Render)

---

## 📁 Estrutura do Projeto

```
SentinelLog-game-price-monitor/
├── api/
│   ├── client.py           # Cliente HTTP reutilizável
│   ├── game_api_client.py  # Integração com CheapShark API
│   └── my_api.py           # API FastAPI
├── dashboard/
│   └── app.py              # Dashboard Streamlit
├── database/
│   └── db_manager.py       # Gerenciamento do PostgreSQL
├── services/
│   └── sentinel_price.py   # Lógica principal do monitor
├── utils/
│   └── logger.py           # Logger com rotação diária
├── logs/                   # Logs gerados (ignorado pelo git)
├── jogos.json              # Lista de jogos monitorados
├── main.py                 # Entry point para teste local
├── Dockerfile.api          # Dockerfile da FastAPI
├── Dockerfile.dashboard    # Dockerfile do Streamlit
├── docker-compose.yml      # Orquestração dos containers
├── requirements.txt        # Dependências
├── .env.example            # Exemplo de variáveis de ambiente
└── .gitignore
```

---

### PRINTS DE EXECUÇÃO:

### N8N
![workflow](assets/worflow_n8n.png)
![Sucesso_no_workflow](assets/workflow_sucess.png)

### LOGS
![LOGGING](assets/logg_action.png)

### STREAMLIT
![dashboard1](assets/dashboard_1.png)
![dashboard2](assets/dashboard_2.png)

---

## 👤 Autor

Feito por **Wellington Roveder**  
[LinkedIn](https://www.linkedin.com/in/wellington-roveder-04637b37b/) • [GitHub](https://github.com/Wellington-Roveder?tab=repositories)