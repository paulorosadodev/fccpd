from flask import Flask, jsonify, request
from datetime import datetime
import socket
import random

app = Flask(__name__)

player_xp = 0
player_level = 1
request_count = 0

def calculate_level(xp):
    return (xp // 100) + 1

def get_title(level):
    titles = {
        1: "🌱 Novato das Requisições",
        5: "⚔️ Guerreiro HTTP",
        10: "🛡️ Guardião dos Endpoints",
        15: "🔥 Mestre do Curl",
        20: "⚡ Senhor das APIs",
        25: "🌟 Lendário Docker",
        30: "👑 Rei das Requisições",
        40: "🏆 Campeão dos Containers",
        50: "💎 Deus das Conexões",
        75: "🌌 Transcendente Digital",
        100: "∞ Entidade Cósmica da Rede"
    }
    
    for req_level in sorted(titles.keys(), reverse=True):
        if level >= req_level:
            return titles[req_level]
    return titles[1]

def get_xp_reward():
    base_xp = random.randint(15, 30)
    is_critical = random.random() < 0.1  
    
    if is_critical:
        return base_xp * 2, True
    return base_xp, False

def get_motivational_message(level):
    messages = [
        "Continue assim, aventureiro! 💪",
        "Você está ficando mais forte! 🚀",
        "Excelente progresso! ⭐",
        "Suas habilidades estão melhorando! 📈",
        "O poder das requisições flui em você! ✨",
        "Imparável! Continue a jornada! 🎯",
        "Cada requisição te leva mais longe! 🌟",
        "A rede reconhece seu poder! ⚡"
    ]
    return random.choice(messages)

@app.route('/')
def home():
    global player_xp, player_level, request_count
    request_count += 1
    
    xp_gained, is_critical = get_xp_reward()
    old_level = player_level
    player_xp += xp_gained
    player_level = calculate_level(player_xp)
    
    leveled_up = player_level > old_level
    
    client_ip = request.remote_addr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hostname = socket.gethostname()
    title = get_title(player_level)
    
    xp_progress = player_xp - ((player_level - 1) * 100)
    
    response_data = {
        'game_status': '🎮 RPG das Requisições HTTP',
        'player_stats': {
            'level': player_level,
            'title': title,
            'total_xp': player_xp,
            'xp_progress': f"{xp_progress}/100 XP",
            'requests_made': request_count
        },
        'this_request': {
            'xp_gained': xp_gained,
            'critical_hit': is_critical,
            'level_up': leveled_up,
            'message': get_motivational_message(player_level)
        },
        'server_info': {
            'hostname': hostname,
            'client_ip': client_ip,
            'timestamp': timestamp
        }
    }

    log_msg = f"[{timestamp}] 🎮 Requisição #{request_count} de {client_ip}"
    if is_critical:
        log_msg += f" | 💥 CRITICAL HIT! +{xp_gained} XP"
    else:
        log_msg += f" | ⚔️ +{xp_gained} XP"
    
    if leveled_up:
        log_msg += f" | 🎊 LEVEL UP! {old_level} → {player_level} | {title}"
    else:
        log_msg += f" | Level {player_level} ({xp_progress}/100 XP)"
    
    print(log_msg)
    
    return jsonify(response_data), 200

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'game_mode': 'active',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/stats')
def stats():
    title = get_title(player_level)
    xp_progress = player_xp - ((player_level - 1) * 100)
    
    return jsonify({
        'game_title': '🎮 RPG das Requisições HTTP - Estatísticas',
        'player': {
            'level': player_level,
            'title': title,
            'total_xp': player_xp,
            'xp_to_next_level': 100 - xp_progress,
            'progress_bar': '█' * (xp_progress // 10) + '░' * (10 - xp_progress // 10),
            'total_requests': request_count,
            'average_xp_per_request': round(player_xp / request_count, 2) if request_count > 0 else 0
        },
        'server': {
            'hostname': socket.gethostname(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🎮 RPG DAS REQUISIÇÕES HTTP - SERVIDOR DE JOGO INICIADO!")
    print("=" * 60)
    print("🏰 Bem-vindo ao mundo das requisições HTTP!")
    print("⚔️  Cada requisição ganha XP e aumenta seu nível")
    print("🏆 Conquiste títulos épicos conforme progride")
    print("💎 10% de chance de CRITICAL HIT (XP em dobro)!")
    print("=" * 60)
    print("🚀 Servidor rodando na porta 8080...")
    print("=" * 60)
    print()
    app.run(host='0.0.0.0', port=8080, debug=False)
