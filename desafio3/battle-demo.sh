#!/bin/bash

echo "============================================================"
echo "⚔️ DEMONSTRAÇÃO DE BATALHAS - Arena RPG"
echo "============================================================"
echo ""

API_URL="http://localhost:5000"

echo "Vamos simular 5 batalhas épicas na arena!"
echo ""

battles=(
    '{"hero1_id": 1, "hero2_id": 2}'
    '{"hero1_id": 3, "hero2_id": 4}'
    '{"hero1_id": 5, "hero2_id": 6}'
    '{"hero1_id": 7, "hero2_id": 8}'
    '{"hero1_id": 2, "hero2_id": 5}'
)

for i in "${!battles[@]}"; do
    echo "⚔️ BATALHA #$((i+1))"
    echo "------------------------------------------------------------"
    
    response=$(curl -s -X POST $API_URL/battle \
      -H "Content-Type: application/json" \
      -d "${battles[$i]}")
    
    battle_id=$(echo $response | python3 -c "import sys, json; print(json.load(sys.stdin)['battle_id'])" 2>/dev/null)
    
    if [ ! -z "$battle_id" ]; then
        echo "$response" | python3 -m json.tool 2>/dev/null | grep -A 20 "result"
        echo ""
        echo "✅ Batalha #$battle_id registrada!"
    else
        echo "❌ Erro na batalha"
    fi
    
    echo ""
    sleep 2
done

echo "============================================================"
echo "🏆 RANKING ATUALIZADO (do Cache Redis):"
echo "============================================================"
curl -s $API_URL/ranking | python3 -m json.tool | grep -A 30 "ranking"
echo ""

echo "✅ Demonstração concluída! Todas as batalhas foram registradas."
echo ""
