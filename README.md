# 🎮 Desafios Docker - Fundamentos de Computação Concorrente, Paralela e Distribuída (FCCPD)

Este repositório contém **5 desafios práticos** desenvolvidos para a disciplina de **Fundamentos de Computação Concorrente, Paralela e Distribuída**, utilizando Docker como ferramenta principal para demonstrar conceitos de containerização, orquestração e arquitetura de microsserviços.

## 🎯 Temática do Projeto

Todos os desafios seguem uma **temática RPG (Role-Playing Game)** unificada, criando uma experiência gamificada e envolvente para o aprendizado:

- **Desafio 1**: Sistema de comunicação entre containers com servidor de jogo que recompensa requisições com XP
- **Desafio 2**: Taverna dos Heróis com persistência de dados em volumes Docker
- **Desafio 3**: Arena de Batalhas com orquestração de múltiplos serviços
- **Desafio 4**: Microsserviços de Guildas com comunicação HTTP independente
- **Desafio 5**: API Gateway centralizando acesso a serviços de jogadores e itens

Cada desafio constrói sobre o anterior, evoluindo de conceitos básicos até arquiteturas complexas de microsserviços.

## 📚 Desafios

### Desafio 1: Comunicação entre Containers 🐳

**Objetivo:** Criar dois containers que se comunicam por uma rede Docker customizada.

**Conceitos Demonstrados:**
- Configuração de redes Docker customizadas
- Comunicação inter-container via DNS interno
- Servidor web Flask e cliente HTTP automático
- Logs e monitoramento de tráfego

**Tema RPG:** Sistema de RPG onde cada requisição HTTP ganha XP, sobe de nível e conquista títulos épicos!

**📁 Diretório:** [`desafio1/`](./desafio1/)

---

### Desafio 2: Volumes e Persistência 💾

**Objetivo:** Demonstrar persistência de dados usando volumes Docker.

**Conceitos Demonstrados:**
- Criação e uso de volumes Docker nomeados
- Persistência de dados após remoção de containers
- Banco de dados PostgreSQL com volume
- Containers que leem dados persistidos

**Tema RPG:** Taverna dos Heróis - sistema completo de gerenciamento de heróis, quests, inventário e conquistas, com dados que persistem mesmo após recriação de containers!

**📁 Diretório:** [`desafio2/`](./desafio2/)

---

### Desafio 3: Docker Compose Orquestrando Serviços 🎼

**Objetivo:** Usar Docker Compose para orquestrar múltiplos serviços dependentes.

**Conceitos Demonstrados:**
- Orquestração de 3 serviços (Web, Database, Cache)
- Depends_on com health checks
- Rede interna customizada
- Variáveis de ambiente e configuração centralizada

**Tema RPG:** Arena de Batalhas - sistema completo de combate entre heróis com API Flask, PostgreSQL para persistência e Redis para cache de rankings em tempo real!

**📁 Diretório:** [`desafio3/`](./desafio3/)

---

### Desafio 4: Microsserviços Independentes 🔗

**Objetivo:** Criar dois microsserviços independentes que se comunicam via HTTP.

**Conceitos Demonstrados:**
- Arquitetura de microsserviços desacoplados
- Comunicação HTTP entre serviços independentes
- Dockerfiles separados por serviço
- Isolamento e independência de serviços

**Tema RPG:** Microsserviços de Guildas - Guild Service fornece dados de guildas e membros, enquanto Guild Reporter consome e gera relatórios combinados e análises detalhadas!

**📁 Diretório:** [`desafio4/`](./desafio4/)

---

### Desafio 5: Microsserviços com API Gateway 🚪

**Objetivo:** Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços.

**Conceitos Demonstrados:**
- API Gateway como ponto único de entrada
- Proxy pattern para roteamento de requisições
- Orquestração de múltiplos serviços
- Isolamento de microsserviços (não expostos externamente)

**Tema RPG:** Sistema completo com Player Service (jogadores), Item Service (equipamentos) e API Gateway que centraliza acesso, faz proxy e orquestra chamadas combinadas!

**📁 Diretório:** [`desafio5/`](./desafio5/)

---

## 🎓 Objetivos de Aprendizado

Através destes desafios, os alunos desenvolvem habilidades em:

- ✅ **Containerização**: Criação e gerenciamento de containers Docker
- ✅ **Redes Docker**: Configuração de redes customizadas e comunicação entre containers
- ✅ **Persistência**: Uso de volumes para dados persistentes
- ✅ **Orquestração**: Docker Compose para gerenciar múltiplos serviços
- ✅ **Microsserviços**: Arquitetura de serviços independentes e desacoplados
- ✅ **API Gateway**: Padrão de gateway para centralizar acesso
- ✅ **Comunicação HTTP**: Requisições REST entre serviços
- ✅ **Health Checks**: Monitoramento e verificação de saúde de serviços
- ✅ **Isolamento**: Segurança através de isolamento de serviços

## 🚀 Como Usar

Cada desafio é **independente** e pode ser executado separadamente:

```bash
# Navegar para o desafio desejado
cd desafio1  # ou desafio2, desafio3, desafio4, desafio5

# Seguir as instruções do README.md específico
# Geralmente:
chmod +x start.sh
./start.sh
```

Cada desafio possui:
- 📖 **README.md completo** com explicações detalhadas
- 🐳 **Dockerfiles** e **docker-compose.yml** configurados
- 🧪 **Scripts de teste** para validar funcionamento
- 📊 **Exemplos práticos** e demonstrações

## 📋 Pré-requisitos

- Docker instalado (versão 20.10 ou superior)
- Docker Compose instalado (versão 2.0 ou superior)
- Portas disponíveis: 5000, 8000, 8001, 8002, 8003, 8080, 5432
- Sistema operacional: Linux, macOS ou Windows (com WSL2)

## 🏗️ Estrutura do Repositório

```
fccpd/
├── desafio1/          # Comunicação entre Containers
├── desafio2/          # Volumes e Persistência
├── desafio3/          # Docker Compose Orquestração
├── desafio4/          # Microsserviços Independentes
├── desafio5/          # Microsserviços com API Gateway
└── README.md          # Este arquivo
```

## 🎮 Progressão dos Desafios

Os desafios foram projetados para **evoluir progressivamente** em complexidade:

1. **Desafio 1** → Comunicação básica entre 2 containers
2. **Desafio 2** → Adiciona persistência com volumes
3. **Desafio 3** → Orquestra 3 serviços interdependentes
4. **Desafio 4** → Microsserviços independentes comunicando via HTTP
5. **Desafio 5** → Arquitetura completa com Gateway centralizado

Cada desafio constrói sobre conceitos aprendidos nos anteriores, criando uma jornada de aprendizado estruturada.

## 📝 Documentação

Cada desafio possui documentação completa incluindo:
- Objetivos e requisitos atendidos
- Arquitetura detalhada com diagramas
- Instruções passo a passo
- Exemplos de uso e testes

## 📄 Licença

Este projeto é livre para uso educacional e demonstrativo.
