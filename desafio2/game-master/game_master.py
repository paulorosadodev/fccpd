import psycopg2
import time
import sys
from datetime import datetime
import random

DB_CONFIG = {
    'dbname': 'tavern_rpg',
    'user': 'gamemaster',
    'password': 'hero123',
    'host': 'tavern-database',
    'port': '5432'
}

def wait_for_database(max_retries=30):
    print("⏳ Aguardando banco de dados da taverna ficar disponível...")
    
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✅ Banco de dados conectado!")
            return True
        except psycopg2.OperationalError:
            print(f"   Tentativa {i+1}/{max_retries}...")
            time.sleep(2)
    
    print("❌ Não foi possível conectar ao banco de dados")
    return False

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def print_separator(char='=', length=70):
    print(char * length)

def show_welcome():
    print_separator()
    print("🏰 BEM-VINDO À TAVERNA DOS HERÓIS - GAME MASTER CONSOLE")
    print_separator()
    print("🎮 Sistema de gerenciamento de heróis, quests e inventário")
    print("💾 Todos os dados são persistidos em volumes Docker")
    print_separator()
    print()

def show_tavern_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("📊 ESTATÍSTICAS DA TAVERNA")
    print_separator('-')
    
    cursor.execute("SELECT * FROM tavern_stats")
    stats = cursor.fetchone()
    
    print(f"  👥 Total de Heróis: {stats[0]}")
    print(f"  📈 Nível Médio: {stats[1]}")
    print(f"  💰 Ouro Total: {stats[2]:,}")
    print(f"  ⭐ Nível Mais Alto: {stats[3]}")
    print(f"  📜 Quests Disponíveis: {stats[4]}")
    print(f"  ✅ Quests Completadas: {stats[5]}")
    print()
    
    cursor.close()
    conn.close()

def show_hero_ranking():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🏆 RANKING DE HERÓIS")
    print_separator('-')
    
    cursor.execute("""
        SELECT ranking, name, class, level, experience, gold 
        FROM hero_ranking
    """)
    
    for row in cursor.fetchall():
        rank_emoji = "🥇" if row[0] == 1 else "🥈" if row[0] == 2 else "🥉" if row[0] == 3 else "  "
        print(f"  {rank_emoji} #{row[0]} - {row[1]}")
        print(f"       Classe: {row[2]} | Nível: {row[3]} | XP: {row[4]:,} | Ouro: {row[5]:,}")
    
    print()
    cursor.close()
    conn.close()

def show_available_quests():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("📜 QUESTS DISPONÍVEIS NO QUADRO DE AVISOS")
    print_separator('-')
    
    cursor.execute("""
        SELECT title, difficulty, reward_xp, reward_gold, status 
        FROM quests 
        WHERE status = 'available'
        ORDER BY 
            CASE difficulty 
                WHEN 'Fácil' THEN 1 
                WHEN 'Médio' THEN 2 
                WHEN 'Difícil' THEN 3 
            END
    """)
    
    for row in cursor.fetchall():
        difficulty_emoji = "🟢" if row[1] == "Fácil" else "🟡" if row[1] == "Médio" else "🔴"
        print(f"  {difficulty_emoji} {row[0]}")
        print(f"       Dificuldade: {row[1]} | Recompensa: {row[2]} XP + {row[3]} Ouro")
    
    print()
    cursor.close()
    conn.close()

def create_new_hero():
    conn = get_connection()
    cursor = conn.cursor()
    
    first_names = ["Aldric", "Brienne", "Cedric", "Diana", "Erik", "Fiona", "Gareth", "Helena"]
    last_names = ["o Valente", "a Sábia", "das Sombras", "de Ferro", "Flamejante", "Gélida"]
    classes = ["Guerreiro", "Mago", "Ranger", "Clérigo", "Paladino", "Ladino"]
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    hero_class = random.choice(classes)
    
    cursor.execute("""
        INSERT INTO heroes (name, class, level, experience, health_points, mana_points, gold)
        VALUES (%s, %s, 1, 0, 100, 50, 100)
        RETURNING id, name, class
    """, (name, hero_class))
    
    hero = cursor.fetchone()
    conn.commit()
    
    print("✨ NOVO HERÓI CHEGOU À TAVERNA!")
    print_separator('-')
    print(f"  ID: {hero[0]}")
    print(f"  Nome: {hero[1]}")
    print(f"  Classe: {hero[2]}")
    print(f"  Nível: 1")
    print(f"  💰 Ouro inicial: 100")
    print()
    
    cursor.close()
    conn.close()

