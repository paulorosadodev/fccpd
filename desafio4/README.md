# 🏰 Microsserviços de Guildas: Desafio de Comunicação HTTP

Este projeto demonstra comunicação entre microsserviços independentes através de requisições HTTP! Dois serviços trabalham em conjunto: **Guild Service** fornece dados de guildas e membros, enquanto **Guild Reporter** consome esses dados e gera relatórios combinados e análises detalhadas.

## 🎯 Objetivo

Demonstrar arquitetura de microsserviços com comunicação HTTP:
- 🏰 **Microsserviço A (Guild Service)**: API REST que retorna lista de guildas e membros
- 📊 **Microsserviço B (Guild Reporter)**: Consome o serviço A via HTTP e gera relatórios
- 🐳 **Dockerfiles Separados**: Cada serviço tem seu próprio Dockerfile
- 🔗 **Comunicação HTTP**: Requisições REST entre serviços sem gateway
- 🌐 **Isolamento**: Serviços independentes e desacoplados

## ▶️ Como rodar o desafio:

```bash
# Tornar scripts executáveis (primeira vez)
chmod +x start.sh test-communication.sh

# Iniciar ambos os microsserviços
./start.sh
```

O script `start.sh` irá:
1. Construir as imagens Docker de ambos os serviços
2. Criar rede customizada para comunicação
3. Iniciar Guild Service primeiro
4. Iniciar Guild Reporter após o Service estar saudável
5. Mostrar status e endpoints disponíveis

### 🧪 Testar Comunicação Entre Microsserviços

Para **comprovar que os serviços estão se comunicando via HTTP**:

```bash
# Execute o script de teste automatizado
./test-communication.sh
```

**O que esse script faz:**
1. ✅ Health check de ambos os serviços
2. 🏰 Testa Guild Service diretamente (retorna dados originais)
3. 📊 Testa Guild Reporter consumindo o Service (combina dados)
4. 📈 Demonstra relatórios detalhados e resumos
5. ⚡ Mostra análise de atividade processada

## ✅ Requisitos Atendidos + Sistema RPG

### ✓ Microsserviço A - Guild Service

**Responsabilidade:** Fornecer dados de guildas e membros

- **Porta:** 8000
- **Endpoints:**
  - `GET /` - Informações do serviço
  - `GET /guilds` - Lista todas as guildas
  - `GET /guilds/<id>` - Detalhes de uma guilda
  - `GET /guilds/<id>/members` - Membros de uma guilda
  - `GET /guilds/<id>/stats` - Estatísticas de uma guilda
  - `GET /health` - Health check

- **Dados Fornecidos:**
  - 5 guildas pré-configuradas
  - Informações de membros, níveis, classes
  - Estatísticas de guildas (nível, reputação, quests)

### ✓ Microsserviço B - Guild Reporter

**Responsabilidade:** Consumir Guild Service e gerar relatórios

- **Porta:** 8001
- **Comunicação:** Faz requisições HTTP ao `guild-service:8000`
- **Endpoints:**
  - `GET /` - Informações do serviço
  - `GET /report` - Relatório completo de todas as guildas
  - `GET /report/<id>` - Relatório detalhado de uma guilda
  - `GET /summary` - Resumo executivo agregado
  - `GET /activity` - Análise de atividade processada
  - `GET /health` - Health check (verifica também o Service)

- **Processamento:**
  - Calcula dias ativos desde fundação
  - Agrega estatísticas de membros
  - Gera métricas de atividade
  - Combina dados em formatos úteis

### ✓ Dockerfiles Separados

Cada microsserviço tem seu próprio Dockerfile:
- `guild-service/Dockerfile` - Imagem Python com Flask
- `guild-reporter/Dockerfile` - Imagem Python com Flask + requests

**Isolamento:**
- Dependências independentes
- Builds separados
- Containers isolados
- Portas diferentes

### ✓ Comunicação HTTP

