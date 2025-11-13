#!/bin/bash

echo "============================================================"
echo "⚔️ INICIANDO ARENA DE BATALHAS - Desafio de Orquestração"
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
docker network inspect arena-network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{println}}{{end}}'
echo ""

echo "💾 VOLUMES CRIADOS:"
echo "============================================================"
docker volume ls | grep arena
echo ""

echo "✅ Arena de Batalhas inicializada com sucesso!"
echo ""
echo "📝 Comandos úteis:"
echo "   • Ver API:           curl http://localhost:5000"
echo "   • Health check:      curl http://localhost:5000/health"
echo "   • Listar heróis:     curl http://localhost:5000/heroes"
echo "   • Ver ranking:       curl http://localhost:5000/ranking"
echo "   • Testar comunicação: ./test-services.sh"
echo "   • Ver logs:          docker compose logs -f"
echo "   • Parar tudo:        docker compose down"
echo ""