def show_hero_inventory(hero_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM heroes WHERE id = %s", (hero_id,))
    hero = cursor.fetchone()
    
    if not hero:
        print(f"❌ Herói com ID {hero_id} não encontrado!")
        return
    
    print(f"🎒 INVENTÁRIO DE {hero[0]}")
    print_separator('-')
    
    cursor.execute("""
        SELECT item_name, item_type, quantity, power 
        FROM inventory 
        WHERE hero_id = %s
        ORDER BY item_type, power DESC
    """, (hero_id,))
    
    items = cursor.fetchall()
    
    if items:
        for item in items:
            type_emoji = "⚔️" if item[1] == "Arma" else "🛡️" if item[1] == "Escudo" or item[1] == "Armadura" else "📦"
            print(f"  {type_emoji} {item[0]}")
            print(f"       Tipo: {item[1]} | Quantidade: {item[2]} | Poder: {item[3]}")
    else:
        print("  📭 Inventário vazio")
    
    print()
    cursor.close()
    conn.close()

def show_achievements(hero_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM heroes WHERE id = %s", (hero_id,))
    hero = cursor.fetchone()
    
    if not hero:
        print(f"❌ Herói com ID {hero_id} não encontrado!")
        return
    
    print(f"🏅 CONQUISTAS DE {hero[0]}")
    print_separator('-')
    
    cursor.execute("""
        SELECT achievement_name, achievement_description, unlocked_at 
        FROM achievements 
        WHERE hero_id = %s
        ORDER BY unlocked_at DESC
    """, (hero_id,))
    
    achievements = cursor.fetchall()
    
    if achievements:
        for ach in achievements:
            print(f"  {ach[0]}")
            print(f"       {ach[1]}")
            print(f"       Desbloqueado em: {ach[2].strftime('%Y-%m-%d %H:%M')}")
    else:
        print("  📭 Nenhuma conquista desbloqueada ainda")
    
    print()
    cursor.close()
    conn.close()

def interactive_mode():
    show_welcome()
    
    while True:
        print("\n🎮 MENU DO GAME MASTER")
        print_separator('-')
        print("  1️⃣  - Mostrar estatísticas da taverna")
        print("  2️⃣  - Mostrar ranking de heróis")
        print("  3️⃣  - Mostrar quests disponíveis")
        print("  4️⃣  - Criar novo herói")
        print("  5️⃣  - Ver inventário de herói")
        print("  6️⃣  - Ver conquistas de herói")
        print("  0️⃣  - Sair")
        print()
        
        choice = input("Escolha uma opção: ").strip()
        print()
        
        if choice == '1':
            show_tavern_stats()
        elif choice == '2':
            show_hero_ranking()
        elif choice == '3':
            show_available_quests()
        elif choice == '4':
            create_new_hero()
        elif choice == '5':
            hero_id = input("Digite o ID do herói: ").strip()
            if hero_id.isdigit():
                show_hero_inventory(int(hero_id))
        elif choice == '6':
            hero_id = input("Digite o ID do herói: ").strip()
            if hero_id.isdigit():
                show_achievements(int(hero_id))
        elif choice == '0':
            print("👋 Até logo, Game Master!")
            break
        else:
            print("❌ Opção inválida!")

def demo_mode():
    show_welcome()
    
    print("🎬 MODO DEMONSTRAÇÃO - Exibindo dados da taverna\n")
    time.sleep(2)
    
    show_tavern_stats()
    time.sleep(3)
    
    show_hero_ranking()
    time.sleep(3)
    
    show_available_quests()
    time.sleep(3)
    
    print("🎒 Exibindo inventário dos heróis principais...\n")
    for hero_id in [1, 2, 3]:
        show_hero_inventory(hero_id)
        time.sleep(2)
    
    print("✅ Demonstração concluída!")
    print("💾 Todos os dados estão sendo persistidos no volume Docker")
    print("🔄 Você pode recriar o container e os dados permanecerão!")

def main():
    if not wait_for_database():
        sys.exit(1)
    
    mode = sys.argv[1] if len(sys.argv) > 1 else 'demo'
    
    if mode == 'interactive':
        interactive_mode()
    else:
        demo_mode()

if __name__ == '__main__':
    main()
