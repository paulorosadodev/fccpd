# ⚔️ Arena de Batalhas: Desafio Docker Compose de Orquestração

Este projeto demonstra orquestração de múltiplos serviços com Docker Compose através de uma **Arena de Batalhas RPG**! Três serviços interdependentes trabalham juntos: uma API Flask para gerenciar batalhas, PostgreSQL para persistir dados e Redis para cache de rankings em tempo real.

## 🎯 Objetivo

Demonstrar orquestração completa de serviços com Docker Compose:
- ⚔️ **3 Serviços Interdependentes**: Web (Flask), Database (PostgreSQL), Cache (Redis)
- 🔗 **Comunicação entre Serviços**: API consulta database e cache
- 🌐 **Rede Interna Customizada**: Todos os serviços na mesma rede
- 📦 **Depends_on com Conditions**: Ordem correta de inicialização
- 🔧 **Variáveis de Ambiente**: Configuração centralizada
- 💾 **Volumes para Persistência**: Dados e cache persistidos

## ▶️ Como rodar o desafio:

```bash
# Tornar scripts executáveis (primeira vez)
chmod +x start.sh test-services.sh battle-demo.sh

# Iniciar todos os serviços
./start.sh
```

O script `start.sh` irá:
1. Construir as 3 imagens Docker
2. Criar rede customizada arena-network
3. Iniciar Database e Cache com health checks
4. Iniciar API apenas após dependências estarem prontas
5. Mostrar status de todos os serviços

### 🧪 Testar Comunicação Entre Serviços

Para **comprovar que os 3 serviços estão se comunicando**:

```bash
# Execute o script de teste automatizado
./test-services.sh
```

**O que esse script faz:**
1. ✅ Health check de todos os 3 serviços
2. 📊 API consulta heróis no Database (PostgreSQL)
3. 🏆 API usa Cache (Redis) para ranking
4. ⚔️ Cria batalha (integração completa dos 3 serviços)
5. 📈 Mostra estatísticas e histórico

### ⚔️ Demonstração de Batalhas

```bash
# Simula 5 batalhas épicas
./battle-demo.sh
```

## ✅ Requisitos Atendidos + Sistema RPG

### ✓ 3 Serviços Orquestrados

**1. Battle Arena (Web/API - Flask)**
- API REST para gerenciar batalhas entre heróis
- Endpoints para criar batalhas, ver ranking, histórico
- Conecta simultaneamente ao Database e Cache
- Health checks integrados

**2. Arena Database (PostgreSQL)**
- Armazena heróis, batalhas e estatísticas
- Schema completo com views e índices
- 8 heróis pré-cadastrados
- Persistência via volume

**3. Arena Cache (Redis)**
- Cache de rankings em tempo real
- TTL de 60 segundos para rankings
- Contadores de estatísticas
- Persistência via AOF (Append Only File)

### ✓ Depends_on e Health Checks

```yaml
battle-arena:
  depends_on:
    arena-database:
      condition: service_healthy
    arena-cache:
      condition: service_healthy
```

- API **só inicia** após Database e Cache estarem saudáveis
- Evita erros de conexão
- Ordem correta de inicialização garantida

### ✓ Rede Interna Customizada

```yaml
networks:
  arena-network:
    name: arena-network
    driver: bridge
    ipam:
      config:
        - subnet: 172.25.0.0/16
```

- Todos os serviços na mesma rede isolada
- Comunicação via DNS interno (hostnames)
- API acessa: `arena-database:5432` e `arena-cache:6379`

### ✓ Variáveis de Ambiente

Configuração centralizada no `docker-compose.yml`:
- Database: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- Cache: configurado via `command` (AOF habilitado)
- API: `FLASK_ENV`, `PYTHONUNBUFFERED`

### ✓ Comunicação Demonstrada

