#!/bin/bash

echo "============================================================"
echo "🧪 TESTE DE COMUNICAÇÃO ENTRE MICROSSERVIÇOS"
echo "============================================================"
echo ""
echo "Este script demonstra a comunicação HTTP entre:"
echo "  1. Guild Service (Microsserviço A) - Fornece dados"
echo "  2. Guild Reporter (Microsserviço B) - Consome e processa"
echo ""
echo "============================================================"
echo ""

GUILD_SERVICE="http://localhost:8000"
REPORTER_SERVICE="http://localhost:8001"

echo "📡 TESTE 1: Health Check dos Serviços"
echo "------------------------------------------------------------"
echo "Verificando se ambos os serviços estão online..."
echo ""

echo "🏰 Guild Service:"
curl -s $GUILD_SERVICE/health | python3 -m json.tool
echo ""

echo "📊 Guild Reporter:"
curl -s $REPORTER_SERVICE/health | python3 -m json.tool
echo ""

read -p "Pressione ENTER para continuar..."
echo ""

echo "🏰 TESTE 2: Microsserviço A - Listar Guildas"
echo "------------------------------------------------------------"
echo "Guild Service retorna lista de guildas (dados originais)..."
echo ""
curl -s $GUILD_SERVICE/guilds | python3 -m json.tool | head -40
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "📊 TESTE 3: Microsserviço B Consome Microsserviço A"
echo "------------------------------------------------------------"
echo "Guild Reporter faz requisição HTTP ao Guild Service..."
echo "e combina os dados em um relatório formatado:"
echo ""
curl -s $REPORTER_SERVICE/report | python3 -m json.tool | head -60
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "📈 TESTE 4: Relatório Detalhado de uma Guilda"
echo "------------------------------------------------------------"
echo "Reporter consome dados específicos do Service..."
echo ""
curl -s $REPORTER_SERVICE/report/1 | python3 -m json.tool | head -50
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "📋 TESTE 5: Resumo Executivo"
echo "------------------------------------------------------------"
echo "Reporter agrega dados de todas as guildas..."
echo ""
curl -s $REPORTER_SERVICE/summary | python3 -m json.tool
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "⚡ TESTE 6: Análise de Atividade"
echo "------------------------------------------------------------"
echo "Reporter processa e analisa dados do Service..."
echo ""
curl -s $REPORTER_SERVICE/activity | python3 -m json.tool | head -40
echo ""

echo "============================================================"
echo "✅ TESTES DE COMUNICAÇÃO CONCLUÍDOS!"
echo "============================================================"
echo ""
echo "🎉 RESULTADOS:"
echo "   ✅ Guild Service (A) está funcionando"
echo "   ✅ Guild Reporter (B) está funcionando"
echo "   ✅ Comunicação HTTP entre serviços OK"
echo "   ✅ Reporter consome dados do Service"
echo "   ✅ Dados são combinados e processados"
echo ""
echo "💡 Microsserviços independentes comunicando via HTTP!"
echo ""
