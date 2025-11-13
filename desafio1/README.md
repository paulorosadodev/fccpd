# 🎮 RPG das Requisições HTTP: Desafio Docker 

Este projeto transforma a comunicação entre containers Docker em um **RPG épico**! Um container executa um servidor de jogo Flask que recompensa cada requisição com XP, enquanto outro container (o jogador) faz requisições periódicas para ganhar experiência, subir de nível e conquistar títulos lendários!

## 🎯 Objetivo

Criar uma experiência gamificada de aprendizado Docker onde:
- 🎮 **Sistema de RPG**: Cada requisição ganha XP (15-30 pontos)
- ⚡ **Critical Hits**: 10% de chance de ganhar XP em dobro!
- 🏆 **Sistema de Níveis**: 100 XP = 1 nível
- 👑 **Títulos Épicos**: 11 títulos diferentes de "Novato" até "Entidade Cósmica"
- 🌐 **Comunicação Docker**: Tudo funciona via rede customizada
- 📊 **Estatísticas em tempo real**: Acompanhe seu progresso!

## ▶️ Como rodar o desafio: 

```bash
# Tornar scripts executáveis 
chmod +x start.sh

# Iniciar o ambiente
./start.sh
```
O script `start.sh` irá:
1. Verificar se Docker está rodando
2. Limpar containers anteriores
3. Construir as imagens
4. Iniciar os containers
5. Exibir status e informações da rede
6. Mostrar logs em tempo real

## ✅ Requisitos Atendidos + Sistema de Jogo

### ✓ Servidor Web de Jogo (Porta 8080)
- Container `web-server` executa um **RPG Game Server** em Flask
- Sistema completo de progressão: XP, Níveis e Títulos
- Três endpoints disponíveis:
  - `/` - **Faça uma requisição e ganhe XP!** Retorna stats do jogador e recompensa
  - `/health` - Health check do servidor de jogo
  - `/stats` - Estatísticas completas com barra de progresso

### ✓ Cliente Jogador (Requisições Periódicas)
- Container `http-client` é o **jogador automático**
- Faz requisições a cada 5 segundos para ganhar XP
- Mostra em tempo real: XP ganho, níveis, títulos e critical hits
- Logs coloridos e animados com emojis épicos

### ✓ Rede Docker Customizada
- Rede nomeada `desafio-network` com driver bridge
- Subnet customizado: `172.20.0.0/16`
- Comunicação segura e isolada entre game server e player
- DNS automático para resolução de nomes

### ✓ Sistema de Progressão RPG
- **XP por Requisição**: 15-30 XP base
- **Critical Hits**: 10% de chance de XP em dobro (💥)
- **Níveis**: A cada 100 XP você sobe 1 nível
- **11 Títulos Épicos**:
  - Nv 1: 🌱 Novato das Requisições
  - Nv 5: ⚔️ Guerreiro HTTP
  - Nv 10: 🛡️ Guardião dos Endpoints
  - Nv 15: 🔥 Mestre do Curl
  - Nv 20: ⚡ Senhor das APIs
  - Nv 25: 🌟 Lendário Docker
  - Nv 30: 👑 Rei das Requisições
  - Nv 40: 🏆 Campeão dos Containers
  - Nv 50: 💎 Deus das Conexões
  - Nv 75: 🌌 Transcendente Digital
  - Nv 100: ∞ Entidade Cósmica da Rede

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                    Host Machine                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Docker Network: desafio-network           │  │
│  │              (172.20.0.0/16)                      │  │
│  │                                                   │  │
│  │  ┌──────────────────┐      ┌──────────────────┐   │  │
│  │  │   web-server     │      │   http-client    │   │  │
│  │  │                  │      │                  │   │  │
│  │  │  Flask App       │◄─────│  curl loop       │   │  │
│  │  │  Port: 8080      │ HTTP │  Every 5s        │   │  │
│  │  │                  │      │                  │   │  │
│  │  └────────┬─────────┘      └──────────────────┘   │  │
│  │           │                                       │  │
│  └───────────┼───────────────────────────────────────┘  │
│              │                                          │
│         Port 8080                                       │
│              ▼                                          │
│      localhost:8080                                     │
└─────────────────────────────────────────────────────────┘
```

### Fluxo de Comunicação

1. **Inicialização**: 
   - Docker cria a rede customizada `desafio-network`
   - Container `web-server` inicia primeiro (healthcheck ativo)
   - Container `http-client` aguarda servidor estar saudável

2. **Comunicação**:
   - Cliente faz requisição HTTP para `http://web-server:8080`
   - DNS do Docker resolve `web-server` para IP do container
   - Servidor processa requisição e retorna JSON
   - Ambos registram logs da transação

3. **Loop Contínuo**:
   - Cliente aguarda 5 segundos
   - Processo se repete indefinidamente

## 📁 Estrutura do Projeto

```
desafio1/
├── server/                     # Servidor Web Flask
│   ├── Dockerfile                # Imagem Docker do servidor
│   ├── app.py                    # Aplicação Flask
│   └── requirements.txt          # Dependências Python
│
├── client/                     # Cliente HTTP
│   ├── Dockerfile                # Imagem Docker do cliente
│   └── request.sh                # Script de requisições
│
├── docker-compose.yml          # Orquestração dos containers
├── start.sh                    # Script para iniciar ambiente
├── .gitignore                  # Arquivos a ignorar no Git
└── README.md                   # Esta documentação
```