**Sem Gateway:**
- Comunicação direta via HTTP
- Reporter faz `requests.get()` ao Service
- DNS interno do Docker (`guild-service:8000`)
- Timeout e tratamento de erros

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                      Host Machine                           │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │    Docker Network: microservices-network               │ │
│  │              (172.30.0.0/16)                           │ │
│  │                                                        │ │
│  │                                                        │ │
│  │  ┌──────────────────────┐                              │ │
│  │  │   guild-service      │                              │ │
│  │  │   (Microsserviço A)  │                              │ │
│  │  │   Port: 8000         │                              │ │
│  │  │   Flask API          │                              │ │
│  │  │                      │                              │ │
│  │  │   • /guilds          │                              │ │
│  │  │   • /guilds/<id>     │                              │ │
│  │  │   • /health          │                              │ │
│  │  └──────────┬───────────┘                              │ │
│  │             │                                          │ │
│  │             │ HTTP GET                                 │ │
│  │             │ requests.get()                           │ │
│  │             │                                          │ │
│  │             ▼                                          │ │
│  │  ┌──────────────────────┐                              │ │
│  │  │  guild-reporter      │                              │ │
│  │  │  (Microsserviço B)   │                              │ │
│  │  │  Port: 8001          │                              │ │
│  │  │  Flask API           │                              │ │
│  │  │                      │                              │ │
│  │  │   • /report          │                              │ │
│  │  │   • /summary         │                              │ │
│  │  │   • /activity        │                              │ │
│  │  │   • /health          │                              │ │
│  │  └──────────────────────┘                              │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  Cliente HTTP                                               │
│  ↓                                                          │
│  localhost:8000 (Guild Service)                             │
│  localhost:8001 (Guild Reporter)                            │
└─────────────────────────────────────────────────────────────┘

Fluxo de Comunicação:
Cliente → Guild Reporter (/report)
       ↓
    HTTP GET → guild-service:8000/guilds
       ↓
    Guild Service retorna JSON
       ↓
    Guild Reporter processa e combina dados
       ↓
    Cliente ← Relatório formatado
```

### Fluxo de Comunicação Detalhado

**1. Requisição ao Reporter:**
```
Cliente → GET http://localhost:8001/report
```

**2. Reporter consome Service:**
```python
# No código do Reporter (app.py)
response = requests.get('http://guild-service:8000/guilds')
guilds_data = response.json()
```

**3. Processamento:**
- Reporter recebe dados JSON do Service
- Calcula métricas (dias ativos, médias, etc.)
- Combina informações de múltiplas guildas
- Formata relatório estruturado

**4. Resposta ao Cliente:**
```
Cliente ← JSON com relatório combinado
```

## 📁 Estrutura do Projeto

```
desafio4/
├── guild-service/              # Microsserviço A
│   ├── Dockerfile                # Dockerfile do Service
│   ├── app.py                    # API Flask (fornece dados)
│   └── requirements.txt          # Dependências (Flask)
│
├── guild-reporter/            # Microsserviço B
│   ├── Dockerfile                # Dockerfile do Reporter
│   ├── app.py                    # API Flask (consome e processa)
│   └── requirements.txt          # Dependências (Flask + requests)
│
├── docker-compose.yml         # Orquestração dos 2 serviços
├── start.sh                   # Script para iniciar
├── test-communication.sh      # Script de teste de comunicação
├── .gitignore                # Arquivos a ignorar
└── README.md                  # Esta documentação
```

## 🎮 Demonstração do Sistema

### 1. Iniciando os Microsserviços

```bash
$ ./start.sh

============================================================
🏰 INICIANDO MICROSSERVIÇOS DE GUILDAS
============================================================

✅ Docker está rodando

🔨 Construindo imagens Docker...
[+] Building 15.2s

🚀 Iniciando microsserviços...
✅ Container guild-service criado
✅ Container guild-reporter criado

📊 STATUS DOS SERVIÇOS:
NAME              STATUS                  PORTS
guild-service     Up (healthy)           0.0.0.0:8000->8000/tcp
guild-reporter    Up (healthy)           0.0.0.0:8001->8001/tcp
```

### 2. Microsserviço A - Dados Originais

```bash
$ curl http://localhost:8000/guilds | python3 -m json.tool

