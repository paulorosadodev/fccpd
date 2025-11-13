from flask import Flask, jsonify, request
import psycopg2
import redis
import random
import time
import json
from datetime import datetime
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'battle_arena',
    'user': 'arena_master',
    'password': 'battle123',
    'host': 'arena-database',
    'port': '5432'
}

REDIS_CONFIG = {
    'host': 'arena-cache',
    'port': 6379,
    'decode_responses': True
}

def get_db():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def get_redis():
    return redis.Redis(**REDIS_CONFIG)

def wait_for_services():
    max_retries = 30
    
    print("⏳ Aguardando serviços...")
    
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            r = redis.Redis(**REDIS_CONFIG)
            r.ping()
            print("✅ Todos os serviços conectados!")
            return True
        except:
            print(f"   Tentativa {i+1}/{max_retries}...")
            time.sleep(2)
    
    return False

@app.route('/')
def home():
    return jsonify({
        'status': '⚔️ Arena de Batalhas - API Online',
        'message': 'Bem-vindo à Arena! Teste seus heróis em combate épico!',
        'endpoints': {
            '/heroes': 'Lista todos os heróis disponíveis',
            '/ranking': 'Ranking em tempo real (via Redis cache)',
            '/battle': 'POST - Iniciar uma batalha entre dois heróis',
            '/battles': 'Histórico de batalhas',
            '/stats': 'Estatísticas gerais da arena',
            '/health': 'Health check de todos os serviços'
        }
    }), 200

@app.route('/health')
def health():
    health_status = {
        'api': 'healthy',
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        conn.close()
        health_status['database'] = 'healthy'
    except Exception as e:
        health_status['database'] = f'unhealthy: {str(e)}'
    
    try:
        r = get_redis()
        r.ping()
        health_status['cache'] = 'healthy'
    except Exception as e:
        health_status['cache'] = f'unhealthy: {str(e)}'
    
    all_healthy = all(v == 'healthy' for k, v in health_status.items() if k != 'timestamp')
    status_code = 200 if all_healthy else 503
    
    return jsonify(health_status), status_code

@app.route('/heroes')
def get_heroes():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, class, level, attack_power, defense_power, 
            health_points, wins, losses, draws
        FROM heroes
        ORDER BY (wins * 3 + draws) DESC
    """)
    
    heroes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({
        'total': len(heroes),
        'heroes': heroes
    }), 200

@app.route('/ranking')
def get_ranking():
    r = get_redis()
    
    cache_key = 'ranking:current'
    cached = r.get(cache_key)
    
    if cached:
        ranking = json.loads(cached)
        return jsonify({
            'source': 'cache',
            'cached_at': ranking.get('cached_at'),
            'ranking': ranking.get('data')
        }), 200
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, class, level, wins, losses, draws, 
            win_rate, ranking_points
        FROM hero_stats
        LIMIT 10
    """)
    
    ranking_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    ranking_response = {
        'cached_at': datetime.now().isoformat(),
        'data': ranking_data
    }
    
    r.setex(cache_key, 60, json.dumps(ranking_response, default=str))
    
    return jsonify({
        'source': 'database',
        'ranking': ranking_data
    }), 200

