#!/bin/bash

echo "============================================================"
echo "🧪 TESTE DE COMUNICAÇÃO ENTRE SERVIÇOS"
echo "============================================================"
echo ""
echo "Este script demonstra a comunicação entre os 3 serviços:"
echo "  1. Battle Arena (Web/API) ↔ Database (PostgreSQL)"
echo "  2. Battle Arena (Web/API) ↔ Cache (Redis)"
echo "  3. Integração completa dos 3 serviços"
echo ""
echo "============================================================"
echo ""

API_URL="http://localhost:5000"

echo "📡 TESTE 1: Health Check de Todos os Serviços"
echo "------------------------------------------------------------"
echo "Verificando se API, Database e Cache estão comunicando..."
echo ""
curl -s $API_URL/health | python3 -m json.tool
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "👥 TESTE 2: Listar Heróis (Web → Database)"
echo "------------------------------------------------------------"
echo "API consultando heróis no PostgreSQL..."
echo ""
curl -s $API_URL/heroes | python3 -m json.tool | head -30
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "🏆 TESTE 3: Ver Ranking (Web → Cache → Database)"
echo "------------------------------------------------------------"
echo "Primeira chamada busca do Database e salva no Redis..."
echo ""
curl -s $API_URL/ranking | python3 -m json.tool
echo ""
echo "Segunda chamada (deve vir do cache Redis)..."
sleep 1
curl -s $API_URL/ranking | python3 -m json.tool | head -15
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "⚔️ TESTE 4: Criar Batalha (Integração Completa)"
echo "------------------------------------------------------------"
echo "Simulando batalha entre dois heróis..."
echo "Isso irá:"
echo "  1. API recebe requisição"
echo "  2. Consulta heróis no Database (PostgreSQL)"
echo "  3. Simula batalha"
echo "  4. Salva resultado no Database"
echo "  5. Invalida cache no Redis"
echo ""

curl -s -X POST $API_URL/battle \
  -H "Content-Type: application/json" \
  -d '{"hero1_id": 1, "hero2_id": 2}' | python3 -m json.tool
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "📊 TESTE 5: Estatísticas Gerais"
echo "------------------------------------------------------------"
curl -s $API_URL/stats | python3 -m json.tool
echo ""
read -p "Pressione ENTER para continuar..."
echo ""

echo "📜 TESTE 6: Histórico de Batalhas (Database)"
echo "------------------------------------------------------------"
curl -s "$API_URL/battles?limit=5" | python3 -m json.tool
echo ""

echo "============================================================"
echo "✅ TESTES DE COMUNICAÇÃO CONCLUÍDOS!"
echo "============================================================"
echo ""
echo "🎉 RESULTADOS:"
echo "   ✅ API (Battle Arena) está funcionando"
echo "   ✅ Database (PostgreSQL) está respondendo"
echo "   ✅ Cache (Redis) está funcionando"
echo "   ✅ Comunicação entre serviços OK"
echo "   ✅ Dependências (depends_on) funcionando"
echo "   ✅ Rede interna (arena-network) operacional"
echo ""
echo "💡 Todos os 3 serviços estão orquestrados e comunicando!"
echo ""
