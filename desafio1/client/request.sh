#!/bin/bash

SERVER_URL="http://web-server:8080"
INTERVAL=5

echo "🔄 Cliente iniciando..."
echo "📡 Servidor alvo: $SERVER_URL"
echo "⏱️  Intervalo entre requisições: ${INTERVAL}s"
echo "=" | head -c 50
echo ""

counter=0

echo "⏳ Aguardando servidor ficar disponível..."
while ! curl -s "$SERVER_URL/health" > /dev/null; do
    echo "   Tentando conectar ao servidor..."
    sleep 2
done
echo "✅ Servidor está disponível!"
echo ""

while true; do
    counter=$((counter + 1))
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] 📤 Requisição #$counter"
    
    response=$(curl -s "$SERVER_URL")
    
    if [ $? -eq 0 ]; then
        echo "✅ Resposta recebida:"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        echo "❌ Erro ao fazer requisição"
    fi
    
    echo "---"
    echo ""
    
    sleep $INTERVAL
done