@app.route('/battle', methods=['POST'])
def create_battle():
    data = request.get_json()
    
    if not data or 'hero1_id' not in data or 'hero2_id' not in data:
        return jsonify({'error': 'hero1_id e hero2_id são obrigatórios'}), 400
    
    hero1_id = data['hero1_id']
    hero2_id = data['hero2_id']
    
    if hero1_id == hero2_id:
        return jsonify({'error': 'Um herói não pode lutar contra si mesmo!'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM heroes WHERE id = %s', (hero1_id,))
    hero1 = cursor.fetchone()
    
    cursor.execute('SELECT * FROM heroes WHERE id = %s', (hero2_id,))
    hero2 = cursor.fetchone()
    
    if not hero1 or not hero2:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Herói não encontrado'}), 404
    
    battle_result = simulate_battle(hero1, hero2)
    
    cursor.execute("""
        INSERT INTO battles (hero1_id, hero2_id, winner_id, hero1_damage_dealt, 
                        hero2_damage_dealt, rounds, battle_log)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (hero1_id, hero2_id, battle_result['winner_id'],
        battle_result['hero1_damage'], battle_result['hero2_damage'],
        battle_result['rounds'], battle_result['log']))
    
    battle_id = cursor.fetchone()['id']
    
    if battle_result['winner_id'] == hero1_id:
        cursor.execute('UPDATE heroes SET wins = wins + 1, total_damage_dealt = total_damage_dealt + %s, total_damage_received = total_damage_received + %s WHERE id = %s',
                    (battle_result['hero1_damage'], battle_result['hero2_damage'], hero1_id))
        cursor.execute('UPDATE heroes SET losses = losses + 1, total_damage_dealt = total_damage_dealt + %s, total_damage_received = total_damage_received + %s WHERE id = %s',
                    (battle_result['hero2_damage'], battle_result['hero1_damage'], hero2_id))
    elif battle_result['winner_id'] == hero2_id:
        cursor.execute('UPDATE heroes SET losses = losses + 1, total_damage_dealt = total_damage_dealt + %s, total_damage_received = total_damage_received + %s WHERE id = %s',
                    (battle_result['hero1_damage'], battle_result['hero2_damage'], hero1_id))
        cursor.execute('UPDATE heroes SET wins = wins + 1, total_damage_dealt = total_damage_dealt + %s, total_damage_received = total_damage_received + %s WHERE id = %s',
                    (battle_result['hero2_damage'], battle_result['hero1_damage'], hero2_id))
    else:
        cursor.execute('UPDATE heroes SET draws = draws + 1 WHERE id IN (%s, %s)', (hero1_id, hero2_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    r = get_redis()
    r.delete('ranking:current')
    r.incr('stats:total_battles')
    
    return jsonify({
        'battle_id': battle_id,
        'result': battle_result
    }), 201

def simulate_battle(hero1, hero2):
    h1_hp = hero1['health_points']
    h2_hp = hero2['health_points']
    
    h1_damage_total = 0
    h2_damage_total = 0
    
    log = []
    rounds = 0
    max_rounds = 20
    
    log.append(f"⚔️ {hero1['name']} VS {hero2['name']}")
    log.append("=" * 50)
    
    while h1_hp > 0 and h2_hp > 0 and rounds < max_rounds:
        rounds += 1
        log.append(f"\nRound {rounds}:")
        
        h1_damage = max(0, hero1['attack_power'] - hero2['defense_power']//2 + random.randint(-10, 10))
        h2_hp -= h1_damage
        h1_damage_total += h1_damage
        log.append(f"  {hero1['name']} ataca! Dano: {h1_damage} (HP: {max(0, h2_hp)})")
        
        if h2_hp <= 0:
            break
        
        h2_damage = max(0, hero2['attack_power'] - hero1['defense_power']//2 + random.randint(-10, 10))
        h1_hp -= h2_damage
        h2_damage_total += h2_damage
        log.append(f"  {hero2['name']} contra-ataca! Dano: {h2_damage} (HP: {max(0, h1_hp)})")
    
    log.append("\n" + "=" * 50)
    
    if h1_hp > h2_hp:
        winner_id = hero1['id']
        log.append(f"🏆 VENCEDOR: {hero1['name']}!")
    elif h2_hp > h1_hp:
        winner_id = hero2['id']
        log.append(f"🏆 VENCEDOR: {hero2['name']}!")
    else:
        winner_id = None
        log.append("🤝 EMPATE!")
    
    return {
        'winner_id': winner_id,
        'hero1_damage': h1_damage_total,
        'hero2_damage': h2_damage_total,
        'rounds': rounds,
        'log': '\n'.join(log)
    }

@app.route('/battles')
def get_battles():
    limit = request.args.get('limit', 20, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.id, b.rounds, b.created_at,
            h1.name as hero1_name, h2.name as hero2_name,
            hw.name as winner_name,
            b.hero1_damage_dealt, b.hero2_damage_dealt
        FROM battles b
        JOIN heroes h1 ON b.hero1_id = h1.id
        JOIN heroes h2 ON b.hero2_id = h2.id
        LEFT JOIN heroes hw ON b.winner_id = hw.id
        ORDER BY b.created_at DESC
        LIMIT %s
    """, (limit,))
    
    battles = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({
        'total': len(battles),
        'battles': battles
    }), 200

@app.route('/stats')
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM heroes')
    total_heroes = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM battles')
    total_battles = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT name, wins FROM heroes 
        WHERE wins > 0 
        ORDER BY wins DESC LIMIT 1
    """)
    most_wins = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    r = get_redis()
    cache_hits = r.get('stats:cache_hits') or 0
    
    return jsonify({
        'total_heroes': total_heroes,
        'total_battles': total_battles,
        'most_victorious': most_wins,
        'cache_hits': int(cache_hits),
        'services_status': {
            'database': 'connected',
            'cache': 'connected',
            'api': 'running'
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("⚔️ ARENA DE BATALHAS - INICIANDO...")
    print("=" * 60)
    
    if wait_for_services():
        print("🚀 API rodando na porta 5000")
        print("=" * 60)
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ Falha ao conectar aos serviços!")
