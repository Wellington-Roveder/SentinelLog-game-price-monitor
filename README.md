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
| SQLite | Persistência do histórico de preços |
| Streamlit | Dashboard interativo de visualização |
| N8N | Orquestração e envio de emails |
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
SQLite — salva apenas quando o preço muda
      ↓
Retorna promoções → N8N envia email
      ↓
Streamlit — Dashboard com histórico e gráficos
```

---

## ⚙️ Como Rodar

### Pré-requisitos
- Python 3.10+
- N8N instalado (local ou cloud)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Wellington-Roveder/SentinelLog--game-price-monitor.git
cd sentinellog

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz com:

```
DB_NAME=sentinel_log_prices.db
CHEAPSHARK_URL=https://www.cheapshark.com/api/1.0
```

### Executando

```bash
# Rodar o monitor manualmente (teste local)
python main.py

# Subir a API (para uso com N8N)
uvicorn api.my_api:app --reload --port 8001

# Rodar o dashboard
streamlit run dashboard/app.py
```

---

## 🧠 Decisões Técnicas

**Por que SQLite?**
Atende o MVP do projeto com conexão simples e zero configuração. A migração para PostgreSQL seria o próximo passo natural em caso de múltiplos usuários simultâneos ou volume maior de dados.

**Por que salvar só quando o preço muda?**
A lógica de comparação antes de inserir evita duplicatas desnecessárias no banco. Se o preço não mudou, nenhuma linha nova é criada — o banco só cresce quando há informação nova de verdade.

**Por que FastAPI como entrypoint?**
Permite que o N8N consuma o monitor via HTTP POST, desacoplando a execução do agendamento. O endpoint retorna as promoções encontradas, permitindo que o N8N decida se envia o email ou não baseado na resposta.

**Por que N8N para os emails?**
Separar a orquestração do código Python deixa cada parte com sua responsabilidade. O Python monitora e detecta, o N8N decide e notifica.

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

---

## 🔮 Melhorias Futuras

- [ ] Retry automático no N8N em caso de falha na requisição
- [ ] Suporte a múltiplos usuários com PostgreSQL
- [ ] Endpoint `GET /historico/{jogo}` para consultar preços via API
- [ ] Adicionar jogos via endpoint sem editar o `jogos.json` manualmente
- [ ] Notificação via Telegram além do email

---

## 📁 Estrutura do Projeto

```
sentinellog/
├── api/
│   ├── client.py           # Cliente HTTP reutilizável
│   ├── game_api_client.py  # Integração com CheapShark API
│   └── my_api.py           # API FastAPI
├── dashboard/
│   └── app.py              # Dashboard Streamlit
├── database/
│   └── db_manager.py       # Gerenciamento do SQLite
├── services/
│   └── sentinel_price.py   # Lógica principal do monitor
├── utils/
│   └── logger.py           # Logger com rotação diária
├── logs/                   # Logs gerados (ignorado pelo git)
├── jogos.json              # Lista de jogos monitorados
├── main.py                 # Entry point para teste local
├── requirements.txt        # Dependências
├── .env                    # Variáveis de ambiente (ignorado pelo git)
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
![dashboard1](assets/dashboard_2.png)

---

## 👤 Autor

Feito por **Wellington Roveder**  
[LinkedIn](https://www.linkedin.com/in/wellington-roveder-04637b37b/) • [GitHub](https://github.com/Wellington-Roveder?tab=repositories)
