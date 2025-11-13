# 🏰 Taverna dos Heróis: Desafio Docker de Volumes e Persistência

Este projeto demonstra persistência de dados em Docker através de um **sistema RPG de taverna**! Um banco de dados PostgreSQL armazena informações de heróis, quests e inventários em um volume Docker, garantindo que os dados sobrevivam mesmo após a remoção e recriação dos containers!

## 🎯 Objetivo

Demonstrar persistência de dados usando volumes Docker em um cenário prático e gamificado:
- 🗄️ **PostgreSQL com Volume**: Banco de dados completamente persistente
- 🎮 **Game Master**: Container que gerencia e cria dados dos heróis
- 📖 **Quest Reader**: Container que lê e verifica dados persistidos
- 💾 **Persistência Comprovada**: Dados sobrevivem à recriação de containers
- 🏆 **Tema RPG**: Taverna com heróis, quests, inventário e conquistas

## ▶️ Como rodar o desafio:

```bash
# Tornar scripts executáveis (primeira vez)
chmod +x start.sh test-persistence.sh

# Iniciar o ambiente
./start.sh
```

O script `start.sh` irá:
1. Construir todas as imagens Docker
2. Iniciar o banco de dados com volume persistente
3. Executar o Game Master para popular os dados
4. Mostrar informações do volume criado

### 🧪 Testar Persistência 

Para **comprovar que os dados persistem** mesmo após remover os containers:

```bash
# Execute o script de teste automatizado
./test-persistence.sh
```

**O que esse script faz:**
1. ✅ Lê os dados iniciais do banco
2. 🗑️ **Remove TODOS os containers** (mas mantém o volume!)
3. 💾 Verifica que o volume ainda existe
4. 🔄 **Recria apenas o container do banco**
5. ✅ Lê os dados novamente e **confirma que persistiram!**

Este teste **demonstra visualmente** que os dados sobrevivem à destruição e recriação dos containers, comprovando a persistência do volume Docker! 

## ✅ Requisitos Atendidos + Sistema RPG

### ✓ Banco de Dados com Volume (PostgreSQL)
- Container `tavern-database` rodando PostgreSQL 16
- **Volume nomeado `tavern-data`** para persistência
- Dados armazenados FORA do container
- Schema completo de RPG: Heróis, Quests, Inventário e Conquistas

### ✓ Persistência Após Recriação
- Script **`test-persistence.sh`** demonstra persistência automaticamente
- Remove containers completamente
- Volume permanece intacto
- Dados são recuperados ao recriar containers
- Logs e evidências visuais da persistência

### ✓ Container para Popular Dados (Game Master)
- Cria e gerencia heróis na taverna
- Adiciona quests, itens e conquistas
- Modo demonstração e modo interativo
- Interface visual com emojis e formatação

### ✓ Container para Ler Dados (Quest Reader)
- Lê todos os dados persistidos
- Verifica integridade da persistência
- Modo único e modo contínuo
- Comprova que dados sobreviveram

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                    Host Machine                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Docker Network: rpg-network               │  │
│  │                                                   │  │
│  │  ┌──────────────────┐      ┌──────────────────┐   │  │
│  │  │  game-master     │──────▶ tavern-database  │   │  │
│  │  │  (Gerencia)      │      │                  │   │  │
│  │  └──────────────────┘      │  PostgreSQL 16   │   │  │
│  │                            │                  │   │  │
│  │  ┌──────────────────┐      │   Port: 5432     │   │  │
│  │  │  quest-reader    │──────▶                  │   │  │
│  │  │  (Lê dados)      │      └─────────┬────────┘   │  │
│  │  └──────────────────┘                │            │  │
│  └──────────────────────────────────────┼────────────┘  │
│                                         │               │
│                                   tavern-data           │
│                                 Docker Volume           │
│                            /var/lib/postgresql/data     │
│                                                         │
│                        💾 PERSISTENTE                   │
│                  (Sobrevive à recriação!)               │
└─────────────────────────────────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
desafio2/
├── database/                   # Banco de Dados PostgreSQL
│   ├── Dockerfile                # Imagem do PostgreSQL
│   └── init.sql                  # Schema e dados iniciais RPG
│
├── game-master/                # Container de Gerenciamento
│   ├── Dockerfile                # Imagem Python
│   ├── game_master.py            # Script de gerenciamento
│   └── requirements.txt          # Dependências Python
│
├── quest-reader/               # Container de Leitura
│   ├── Dockerfile                # Imagem Python
│   ├── quest_reader.py           # Script de leitura
│   └── requirements.txt          # Dependências Python
│
├── docker-compose.yml          # Orquestração + VOLUMES
├── start.sh                    # Script para iniciar
├── test-persistence.sh         # Script de teste de persistência
├── .gitignore                  # Arquivos a ignorar
└── README.md                   # Esta documentação
```

## 🎮 Demonstração do Sistema

### 1. Iniciando a Taverna

```bash
$ ./start.sh

============================================================
🏰 INICIANDO TAVERNA DOS HERÓIS - Desafio de Persistência
============================================================

✅ Docker está rodando

🔨 Construindo imagens Docker...
[+] Building 15.2s

🚀 Iniciando containers...
✅ Container tavern-database criado

⏳ Aguardando banco de dados inicializar...

