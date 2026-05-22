# 🎮 SentinelLog — Game Price Monitor

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Tests](https://img.shields.io/badge/Tests-Pytest-yellow)
![Railway](https://img.shields.io/badge/Deploy-Railway-purple)

> A Python ETL pipeline that monitors game prices in real time via REST API, automatically detects price changes, and sends email alerts when deals are found.

---

## 📌 About the Project

SentinelLog was born from the idea of never missing a game sale. It queries the [CheapShark API](https://www.cheapshark.com/), compares prices against a history saved in the database, and automatically fires an alert via N8N whenever a price drop is detected.

The project was built with scalability and best practices in mind — layered separation of concerns, structured logging with daily rotation, and end-to-end automation with no manual intervention.

SentinelLog is currently deployed in production and growing more robust with every sprint. Beyond a price monitor, it is a full monitoring API — turning a simple automation into a real, scalable project.

---

## 🚀 Technologies

| Technology | Usage |
|---|---|
| Python | Core language |
| FastAPI + Uvicorn | API to expose the monitor as a service |
| PostgreSQL | Price history persistence |
| psycopg2 | Python → PostgreSQL connector |
| Redis | Store cache and API optimization |
| Streamlit | Interactive visualization dashboard |
| N8N | Orchestration and email delivery |
| Docker + Docker Compose | Service containerization |
| python-dotenv | Environment variable management |
| Requests | External API consumption |

---

## 🏗️ Architecture

```
N8N Schedule Trigger
      ↓
HTTP POST /executar (FastAPI)
      ↓
sentinel_price.py — fetches and compares prices
      ↓
CheapShark API (real-time prices)
      ↓
Redis cache (24h TTL)
      ↓
PostgreSQL — saves only when the price changes
      ↓
Returns deals → N8N sends email
      ↓
Streamlit — Dashboard with history and charts
```

---

## 🐳 Docker Architecture

The application runs in a multi-container environment orchestrated with Docker Compose.

Services:

- **FastAPI** — application entrypoint, exposes the monitor as a REST service
- **Streamlit** — interactive dashboard for price history visualization
- **PostgreSQL** — persistent relational database
- **Redis** — cache layer for store data

All services communicate through Docker internal networking, using isolated containers and persistent volumes.

```bash
docker-compose up --build
```

---

## ⚡ Redis Cache

The list of stores returned by CheapShark is cached in Redis with a 24-hour TTL, reducing unnecessary external API requests and improving monitor performance. This avoids redundant calls to external services on every execution cycle.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/executar` | Executes the price monitor |
| GET | `/historico/{game}` | Returns price history for a specific game |
| POST | `/jogos` | Adds a game to the monitored list |
| GET | `/jogos` | Lists all monitored games |
| DELETE | `/jogos/{id}` | Removes a game from the monitored list |

All endpoints require authentication via `x-api-key` header.

---

## 🛡️ Production Concerns

- Environment variable isolation via `.env`
- Dockerized services with Docker Compose
- Persistent PostgreSQL volumes
- Redis cache layer with TTL
- API authentication via `x-api-key`
- Structured logging with daily rotation
- Connection pooling with `ThreadedConnectionPool`
- Correct HTTP status codes on all endpoints
- Automatic retry with exponential backoff on API failures
- Rate limit handling for external APIs

---

## ⚙️ How to Run

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- N8N installed (local or cloud)

### Installation

```bash
# Clone the repository
git clone https://github.com/Wellington-Roveder/SentinelLog-game-price-monitor.git
cd SentinelLog-game-price-monitor

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Environment Variables

Create a `.env` file at the project root:

```
DB_NAME=sentinel_log
CHEAPSHARK_URL=https://www.cheapshark.com/api/1.0
DB_USER=your_user
DB_SENHA=your_password
DB_HOST=localhost
DB_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
INTERNAL_API_KEY=your_key
```

> ⚠️ Create the `sentinel_log` database in PostgreSQL before running the project.

### Running

```bash
# Run the monitor manually (local test)
python main.py

# Start the API
uvicorn api.my_api:app --reload --port 8001

# Run the dashboard
python -m streamlit run dashboard/app.py
```

### With Docker

```bash
docker-compose up --build
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

Tests cover:

- Retry decorator behavior under HTTP failures
- Service layer business rules with `MagicMock`
- Isolated unit tests with no external dependencies
- HTTP failure simulation and error handling

---

## 🧠 Technical Decisions

**Why PostgreSQL?**
Migrated from SQLite to support multiple concurrent users, larger data volumes, and production deployments. The database layer is isolated in `db_manager.py`, making the migration transparent to the rest of the system.

**Why save only when the price changes?**
The comparison logic before inserting avoids unnecessary duplicates in the database. If the price hasn't changed, no new row is created — the database only grows when there is genuinely new information.

**Why FastAPI as the entrypoint?**
It allows N8N to consume the monitor via HTTP POST, decoupling execution from scheduling. The endpoint returns the deals found, letting N8N decide whether to send an email based on the response.

**Why N8N for emails?**
Separating orchestration from the Python code gives each part a single responsibility. Python monitors and detects; N8N decides and notifies.

**Why Docker?**
Ensures the environment is reproducible on any machine — no dependency issues or manual database configuration.

**Production readiness**
Endpoints were implemented to manage the list of monitored games without taking the application down — adding and removing games via API, plus an endpoint to query price history outside the dashboard.

**ThreadedConnectionPool**
The connection pool handles dead connections automatically, reusing them across requests. This avoids the overhead of authentication and network setup required to establish a connection from scratch, reduces request latency, and preserves memory and processing on the database server.

**Authentication**
Every endpoint requires authentication via `x-api-key`, returning the correct HTTP status codes on failure. Since the endpoints will be consumed by both N8N and external users, security handling was implemented from the start. Future improvements will include token generation and refresh for real-time use.

**Unit Tests**
Unit tests ensure coverage of business rule changes. Tests were implemented using the Pytest framework together with `unittest.mock` via `MagicMock`, allowing dependencies to be simulated and behaviors validated in an isolated, reliable way.

**Retry with exponential backoff**
The HTTP client implements automatic retry with exponential backoff (2s, 4s, 8s) for transient failures. Rate limit responses (429) trigger a 60-second pause before continuing to the next game.

---

## 📊 Dashboard

The Streamlit dashboard displays:
- Total monitored games
- Price variation chart per game
- Table with all saved records

```bash
python -m streamlit run dashboard/app.py
```

---

## ☁️ Deployment

The project is deployed on **Railway** with managed PostgreSQL and Redis.

Live API: `https://responsible-unity-production-32d1.up.railway.app`

Also compatible with:
- Render
- VPS with Docker
- Oracle Cloud Free Tier

---

## 🐛 Challenges & Learnings

**Logger with daily rotation** — correctly configuring `TimedRotatingFileHandler`, avoiding duplicate handlers with the `if not logger.handlers` guard, and understanding that the file stays locked while the process is running were the main challenges.

**Database design** — the decision between using `UNIQUE` with upsert versus simple insertion with validation at the service layer. The logic lives in `sentinel_price.py`, leaving the database responsible only for persistence — cleaner and more scalable.

**N8N + FastAPI integration** — understanding the data flow between the Schedule Trigger, the HTTP Request node, and the IF node to avoid email spam was an important lesson in workflow orchestration.

**SQLite → PostgreSQL migration** — adapting `db_manager.py` by swapping `sqlite3` for `psycopg2`, adjusting placeholders from `?` to `%s`, and `AUTOINCREMENT` to `SERIAL`. The service layer required no changes at all.

**HTTP error handling** — understanding that returning `200 OK` with `{"status": "error"}` in the body is not the same as returning a real HTTP error. Tools like N8N cannot treat this as a failure — the correct status code is what defines the automation's behavior.

**Connection pool** — migrating from a single connection in `__init__` to a shared `ThreadedConnectionPool`, ensuring the application does not break if the database restarts and that multiple simultaneous requests are handled correctly.

**Rate limiting** — handling CheapShark's rate limit in production by implementing randomized delays between requests and a dedicated 60-second pause on 429 responses.

---

## 🔮 Future Improvements

- [x] Migration from SQLite to PostgreSQL
- [x] Containerization with Docker
- [x] Connection pooling with `ThreadedConnectionPool`
- [x] `GET /historico/{game}` endpoint to query prices via API
- [x] Game management via endpoints (`POST`, `GET`, `DELETE`)
- [x] Store cache with Redis (24h TTL)
- [x] Automatic retry with exponential backoff on API failures
- [x] Production deployment on Railway
- [ ] JWT authentication with token refresh
- [ ] Telegram notifications in addition to email

---

## 📁 Project Structure

```
SentinelLog-game-price-monitor/
├── api/
│   ├── client.py           # Reusable HTTP client with retry
│   ├── game_api_client.py  # CheapShark API integration
│   └── my_api.py           # FastAPI application
├── dashboard/
│   └── app.py              # Streamlit dashboard
├── database/
│   ├── connection.py       # PostgreSQL connection pool
│   ├── db_manager.py       # Database management
│   └── redis_client.py     # Redis cache client
├── services/
│   └── sentinel_price.py   # Core monitor logic
├── tests/
│   ├── test_sentinel_price.py
│   └── test_retry.py
├── utils/
│   └── logger.py           # Logger with daily rotation
├── logs/                   # Generated logs (git-ignored)
├── main.py                 # Entry point for local testing
├── Dockerfile.api          # FastAPI Dockerfile
├── Dockerfile.dashboard    # Streamlit Dockerfile
├── docker-compose.yml      # Container orchestration
├── requirements.txt        # Dependencies
├── .env.example            # Environment variable example
└── .gitignore
```

---

## 📸 Screenshots

#### N8N Workflow
![workflow](assets/worflow_n8n.png)
![Workflow success](assets/workflow_sucess.png)

#### Logs
![Logging](assets/logg_action.png)

#### Streamlit Dashboard
![Dashboard 1](assets/dashboard_1.png)
![Dashboard 2](assets/dashboard_2.png)

#### Swagger Documentation
![Endpoints](assets/doc_api.png)
![Schemas](assets/api_schemas.png)

---

## 👤 Author

Made by **Wellington Roveder**  
[LinkedIn](https://www.linkedin.com/in/wellington-roveder-04637b37b/) • [GitHub](https://github.com/Wellington-Roveder?tab=repositories)