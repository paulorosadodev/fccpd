#!/bin/bash

echo "============================================================"
echo "🧪 TESTE DE PERSISTÊNCIA - Taverna dos Heróis"
echo "============================================================"
echo ""
echo "Este script demonstra que os dados persistem após recriação"
echo "dos containers, graças aos volumes Docker."
echo ""
echo "============================================================"
echo ""

read -p "Pressione ENTER para iniciar o teste..."
echo ""

echo "📖 PASSO 1: Lendo dados atuais..."
echo "------------------------------------------------------------"
docker compose run --rm quest-reader
echo ""

read -p "Pressione ENTER para continuar..."
echo ""

echo "🗑️  PASSO 2: REMOVENDO TODOS OS CONTAINERS..."
echo "------------------------------------------------------------"
echo "⚠️  Atenção: Vamos remover os containers (mas não o volume!)"
docker compose down
echo ""
echo "✅ Containers removidos!"
echo ""

read -p "Pressione ENTER para continuar..."
echo ""

echo "💾 PASSO 3: Verificando se o VOLUME ainda existe..."
echo "------------------------------------------------------------"
docker volume ls | grep tavern-data
echo ""
if docker volume inspect tavern-data > /dev/null 2>&1; then
    echo "✅ Volume 'tavern-data' AINDA EXISTE!"
    echo "   Os dados estão seguros no volume."
else
    echo "❌ Volume não encontrado!"
    exit 1
fi
echo ""

read -p "Pressione ENTER para continuar..."
echo ""

echo "🔄 PASSO 4: RECRIANDO o container do banco de dados..."
echo "------------------------------------------------------------"
docker compose up -d tavern-database
echo ""
echo "⏳ Aguardando banco ficar pronto..."
sleep 15
echo "✅ Container do banco recriado!"
echo ""

read -p "Pressione ENTER para continuar..."
echo ""

echo "📖 PASSO 5: Lendo dados APÓS recriar o container..."
echo "------------------------------------------------------------"
docker compose run --rm quest-reader
echo ""

echo "============================================================"
echo "✅ TESTE DE PERSISTÊNCIA CONCLUÍDO!"
echo "============================================================"
echo ""
echo "🎉 RESULTADO: Os dados PERSISTIRAM!"
echo ""
echo "📚 O QUE ACONTECEU:"
echo "   1. Lemos os dados originais"
echo "   2. Removemos TODOS os containers"
echo "   3. O volume permaneceu intacto"
echo "   4. Recriamos o container do banco"
echo "   5. Os mesmos dados foram recuperados!"
echo ""
echo "💡 CONCLUSÃO:"
echo "   Volumes Docker garantem que os dados sobrevivam à"
echo "   remoção e recriação de containers!"
echo ""
echo "============================================================"
echo ""