**Fluxo de uma Batalha:**
1. Cliente faz POST `/battle` na API
2. API consulta heróis no **PostgreSQL**
3. API simula batalha
4. API salva resultado no **PostgreSQL**
5. API invalida cache do **Redis**
6. Próxima consulta ao ranking usa cache

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                      Host Machine                           │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Docker Network: arena-network                  │ │
│  │              (172.25.0.0/16)                           │ │
│  │                                                        │ │
│  │                                                        │ │
│  │         ┌──────────────────────┐                       │ │
│  │         │   battle-arena       │                       │ │
│  │         │   (Flask API)        │                       │ │
│  │         │   Port: 5000         │                       │ │
│  │         └──────────┬───────────┘                       │ │
│  │                    │                                   │ │
│  │         ┌──────────┴───────────┐                       │ │
│  │         │                      │                       │ │
│  │         ▼                      ▼                       │ │
│  │  ┌──────────────┐        ┌─────────────┐               │ │
│  │  │arena-database│        │ arena-cache │               │ │
│  │  │              │        │             │               │ │
│  │  │ PostgreSQL   │        │   Redis     │               │ │
│  │  │ Port: 5432   │        │ Port: 6379  │               │ │
│  │  └──────┬───────┘        └──────┬──────┘               │ │
│  │         │                       │                      │ │
│  └─────────┼───────────────────────┼──────────────────────┘ │
│            │                       │                        │
│            ▼                       ▼                        │
│    arena-db-data           arena-cache-data                 │
│    Docker Volume           Docker Volume                    │
│    (Persistente)           (Persistente)                    │
└─────────────────────────────────────────────────────────────┘

```

### Fluxo de Comunicação

**1. Inicialização (com depends_on):**
```
1. Docker Compose inicia
2. Cria rede arena-network
3. Inicia arena-database (health check ativo)
4. Inicia arena-cache (health check ativo)
5. Aguarda ambos ficarem "healthy"
6. Inicia battle-arena
7. API conecta aos serviços
```

**2. Requisição de Listagem de Heróis:**
```
Cliente → API (/heroes) → PostgreSQL → API → Cliente
```

**3. Requisição de Ranking (com cache):**
```
Cliente → API (/ranking) → Redis (hit) → API → Cliente
                      ou
Cliente → API (/ranking) → Redis (miss) → PostgreSQL → Redis (save) → API → Cliente
```

**4. Criação de Batalha (integração completa):**
```
Cliente → API (/battle POST)
       ↓
    PostgreSQL (busca heróis)
       ↓
    API (simula batalha)
       ↓
    PostgreSQL (salva resultado)
       ↓
    Redis (invalida cache)
       ↓
    Cliente ← API (retorna resultado)
```

## 📁 Estrutura do Projeto

```
desafio3/
├── database/                   # Serviço Database
│   ├── Dockerfile                # PostgreSQL 16
│   └── init.sql                  # Schema e dados iniciais
│
├── web/                        # Serviço Web/API
│   ├── Dockerfile                # Flask + psycopg2 + redis
│   ├── app.py                    # API REST completa
│   └── requirements.txt          # Dependências Python
│
├── docker-compose.yml          # ORQUESTRAÇÃO DOS 3 SERVIÇOS
├── start.sh                    # Script para iniciar tudo
├── test-services.sh            # Script de teste de comunicação
├── battle-demo.sh              # Demonstração de batalhas
├── .gitignore                  # Arquivos a ignorar
└── README.md                   # Esta documentação
```

## 🎮 Demonstração do Sistema

### 1. Iniciando a Arena

```bash
$ ./start.sh

============================================================
⚔️ INICIANDO ARENA DE BATALHAS - Desafio de Orquestração
============================================================

✅ Docker está rodando

🔨 Construindo imagens Docker...
[+] Building 25.3s

🚀 Iniciando todos os serviços...
✅ Container arena-database criado
✅ Container arena-cache criado
✅ Container battle-arena criado

📊 STATUS DOS SERVIÇOS:
NAME            STATUS                  PORTS
arena-database  Up (healthy)           5432/tcp
arena-cache     Up (healthy)           6379/tcp
battle-arena    Up (healthy)           0.0.0.0:5000->5000/tcp
```

### 2. Testando Comunicação

```bash
$ curl http://localhost:5000/health | python3 -m json.tool

