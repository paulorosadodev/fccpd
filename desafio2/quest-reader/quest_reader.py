import psycopg2
import time
import sys
from datetime import datetime

DB_CONFIG = {
    'dbname': 'tavern_rpg',
    'user': 'gamemaster',
    'password': 'hero123',
    'host': 'tavern-database',
    'port': '5432'
}

def wait_for_database(max_retries=30):
    print("⏳ Quest Reader aguardando banco de dados...")
    
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✅ Conectado ao banco de dados persistido!")
            return True
        except psycopg2.OperationalError:
            print(f"   Tentativa {i+1}/{max_retries}...")
            time.sleep(2)
    
    print("❌ Não foi possível conectar ao banco de dados")
    return False

def print_separator(char='=', length=70):
    print(char * length)

def verify_data_persistence():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print_separator()
    print("🔍 VERIFICAÇÃO DE PERSISTÊNCIA DE DADOS")
    print_separator()
    print()
    
    cursor.execute("SELECT COUNT(*) FROM heroes")
    hero_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM quests")
    quest_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM inventory")
    item_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM achievements")
    achievement_count = cursor.fetchone()[0]
    
    print("✅ DADOS ENCONTRADOS NO VOLUME:")
    print(f"   👥 Heróis: {hero_count}")
    print(f"   📜 Quests: {quest_count}")
    print(f"   🎒 Itens: {item_count}")
    print(f"   🏅 Conquistas: {achievement_count}")
    print()
    
    if hero_count > 0:
        print("💾 ✅ PERSISTÊNCIA CONFIRMADA!")
        print("   Os dados sobreviveram à recriação do container!")
    else:
        print("⚠️  Nenhum dado encontrado (primeira execução?)")
    
    print()
    cursor.close()
    conn.close()

def read_all_heroes():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("📚 LENDO TODOS OS HERÓIS DA TAVERNA")
    print_separator('-')
    
    cursor.execute("""
        SELECT id, name, class, level, experience, health_points, mana_points, gold, created_at
        FROM heroes
        ORDER BY level DESC, experience DESC
    """)
    
    heroes = cursor.fetchall()
    
    if heroes:
        for hero in heroes:
            print(f"\n  🦸 ID: {hero[0]} - {hero[1]}")
            print(f"     Classe: {hero[2]} | Nível: {hero[3]}")
            print(f"     💚 HP: {hero[5]} | 💙 MP: {hero[6]} | 💰 Ouro: {hero[7]:,}")
            print(f"     ⚡ XP: {hero[4]:,}")
            print(f"     📅 Criado em: {hero[8].strftime('%Y-%m-%d %H:%M')}")
    else:
        print("  📭 Nenhum herói encontrado")
    
    print()
    cursor.close()
    conn.close()

def read_all_quests():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("📚 LENDO TODAS AS QUESTS")
    print_separator('-')
    
    cursor.execute("""
        SELECT title, description, difficulty, reward_xp, reward_gold, status, created_at
        FROM quests
        ORDER BY 
            CASE difficulty 
                WHEN 'Fácil' THEN 1 
                WHEN 'Médio' THEN 2 
                WHEN 'Difícil' THEN 3 
            END,
            created_at
    """)
    
    quests = cursor.fetchall()
    
    if quests:
        for quest in quests:
            status_emoji = "✅" if quest[5] == "completed" else "🔄" if quest[5] == "in_progress" else "📜"
            difficulty_emoji = "🟢" if quest[2] == "Fácil" else "🟡" if quest[2] == "Médio" else "🔴"
            
            print(f"\n  {status_emoji} {quest[0]}")
            print(f"     {quest[1]}")
            print(f"     {difficulty_emoji} Dificuldade: {quest[2]} | Status: {quest[5]}")
            print(f"     💎 Recompensa: {quest[3]} XP + {quest[4]} Ouro")
    else:
        print("  📭 Nenhuma quest encontrada")
    
    print()
    cursor.close()
    conn.close()

def continuous_reading():
    print_separator()
    print("📖 QUEST READER - MODO CONTÍNUO")
    print_separator()
    print("Lendo dados a cada 10 segundos...")
    print("(Pressione Ctrl+C para parar)")
    print()
    
    iteration = 1
    while True:
        try:
            print(f"\n🔄 Leitura #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print_separator('-')
            
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM heroes")
            heroes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM quests WHERE status = 'completed'")
            completed = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(gold) FROM heroes")
            total_gold = cursor.fetchone()[0] or 0
            
            print(f"  👥 Heróis na taverna: {heroes}")
            print(f"  ✅ Quests completadas: {completed}")
            print(f"  💰 Ouro total: {total_gold:,}")
            
            cursor.close()
            conn.close()
            
            iteration += 1
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n\n👋 Leitura interrompida pelo usuário")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            time.sleep(5)

def main():

    if not wait_for_database():
        sys.exit(1)
    
    time.sleep(2)
    
    verify_data_persistence()
    
    read_all_heroes()
    read_all_quests()

    mode = sys.argv[1] if len(sys.argv) > 1 else 'once'
    if mode == 'continuous':
        continuous_reading()
    else:
        print("✅ Leitura concluída!")
        print("💾 Dados lidos do volume persistido com sucesso!")

if __name__ == '__main__':
    main()
