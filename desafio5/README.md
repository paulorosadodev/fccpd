# 🚪 API Gateway: Desafio de Orquestração de Microsserviços

Este projeto demonstra uma arquitetura com **API Gateway** como ponto único de entrada para dois microsserviços independentes! O Gateway centraliza o acesso, faz proxy para os serviços e orquestra chamadas combinadas, enquanto os microsserviços permanecem isolados e não expostos externamente.

## 🎯 Objetivo

Demonstrar arquitetura de API Gateway com microsserviços:
- 🚪 **API Gateway**: Ponto único de entrada (porta 8000)
- 👤 **Microsserviço 1 (Player Service)**: Gerencia dados de jogadores
- ⚔️ **Microsserviço 2 (Item Service)**: Gerencia dados de itens/equipamentos
- 🔗 **Orquestração**: Gateway combina dados de múltiplos serviços
- 🐳 **Isolamento**: Microsserviços não expostos externamente (apenas Gateway)

## ▶️ Como rodar o desafio:

```bash
# Tornar scripts executáveis (primeira vez)
chmod +x start.sh test-gateway.sh

# Iniciar Gateway e Microsserviços
./start.sh
```

O script `start.sh` irá:
1. Construir as 3 imagens Docker (Gateway + 2 Microsserviços)
2. Criar rede customizada gateway-network
3. Iniciar Player Service e Item Service com health checks
4. Iniciar API Gateway apenas após ambos estarem saudáveis
5. Mostrar status e endpoints disponíveis

### 🧪 Testar API Gateway

Para **comprovar que o Gateway funciona como ponto único de entrada**:

```bash
# Execute o script de teste automatizado
./test-gateway.sh
```

**O que esse script faz:**
1. ✅ Health check do Gateway (verifica todos os serviços)
2. 👤 Gateway faz proxy para Player Service
3. ⚔️ Gateway faz proxy para Item Service
4. 🔗 Gateway orquestra múltiplos serviços (combina Player + Item)
5. 📊 Demonstra estatísticas agregadas
6. 🎯 Mostra isolamento (microsserviços não acessíveis externamente)

## ✅ Requisitos Atendidos + Sistema RPG

### ✓ Microsserviço 1 - Player Service

**Responsabilidade:** Gerenciar dados de jogadores

- **Porta Interna:** 8002 (não exposta externamente)
- **Endpoints:**
  - `GET /players` - Lista todos os jogadores
  - `GET /players/<id>` - Detalhes de um jogador
  - `GET /players/<id>/stats` - Estatísticas de um jogador
  - `GET /health` - Health check

- **Dados Fornecidos:**
  - 6 jogadores pré-configurados
  - Informações: username, email, level, class, gold, guild
  - Status online/offline

### ✓ Microsserviço 2 - Item Service

**Responsabilidade:** Gerenciar dados de itens e equipamentos

- **Porta Interna:** 8003 (não exposta externamente)
- **Endpoints:**
  - `GET /items` - Lista todos os itens
  - `GET /items/<id>` - Detalhes de um item
  - `GET /items/player/<player_id>` - Itens de um jogador
  - `GET /items/type/<type>` - Itens por tipo
  - `GET /health` - Health check

- **Dados Fornecidos:**
  - 10 itens pré-configurados
  - Informações: name, type, rarity, power, price, owner
  - Status: equipped/inventory

### ✓ API Gateway

**Responsabilidade:** Ponto único de entrada e orquestração

- **Porta Externa:** 8000 (única porta exposta)
- **Funcionalidades:**
  - **Proxy**: Encaminha requisições aos microsserviços
  - **Orquestração**: Combina dados de múltiplos serviços
  - **Agregação**: Estatísticas combinadas
  - **Health Check**: Verifica saúde de todos os serviços

- **Endpoints Expostos:**
  - `GET /players` → Proxy para Player Service
  - `GET /players/<id>` → Proxy para Player Service
  - `GET /items` → Proxy para Item Service
  - `GET /items/<id>` → Proxy para Item Service
  - `GET /players/<id>/items` → **Orquestra** Player + Item Service
  - `GET /stats` → **Agrega** dados de ambos os serviços
  - `GET /health` → Verifica todos os serviços

### ✓ Isolamento e Segurança

