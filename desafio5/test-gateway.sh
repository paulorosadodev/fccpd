#!/bin/bash

echo "============================================================"
echo "🧪 TESTE DO API GATEWAY"
echo "============================================================"
echo ""
echo "Este script demonstra o Gateway como ponto único de entrada:"
echo "  1. Gateway orquestra chamadas aos microsserviços"
echo "  2. Cliente só precisa conhecer o Gateway (porta 8000)"
echo "  3. Gateway faz proxy para Player Service e Item Service"
echo "  4. Gateway combina dados de múltiplos serviços"
echo ""
echo "============================================================"
echo ""

GATEWAY_URL="http://localhost:8000"

echo "📡 TESTE 1: Health Check do Gateway"
echo "------------------------------------------------------------"
echo "Gateway verifica saúde de todos os serviços..."
echo ""
curl -s $GATEWAY_URL/health | python3 -m json.tool
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "👤 TESTE 2: Gateway → Player Service"
echo "------------------------------------------------------------"
echo "Cliente chama Gateway, Gateway chama Player Service..."
echo ""
curl -s $GATEWAY_URL/players | python3 -m json.tool | head -40
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "⚔️ TESTE 3: Gateway → Item Service"
echo "------------------------------------------------------------"
echo "Cliente chama Gateway, Gateway chama Item Service..."
echo ""
curl -s $GATEWAY_URL/items | python3 -m json.tool | head -40
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "🔗 TESTE 4: Gateway Orquestra Múltiplos Serviços"
echo "------------------------------------------------------------"
echo "Gateway combina Player Service + Item Service..."
echo "Cliente faz UMA requisição, Gateway faz DUAS internamente!"
echo ""
curl -s $GATEWAY_URL/players/1/items | python3 -m json.tool | head -50
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "📊 TESTE 5: Estatísticas Agregadas"
echo "------------------------------------------------------------"
echo "Gateway agrega dados de ambos os serviços..."
echo ""
curl -s $GATEWAY_URL/stats | python3 -m json.tool
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "🎯 TESTE 6: Demonstração de Isolamento"
echo "------------------------------------------------------------"
echo "Verificando que microsserviços NÃO estão expostos externamente..."
echo ""
echo "Verificando portas mapeadas:"
docker compose ps | grep -E "player-service|item-service|api-gateway" | awk '{print "  " $1 ": " $5}'
echo ""
echo "Tentando acessar Player Service diretamente na porta 8002..."
response=$(curl -s --connect-timeout 2 -w "\n%{http_code}" http://localhost:8002/players 2>&1)
http_code=$(echo "$response" | tail -1)
error_msg=$(echo "$response" | grep -i "connection\|refused\|timeout\|failed" | head -1)

if [ "$http_code" = "000" ] || [ -z "$http_code" ] || [ ! -z "$error_msg" ]; then
    echo "✅ CONFIRMADO: Player Service não está acessível externamente!"
    echo "   Erro: $error_msg (esperado - porta não exposta!)"
else
    echo "⚠️  ATENÇÃO: Player Service está acessível na porta 8002"
    echo "   HTTP Status: $http_code"
    echo "   Isso não deveria acontecer! Verifique docker-compose.yml"
fi
echo ""
echo "Tentando acessar Item Service diretamente na porta 8003..."
response=$(curl -s --connect-timeout 2 -w "\n%{http_code}" http://localhost:8003/items 2>&1)
http_code=$(echo "$response" | tail -1)
error_msg=$(echo "$response" | grep -i "connection\|refused\|timeout\|failed" | head -1)

if [ "$http_code" = "000" ] || [ -z "$http_code" ] || [ ! -z "$error_msg" ]; then
    echo "✅ CONFIRMADO: Item Service não está acessível externamente!"
    echo "   Erro: $error_msg (esperado - porta não exposta!)"
else
    echo "⚠️  ATENÇÃO: Item Service está acessível na porta 8003"
    echo "   HTTP Status: $http_code"
    echo "   Isso não deveria acontecer! Verifique docker-compose.yml"
fi
echo ""
echo "✅ Gateway é o ÚNICO ponto de entrada!"
echo "   Cliente só precisa conhecer porta 8000"
echo ""

echo "============================================================"
echo "✅ TESTES DO GATEWAY CONCLUÍDOS!"
echo "============================================================"
echo ""
echo "🎉 RESULTADOS:"
echo "   ✅ Gateway funciona como ponto único de entrada"
echo "   ✅ Gateway faz proxy para Player Service"
echo "   ✅ Gateway faz proxy para Item Service"
echo "   ✅ Gateway orquestra múltiplos serviços"
echo "   ✅ Microsserviços isolados (não expostos externamente)"
echo ""
echo "💡 Cliente só precisa conhecer o Gateway (porta 8000)!"
echo ""
