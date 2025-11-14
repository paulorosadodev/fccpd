#!/bin/bash

echo "============================================================"
echo "🚪 INICIANDO API GATEWAY E MICROSSERVIÇOS"
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

echo "🚀 Iniciando todos os serviços..."
docker compose up -d
echo ""

echo "⏳ Aguardando serviços ficarem prontos..."
sleep 15
echo ""

echo "📊 STATUS DOS SERVIÇOS:"
echo "============================================================"
docker compose ps
echo ""

echo "🌐 INFORMAÇÕES DA REDE:"
echo "============================================================"
docker network inspect gateway-network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{println}}{{end}}'
echo ""

echo "✅ API Gateway e Microsserviços inicializados com sucesso!"
echo ""
echo "📝 Endpoints disponíveis via Gateway (porta 8000):"
echo ""
echo "🚪 API Gateway (Ponto Único de Entrada):"
echo "   • http://localhost:8000"
echo "   • http://localhost:8000/health"
echo ""
echo "👤 Endpoints de Jogadores (via Gateway):"
echo "   • http://localhost:8000/players"
echo "   • http://localhost:8000/players/1"
echo ""
echo "⚔️ Endpoints de Itens (via Gateway):"
echo "   • http://localhost:8000/items"
echo "   • http://localhost:8000/items/1"
echo ""
echo "🔗 Endpoints Orquestrados:"
echo "   • http://localhost:8000/players/1/items (combina Player + Item)"
echo "   • http://localhost:8000/stats (estatísticas agregadas)"
echo ""
echo "🧪 Testar gateway: ./test-gateway.sh"
echo ""