## 🎮 Demonstração do Jogo em Ação

### Logs do Game Server (web-server)

```
============================================================
🎮 RPG DAS REQUISIÇÕES HTTP - SERVIDOR DE JOGO INICIADO!
============================================================
🏰 Bem-vindo ao mundo das requisições HTTP!
⚔️  Cada requisição ganha XP e aumenta seu nível
🏆 Conquiste títulos épicos conforme progride
💎 10% de chance de CRITICAL HIT (XP em dobro)!
============================================================
🚀 Servidor rodando na porta 8080...
============================================================

[2025-11-13 10:15:01] 🎮 Requisição #1 de 172.20.0.3 | ⚔️ +25 XP | Level 1 (25/100 XP)
[2025-11-13 10:15:06] 🎮 Requisição #2 de 172.20.0.3 | 💥 CRITICAL HIT! +60 XP | Level 1 (85/100 XP)
[2025-11-13 10:15:11] 🎮 Requisição #3 de 172.20.0.3 | ⚔️ +18 XP | 🎊 LEVEL UP! 1 → 2 | 🌱 Novato das Requisições
[2025-11-13 10:15:16] 🎮 Requisição #4 de 172.20.0.3 | ⚔️ +22 XP | Level 2 (25/100 XP)
```

### Logs do Cliente Jogador (http-client)

```
🔄 Cliente iniciando...
📡 Servidor alvo: http://web-server:8080
⏱️  Intervalo entre requisições: 5s
==================================================

⏳ Aguardando servidor ficar disponível...
✅ Servidor está disponível!

[2025-11-13 10:15:01] 📤 Requisição #1
✅ Resposta recebida:
{
    "game_status": "🎮 RPG das Requisições HTTP",
    "player_stats": {
        "level": 1,
        "title": "🌱 Novato das Requisições",
        "total_xp": 25,
        "xp_progress": "25/100 XP",
        "requests_made": 1
    },
    "this_request": {
        "xp_gained": 25,
        "critical_hit": false,
        "level_up": false,
        "message": "Continue assim, aventureiro! 💪"
    },
    "server_info": {
        "hostname": "web-server",
        "client_ip": "172.20.0.3",
        "timestamp": "2025-11-13 10:15:01"
    }
}
---

[2025-11-13 10:15:06] 📤 Requisição #2
✅ Resposta recebida:
{
    "game_status": "🎮 RPG das Requisições HTTP",
    "player_stats": {
        "level": 1,
        "title": "🌱 Novato das Requisições",
        "total_xp": 85,
        "xp_progress": "85/100 XP",
        "requests_made": 2
    },
    "this_request": {
        "xp_gained": 60,
        "critical_hit": true,
        "level_up": false,
        "message": "💥 CRITICAL HIT! Suas habilidades estão melhorando! 📈"
    }
}
---
```

## 🔍 Detalhes Técnicos

### 🎲 Sistema de Jogo

**Mecânicas de Progressão:**
- Cada requisição ganha entre 15-30 XP (aleatório)
- 10% de chance de CRITICAL HIT (dobra o XP ganho)
- 100 XP = 1 nível
- Títulos especiais desbloqueados em níveis específicos
- Mensagens motivacionais aleatórias

**Persistência:**
- XP e nível são mantidos enquanto o container estiver rodando
- Reiniciar o container reseta o progresso (como um New Game+!)

**Algoritmo de Níveis:**
```python
nivel = (xp_total // 100) + 1
xp_no_nivel_atual = xp_total - ((nivel - 1) * 100)
```

### 1. Configuração da Rede Docker

A rede `desafio-network` é configurada no `docker-compose.yml`:

```yaml
networks:
  desafio-network:
    name: desafio-network
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

**Características:**
- **Driver bridge**: Permite comunicação entre containers no mesmo host
- **Subnet customizado**: Range de IPs dedicado (172.20.0.0/16)
- **DNS automático**: Containers se comunicam por nome (web-server, http-client)
- **Isolamento**: Tráfego isolado de outras redes Docker

### 2. Health Check e Dependências

O servidor possui health check configurado:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 10s
```
O cliente espera o servidor estar saudável:

```yaml
depends_on:
  web-server:
    condition: service_healthy
```
Isso garante que:
- O cliente só inicia após o servidor estar pronto
- Evita erros de conexão durante inicialização
- Torna o ambiente mais robusto

### 3. Resolução DNS

O Docker fornece DNS interno automático:
- Cada container pode acessar outros pelo nome do serviço
- `http://web-server:8080` resolve para o IP do container
- Não é necessário hardcoded de IPs
- Se o container reiniciar com novo IP, DNS atualiza automaticamente

### 4. Logs e Monitoramento

Ambos os containers geram logs estruturados:
- **Timestamps**: Todas as operações têm timestamp
- **Contadores**: Rastreiam número de requisições
- **Informações de rede**: IPs e hostnames nos logs
- **Status**: Indicadores visuais (✅, ❌, 📤, etc.)
