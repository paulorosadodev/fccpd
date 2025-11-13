#!/bin/bash

echo "============================================================"
echo "🏰 INICIANDO TAVERNA DOS HERÓIS - Desafio de Persistência"
echo "============================================================"
echo ""

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker."
    exit 1
fi

echo "✅ Docker está rodando"
echo ""

echo "🔨 Construindo imagens Docker..."
docker compose build
echo ""

echo "🚀 Iniciando containers..."
docker compose up -d tavern-database
echo ""

echo "⏳ Aguardando banco de dados inicializar..."
sleep 10
echo ""

echo "🎮 Executando Game Master (demonstração)..."
docker compose run --rm game-master
echo ""

echo "💾 INFORMAÇÕES DO VOLUME PERSISTENTE:"
echo "============================================================"
docker volume inspect tavern-data --format '{{.Name}}: {{.Mountpoint}}'
docker volume inspect tavern-data --format 'Driver: {{.Driver}}'
echo ""

echo "✅ Taverna dos Heróis inicializada com sucesso!"
echo ""
echo "📝 Comandos úteis:"
echo "   • Ver dados: docker compose run --rm quest-reader"
echo "   • Modo interativo Game Master: docker compose run --rm game-master python game_master.py interactive"
echo "   • Ver logs do banco: docker compose logs tavern-database"
echo "   • Parar tudo: docker compose down"
echo "   • Testar persistência: ./test-persistence.sh"
echo ""