- **Microsserviços isolados**: Portas 8002 e 8003 não mapeadas no host
- **Gateway único ponto de entrada**: Apenas porta 8000 exposta
- **Cliente não conhece microsserviços**: Só precisa do Gateway
- **Rede interna**: Comunicação via DNS interno do Docker

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                      Host Machine                           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │    Docker Network: gateway-network                    │  │
│  │              (172.35.0.0/16)                          │  │
│  │                                                       │  │
│  │                                                       │  │
│  │  ┌──────────────────────┐                             │  │
│  │  │   api-gateway        │                             │  │
│  │  │   Port: 8000         ◄─────── Cliente              │  │
│  │  │   (ÚNICO PONTO       │     (porta 8000)            │  │
│  │  │    DE ENTRADA)       │                             │  │
│  │  └──────────┬───────────┘                             │  │
│  │             │                                         │  │
│  │             │ HTTP Proxy                              │  │
│  │             │                                         │  │
│  │    ┌────────┴────────┐                                │  │
│  │    │                 │                                │  │
│  │    ▼                 ▼                                │  │
│  │  ┌──────────┐    ┌──────────┐                         │  │
│  │  │player-   │    │item-     │                         │  │
│  │  │service   │    │service   │                         │  │ 
│  │  │          │    │          │                         │  │
│  │  │Port:8002 │    │Port:8003 │                         │  │ 
│  │  │(INTERNO) │    │(INTERNO) │                         │  │
│  │  └──────────┘    └──────────┘                         │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ❌ Portas 8002 e 8003 NÃO estão expostas!                  │
│  ✅ Apenas Gateway (8000) é acessível externamente          │
└─────────────────────────────────────────────────────────────┘

Fluxo de Requisição:
Cliente → GET http://localhost:8000/players/1/items
       ↓
    API Gateway recebe requisição
       ↓
    Gateway → GET http://player-service:8002/players/1
       ↓
    Player Service retorna dados do jogador
       ↓
    Gateway → GET http://item-service:8003/items/player/1
       ↓
    Item Service retorna itens do jogador
       ↓
    Gateway combina dados e retorna ao cliente
       ↓
    Cliente ← JSON com player + items combinados
```

### Fluxo de Comunicação Detalhado

**1. Requisição Simples (Proxy):**
```
Cliente → GET http://localhost:8000/players
       ↓
    Gateway recebe
       ↓
    Gateway → GET http://player-service:8002/players
       ↓
    Player Service responde
       ↓
    Gateway → Cliente (com timestamp do gateway)
```

**2. Requisição Orquestrada:**
```
Cliente → GET http://localhost:8000/players/1/items
       ↓
    Gateway recebe
       ↓
    Gateway → Player Service (/players/1)
       ↓
    Gateway → Item Service (/items/player/1)
       ↓
    Gateway combina ambos os resultados
       ↓
    Gateway → Cliente (JSON combinado)
```

**3. Agregação de Dados:**
```
Cliente → GET http://localhost:8000/stats
       ↓
    Gateway recebe
       ↓
    Gateway → Player Service (/players)
       ↓
    Gateway → Item Service (/items)
       ↓
    Gateway calcula estatísticas agregadas
       ↓
    Gateway → Cliente (stats combinadas)
```

## 📁 Estrutura do Projeto

```
desafio5/
├── player-service/            # Microsserviço 1
│   ├── Dockerfile               # Dockerfile do Player Service
│   ├── app.py                   # API Flask (dados de jogadores)
│   └── requirements.txt         # Dependências (Flask)
│
├── item-service/              # Microsserviço 2
│   ├── Dockerfile               # Dockerfile do Item Service
│   ├── app.py                   # API Flask (dados de itens)
│   └── requirements.txt         # Dependências (Flask)
│
├── api-gateway/               # API Gateway
│   ├── Dockerfile               # Dockerfile do Gateway
│   ├── app.py                   # Gateway Flask (orquestra serviços)
│   └── requirements.txt         # Dependências (Flask + requests)
│
├── docker-compose.yml         # Orquestração dos 3 serviços
├── start.sh                  # Script para iniciar
├── test-gateway.sh           # Script de teste do Gateway
├── .gitignore                # Arquivos a ignorar
└── README.md                 # Esta documentação
```

## 🎮 Demonstração do Sistema

### 1. Iniciando o Gateway e Microsserviços

```bash
$ ./start.sh

============================================================
🚪 INICIANDO API GATEWAY E MICROSSERVIÇOS
============================================================

✅ Docker está rodando

🔨 Construindo imagens Docker...
[+] Building 20.5s

🚀 Iniciando todos os serviços...
✅ Container player-service criado
✅ Container item-service criado
✅ Container api-gateway criado

📊 STATUS DOS SERVIÇOS:
NAME            STATUS                  PORTS
player-service  Up (healthy)           8002/tcp
item-service    Up (healthy)           8003/tcp
api-gateway     Up (healthy)           0.0.0.0:8000->8000/tcp
```

### 2. Health Check do Gateway

```bash
$ curl http://localhost:8000/health | python3 -m json.tool

{
    "all_services_healthy": true,
    "gateway": "healthy",
    "item_service": "healthy",
    "player_service": "healthy",
    "timestamp": "2025-11-14T18:00:00"
}
```

### 3. Gateway Faz Proxy para Player Service

```bash
$ curl http://localhost:8000/players | python3 -m json.tool