{
    "api": "healthy",
    "database": "healthy",
    "cache": "healthy",
    "timestamp": "2025-11-13T20:30:45.123456"
}
```

### 3. Listando Heróis (API → Database)

```bash
$ curl http://localhost:5000/heroes

{
    "total": 8,
    "heroes": [
        {
            "id": 1,
            "name": "Dragão Vermelho",
            "class": "Monstro",
            "level": 50,
            "attack_power": 95,
            "defense_power": 80,
            "health_points": 500,
            "wins": 0,
            "losses": 0,
            "draws": 0
        },
        ...
    ]
}
```

### 4. Criando Batalha (Integração Completa)

```bash
$ curl -X POST http://localhost:5000/battle \
  -H "Content-Type: application/json" \
  -d '{"hero1_id": 1, "hero2_id": 2}'

{
    "battle_id": 1,
    "result": {
        "winner_id": 1,
        "hero1_damage": 245,
        "hero2_damage": 198,
        "rounds": 8,
        "log": "⚔️ Dragão Vermelho VS Cavaleiro Sagrado\n...\n🏆 VENCEDOR: Dragão Vermelho!"
    }
}
```

### 5. Ranking (API → Cache → Database)

```bash
$ curl http://localhost:5000/ranking

{
    "source": "database",  // Primeira chamada
    "ranking": [
        {
            "name": "Dragão Vermelho",
            "class": "Monstro",
            "level": 50,
            "wins": 1,
            "losses": 0,
            "win_rate": 100.00,
            "ranking_points": 3
        },
        ...
    ]
}

# Segunda chamada (mesma requisição):
{
    "source": "cache",  // Agora vem do Redis!
    "cached_at": "2025-11-13T20:31:00",
    "ranking": [...]
}
```

## 🔍 Detalhes Técnicos

### 🎯 Depends_on com Conditions

No `docker-compose.yml`, a API depende de ambos os serviços:

```yaml
battle-arena:
  depends_on:
    arena-database:
      condition: service_healthy
    arena-cache:
      condition: service_healthy
```

**Por que isso é importante:**
- Garante ordem correta de inicialização
- API não tenta conectar antes dos serviços estarem prontos
- Health checks garantem que serviços estão realmente funcionais
- Evita race conditions e erros de conexão

### 🌐 Rede Interna

Todos os serviços estão na mesma rede:

```yaml
networks:
  arena-network:
    name: arena-network
    driver: bridge
    ipam:
      config:
        - subnet: 172.25.0.0/16
```

**Benefícios:**
- Comunicação via DNS interno (nomes dos serviços)
- Isolamento de outras redes Docker
- Subnet customizado para melhor controle
- Todos os containers podem se comunicar

### 🔧 Variáveis de Ambiente

**Database:**
```yaml
environment:
  POSTGRES_DB: battle_arena
  POSTGRES_USER: arena_master
  POSTGRES_PASSWORD: battle123
```

**API (em app.py):**
```python
DB_CONFIG = {
    'host': 'arena-database',  
    'port': '5432',
    'dbname': 'battle_arena',
    'user': 'arena_master',
    'password': 'battle123'
}

REDIS_CONFIG = {
    'host': 'arena-cache',  
    'port': 6379
}
```

### 💾 Volumes e Persistência

Dois volumes são criados:

```yaml
volumes:
  arena-db-data:
    name: arena-db-data
    driver: local
  arena-cache-data:
    name: arena-cache-data
    driver: local
```

- **arena-db-data**: Dados do PostgreSQL (heróis, batalhas)
- **arena-cache-data**: Dados do Redis (com AOF habilitado)

### 🏥 Health Checks

Cada serviço tem seu health check:

**Database:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U arena_master -d battle_arena"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**Cache:**
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**API:**
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:5000/health')"]
  interval: 30s
  timeout: 10s
  retries: 3
```