{
    "total": 5,
    "guilds": [
        {
            "id": 1,
            "name": "Ordem dos Cavaleiros Sagrados",
            "founded_date": "2020-01-15",
            "members": [
                {
                    "id": 101,
                    "name": "Sir Lancelot",
                    "class": "Paladino",
                    "level": 45,
                    "joined_date": "2020-01-20"
                },
                ...
            ],
            "guild_level": 85,
            "total_quests_completed": 1247,
            "reputation": "Lendária"
        },
        ...
    ]
}
```

### 3. Microsserviço B - Consumindo e Processando

```bash
$ curl http://localhost:8001/report | python3 -m json.tool

{
    "generated_at": "2025-11-13T21:00:00",
    "total_guilds": 5,
    "guilds_report": [
        {
            "guild_id": 1,
            "guild_name": "Ordem dos Cavaleiros Sagrados",
            "status": "Ativa há 1800 dias",  ← Calculado pelo Reporter!
            "founded_date": "2020-01-15",
            "days_active": 1800,
            "members_summary": {
                "total": 4,
                "average_level": 41.25,      ← Processado pelo Reporter!
                "highest_level": 45,
                "lowest_level": 38
            },
            "guild_stats": {
                "level": 85,
                "reputation": "Lendária",
                "quests_completed": 1247,
                "quests_per_member": 311.75   ← Métrica calculada!
            },
            "members": [
                {
                    "name": "Sir Lancelot",
                    "class": "Paladino",
                    "level": 45,
                    "status": "Membro há 1795 dias",  ← Processado!
                    "joined_date": "2020-01-20",
                    "days_as_member": 1795
                },
                ...
            ]
        },
        ...
    ]
}
```

### 4. Resumo Executivo (Agregação)

```bash
$ curl http://localhost:8001/summary

{
    "generated_at": "2025-11-13T21:00:00",
    "overview": {
        "total_guilds": 5,
        "total_members": 22,              ← Agregado de todas as guildas
        "average_members_per_guild": 4.4,
        "total_quests_completed": 8752,   ← Soma de todas
        "average_guild_level": 87.6       ← Média calculada
    },
    "reputation_distribution": {
        "Lendária": 2,
        "Mítica": 2,
        "Épica": 1
    },
    "top_guilds": {
        "by_level": [...],
        "by_quests": [...]
    }
}
```

## 🔍 Detalhes Técnicos

### 🔗 Comunicação HTTP

**No Guild Reporter (app.py):**

```python
def get_guild_service_data(endpoint):
    """Faz requisição HTTP ao Guild Service"""
    try:
        response = requests.get(
            f'http://guild-service:8000{endpoint}',
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao conectar: {str(e)}'}
```

**Características:**
- **DNS Interno**: `guild-service` resolve para IP do container
- **Timeout**: 5 segundos para evitar travamentos
- **Error Handling**: Tratamento de erros de conexão
- **JSON**: Resposta automaticamente parseada

### 🐳 Dockerfiles Separados

**Guild Service Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]
```

**Guild Reporter Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # Inclui requests!
COPY app.py .
EXPOSE 8001
CMD ["python", "app.py"]
```

**Isolamento:**
- Dependências diferentes (Reporter precisa de `requests`)
- Builds independentes
- Containers separados
- Portas diferentes

### 🌐 Rede e DNS

```yaml
networks:
  microservices-network:
    name: microservices-network
    driver: bridge
    ipam:
      config:
        - subnet: 172.30.0.0/16
```

**Comunicação:**
- Ambos na mesma rede
- DNS automático: `guild-service` → IP do container
- Comunicação interna (não exposta externamente)
- Portas expostas apenas para acesso do host

### 📦 Dependências e Ordem

```yaml
guild-reporter:
  depends_on:
    guild-service:
      condition: service_healthy
```

**Garante:**
- Guild Service inicia primeiro
- Reporter só inicia após Service estar saudável
- Evita erros de conexão na inicialização
- Health checks verificam disponibilidade real

### 🔄 Processamento de Dados

**Reporter processa dados do Service:**

1. **Cálculo de Dias Ativos:**
```python
founded_date = parser.parse(guild['founded_date'])
days_active = (datetime.now() - founded_date).days
```

2. **Agregação de Estatísticas:**
```python
total_levels = sum(m['level'] for m in guild['members'])
avg_level = total_levels / total_members
```

3. **Métricas Combinadas:**
```python
quests_per_member = total_quests / total_members
activity_score = (quests / days_active) * (level / 100)
```