🎮 Executando Game Master (demonstração)...
```

### 2. Saída do Game Master

```
============================================================
🏰 BEM-VINDO À TAVERNA DOS HERÓIS - GAME MASTER CONSOLE
============================================================
🎮 Sistema de gerenciamento de heróis, quests e inventário
💾 Todos os dados são persistidos em volumes Docker
============================================================

📊 ESTATÍSTICAS DA TAVERNA
------------------------------------------------------------
  👥 Total de Heróis: 5
  📈 Nível Médio: 18.00
  💰 Ouro Total: 10,200
  ⭐ Nível Mais Alto: 25
  📜 Quests Disponíveis: 3
  ✅ Quests Completadas: 1

🏆 RANKING DE HERÓIS
------------------------------------------------------------
  🥇 #1 - Gandalf o Sábio
       Classe: Mago | Nível: 25 | XP: 6,000 | Ouro: 3,000
  🥈 #2 - Thorin Machado
       Classe: Anão Guerreiro | Nível: 20 | XP: 4,500 | Ouro: 2,500
  🥉 #3 - Legolas Arqueiro
       Classe: Ranger | Nível: 18 | XP: 3,100 | Ouro: 2,000
```

### 3. Testando Persistência

```bash
$ ./test-persistence.sh

============================================================
🧪 TESTE DE PERSISTÊNCIA - Taverna dos Heróis
============================================================

📖 PASSO 1: Lendo dados atuais...
------------------------------------------------------------
🔍 VERIFICAÇÃO DE PERSISTÊNCIA DE DADOS
✅ DADOS ENCONTRADOS NO VOLUME:
   👥 Heróis: 5
   📜 Quests: 5
   🎒 Itens: 9
   🏅 Conquistas: 6

💾 ✅ PERSISTÊNCIA CONFIRMADA!

🗑️  PASSO 2: REMOVENDO TODOS OS CONTAINERS...
------------------------------------------------------------
 Container quest-reader  Removed
 Container game-master  Removed
 Container tavern-database  Removed
 Network rpg-network  Removed

✅ Containers removidos!

💾 PASSO 3: Verificando se o VOLUME ainda existe...
------------------------------------------------------------
local     tavern-data
✅ Volume 'tavern-data' AINDA EXISTE!
   Os dados estão seguros no volume.

🔄 PASSO 4: RECRIANDO o container do banco de dados...
------------------------------------------------------------
 Container tavern-database  Created
 Container tavern-database  Started

✅ Container do banco recriado!

📖 PASSO 5: Lendo dados APÓS recriar o container...
------------------------------------------------------------
🔍 VERIFICAÇÃO DE PERSISTÊNCIA DE DADOS
✅ DADOS ENCONTRADOS NO VOLUME:
   👥 Heróis: 5
   📜 Quests: 5
   🎒 Itens: 9
   🏅 Conquistas: 6

💾 ✅ PERSISTÊNCIA CONFIRMADA!
   Os dados sobreviveram à recriação do container!

============================================================
✅ TESTE DE PERSISTÊNCIA CONCLUÍDO!
============================================================

🎉 RESULTADO: Os dados PERSISTIRAM!

📚 O QUE ACONTECEU:
   1. Lemos os dados originais
   2. Removemos TODOS os containers
   3. O volume permaneceu intacto
   4. Recriamos o container do banco
   5. Os mesmos dados foram recuperados!

💡 CONCLUSÃO:
   Volumes Docker garantem que os dados sobrevivam à
   remoção e recriação de containers!
```

## 🔍 Detalhes Técnicos

### 💾 Sistema de Volumes

O volume é configurado no `docker-compose.yml`:

```yaml
volumes:
  tavern-data:
    name: tavern-data
    driver: local
```

**Características:**
- **Nome fixo**: `tavern-data` para fácil identificação
- **Driver local**: Armazena dados no host
- **Montagem**: `/var/lib/postgresql/data` no container
- **Persistência**: Sobrevive a `docker compose down`
- **Isolamento**: Separado do filesystem do container

### 🗄️ Schema do Banco de Dados

**Tabelas Principais:**

1. **heroes** - Informações dos heróis
   - id, name, class, level, experience
   - health_points, mana_points, gold
   - created_at, last_login

2. **quests** - Missões disponíveis
   - id, title, description, difficulty
   - reward_xp, reward_gold, status
   - created_at

3. **inventory** - Itens dos heróis
   - id, hero_id, item_name, item_type
   - quantity, power, acquired_at

4. **achievements** - Conquistas desbloqueadas
   - id, hero_id, achievement_name
   - achievement_description, unlocked_at

**Views e Estatísticas:**
- `hero_ranking` - Ranking de heróis por nível
- `tavern_stats` - Estatísticas gerais da taverna

### 🔗 Comunicação entre Containers

1. **Game Master** conecta ao banco:
   - Host: `tavern-database` (DNS do Docker)
   - Porta: `5432`
   - User: `gamemaster`
   - Database: `tavern_rpg`

2. **Quest Reader** lê os mesmos dados:
   - Mesmas credenciais
   - Leitura apenas
   - Verifica integridade

3. **Health Checks**:
   - PostgreSQL usa `pg_isready`
   - Containers aguardam banco estar saudável
   - Evita erros de conexão

### 📊 Dados Iniciais

O banco é populado automaticamente com:
- **5 heróis** pré-criados (Aragorn, Gandalf, Legolas, Thalia, Thorin)
- **5 quests** com diferentes dificuldades
- **9 itens** no inventário dos heróis
- **6 conquistas** já desbloqueadas
