#!/bin/bash

echo "🐳 Iniciando Desafio Docker - Comunicação entre Containers"
echo "=" | head -c 60
echo ""

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker e tente novamente."
    exit 1
fi

echo "✅ Docker está rodando"
echo ""

echo "🧹 Limpando containers anteriores (se existirem)..."
docker compose down 2>/dev/null
echo ""

echo "🔨 Construindo imagens Docker..."
docker compose build --no-cache
echo ""

echo "🚀 Iniciando containers..."
docker compose up -d
echo ""

echo "⏳ Aguardando containers iniciarem..."
sleep 5
echo ""

echo "📊 Status dos containers:"
docker compose ps
echo ""

echo "🌐 Informações da rede customizada:"
docker network inspect desafio-network --format '{{range .Containers}}Container: {{.Name}} - IP: {{.IPv4Address}}{{println}}{{end}}'
echo ""

echo "✅ Ambiente iniciado com sucesso!"
echo ""
echo "📝 Comandos úteis:"
echo "   • Ver logs do servidor:  docker compose logs -f web-server"
echo "   • Ver logs do cliente:   docker compose logs -f http-client"
echo "   • Ver logs de ambos:     docker compose logs -f"
echo "   • Parar containers:      docker compose down"
echo "   • Acessar servidor:      curl http://localhost:8080"
echo ""
echo "🔍 Iniciando visualização dos logs (Ctrl+C para sair)..."
echo ""
sleep 2

docker compose logs -f
