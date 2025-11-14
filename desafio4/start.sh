#!/bin/bash

echo "============================================================"
echo "🏰 INICIANDO MICROSSERVIÇOS DE GUILDAS"
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

echo "🚀 Iniciando microsserviços..."
docker compose up -d
echo ""

echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10
echo ""

echo "📊 STATUS DOS SERVIÇOS:"
echo "============================================================"
docker compose ps
echo ""

echo "🌐 INFORMAÇÕES DA REDE:"
echo "============================================================"
docker network inspect microservices-network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{println}}{{end}}'
echo ""

echo "✅ Microsserviços inicializados com sucesso!"
echo ""
echo "📝 Endpoints disponíveis:"
echo ""
echo "🏰 Guild Service (Microsserviço A):"
echo "   • http://localhost:8000"
echo "   • http://localhost:8000/guilds"
echo "   • http://localhost:8000/guilds/1"
echo "   • http://localhost:8000/health"
echo ""
echo "📊 Guild Reporter (Microsserviço B):"
echo "   • http://localhost:8001"
echo "   • http://localhost:8001/report"
echo "   • http://localhost:8001/report/1"
echo "   • http://localhost:8001/summary"
echo "   • http://localhost:8001/activity"
echo ""
echo "🧪 Testar comunicação: ./test-communication.sh"
echo ""