{
    "source": "player-service",
    "gateway_timestamp": "2025-11-14T18:00:00",
    "total": 6,
    "players": [
        {
            "id": 1,
            "username": "DragonSlayer99",
            "level": 45,
            "class": "Guerreiro",
            "gold": 50000,
            ...
        },
        ...
    ]
}
```

### 4. Gateway Faz Proxy para Item Service

```bash
$ curl http://localhost:8000/items | python3 -m json.tool

{
    "source": "item-service",
    "gateway_timestamp": "2025-11-14T18:00:00",
    "total": 10,
    "items": [
        {
            "id": 1,
            "name": "Espada Lendária do Dragão",
            "type": "Arma",
            "rarity": "Lendária",
            "power": 95,
            "price": 50000,
            ...
        },
        ...
    ]
}
```

### 5. Gateway Orquestra Múltiplos Serviços

```bash
$ curl http://localhost:8000/players/1/items | python3 -m json.tool

{
    "orchestrated_by": "api-gateway",
    "gateway_timestamp": "2025-11-14T18:00:00",
    "player": {
        "id": 1,
        "username": "DragonSlayer99",
        "level": 45,
        "class": "Guerreiro",
        "gold": 50000,
        ...
    },
    "items": [
        {
            "id": 1,
            "name": "Espada Lendária do Dragão",
            "type": "Arma",
            "power": 95,
            "status": "equipped"
        },
        {
            "id": 4,
            "name": "Armadura de Mithril",
            "type": "Armadura",
            "power": 82,
            "status": "equipped"
        }
    ],
    "total_items": 2
}
```

### 6. Estatísticas Agregadas

```bash
$ curl http://localhost:8000/stats | python3 -m json.tool

{
    "generated_at": "2025-11-14T18:00:00",
    "summary": {
        "players": {
            "total": 6,
            "online": 5,
            "offline": 1,
            "total_gold": 312000,
            "average_level": 44.67
        },
        "items": {
            "total": 10,
            "total_value": 403500,
            "rarity_distribution": {
                "Lendária": 3,
                "Épica": 3,
                "Rara": 3,
                "Comum": 1
            }
        }
    }
}
```

## 🔍 Detalhes Técnicos

### 🚪 Funcionamento do Gateway

**Proxy Simples:**
```python
@app.route('/players')
def get_players():
    result = call_service(PLAYER_SERVICE_URL, '/players')
    return jsonify({
        'source': 'player-service',
        'gateway_timestamp': datetime.now().isoformat(),
        **result
    }), 200
```

**Orquestração:**
```python
@app.route('/players/<int:player_id>/items')
def get_player_with_items(player_id):
    # Chama Player Service
    player_result = call_service(PLAYER_SERVICE_URL, f'/players/{player_id}')
    
    # Chama Item Service
    items_result = call_service(ITEM_SERVICE_URL, f'/items/player/{player_id}')
    
    # Combina resultados
    return jsonify({
        'player': player_result,
        'items': items_result.get('items', []),
        'orchestrated_by': 'api-gateway'
    }), 200
```

### 🐳 Isolamento de Portas

**docker-compose.yml:**
```yaml
player-service:
  # NÃO tem "ports:" - não exposto externamente!
  networks:
    - gateway-network

item-service:
  # NÃO tem "ports:" - não exposto externamente!
  networks:
    - gateway-network

api-gateway:
  ports:
    - "8000:8000"  # ÚNICA porta exposta!
  depends_on:
    player-service:
      condition: service_healthy
    item-service:
      condition: service_healthy
```

**Benefícios:**
- Cliente só conhece porta 8000 (Gateway)
- Microsserviços protegidos (não acessíveis externamente)
- Segurança adicional (firewall interno)
- Facilita mudanças internas sem afetar clientes

### 🌐 Rede e DNS

```yaml
networks:
  gateway-network:
    name: gateway-network
    driver: bridge
    ipam:
      config:
        - subnet: 172.35.0.0/16
```

**Comunicação:**
- Todos na mesma rede interna
- DNS automático: `player-service` e `item-service`
- Gateway acessa via hostnames internos
- Cliente não precisa conhecer estrutura interna

### 📦 Depends_on e Health Checks

```yaml
api-gateway:
  depends_on:
    player-service:
      condition: service_healthy
    item-service:
      condition: service_healthy
```

**Garante:**
- Gateway só inicia após ambos estarem prontos
- Health checks verificam disponibilidade real
- Evita erros de conexão na inicialização
- Ordem correta de startup

### 🔄 Tratamento de Erros

```python
def call_service(service_url, endpoint, method='GET', data=None):
    try:
        response = requests.get(f'{service_url}{endpoint}', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao conectar: {str(e)}'}
```

**Características:**
- Timeout de 5 segundos
- Tratamento de erros de rede
- Retorno de erros estruturados
- Gateway não quebra se um serviço falhar
