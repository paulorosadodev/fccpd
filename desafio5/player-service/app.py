from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

PLAYERS_DATA = [
    {
        'id': 1,
        'username': 'DragonSlayer99',
        'email': 'dragonslayer@rpgmail.com',
        'level': 45,
        'class': 'Guerreiro',
        'experience': 125000,
        'gold': 50000,
        'guild': 'Ordem dos Cavaleiros',
        'created_at': '2020-03-15T10:30:00',
        'last_login': '2025-11-13T14:22:00',
        'status': 'online'
    },
    {
        'id': 2,
        'username': 'MageMaster',
        'email': 'mage@arcanemail.com',
        'level': 52,
        'class': 'Arquimago',
        'experience': 180000,
        'gold': 75000,
        'guild': 'Círculo dos Magos',
        'created_at': '2019-11-20T08:15:00',
        'last_login': '2025-11-13T16:45:00',
        'status': 'online'
    },
    {
        'id': 3,
        'username': 'ShadowHunter',
        'email': 'shadow@stealthmail.com',
        'level': 38,
        'class': 'Assassino',
        'experience': 95000,
        'gold': 35000,
        'guild': 'Irmandade dos Assassinos',
        'created_at': '2021-05-10T12:00:00',
        'last_login': '2025-11-12T20:30:00',
        'status': 'offline'
    },
    {
        'id': 4,
        'username': 'NatureGuardian',
        'email': 'nature@druidmail.com',
        'level': 41,
        'class': 'Druida',
        'experience': 110000,
        'gold': 42000,
        'guild': 'Clã dos Bárbaros',
        'created_at': '2020-09-25T15:45:00',
        'last_login': '2025-11-13T10:15:00',
        'status': 'online'
    },
    {
        'id': 5,
        'username': 'ElvenArcher',
        'email': 'elf@archermail.com',
        'level': 48,
        'class': 'Ranger',
        'experience': 150000,
        'gold': 60000,
        'guild': 'Aliança dos Elfos',
        'created_at': '2020-01-10T09:20:00',
        'last_login': '2025-11-13T18:00:00',
        'status': 'online'
    },
    {
        'id': 6,
        'username': 'HolyPaladin',
        'email': 'holy@paladinmail.com',
        'level': 44,
        'class': 'Paladino',
        'experience': 135000,
        'gold': 55000,
        'guild': 'Ordem dos Cavaleiros',
        'created_at': '2020-04-18T11:30:00',
        'last_login': '2025-11-13T12:00:00',
        'status': 'online'
    }
]

@app.route('/')
def home():
    return jsonify({
        'service': 'Player Service',
        'version': '1.0.0',
        'description': 'Microsserviço de gerenciamento de jogadores',
        'endpoints': {
            '/players': 'Lista todos os jogadores',
            '/players/<id>': 'Detalhes de um jogador específico',
            '/players/<id>/stats': 'Estatísticas de um jogador',
            '/health': 'Health check do serviço'
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'player-service',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/players')
def get_players():
    return jsonify({
        'total': len(PLAYERS_DATA),
        'players': PLAYERS_DATA
    }), 200

@app.route('/players/<int:player_id>')
def get_player(player_id):
    player = next((p for p in PLAYERS_DATA if p['id'] == player_id), None)
    
    if not player:
        return jsonify({'error': 'Jogador não encontrado'}), 404
    
    return jsonify(player), 200

@app.route('/players/<int:player_id>/stats')
def get_player_stats(player_id):
    player = next((p for p in PLAYERS_DATA if p['id'] == player_id), None)
    
    if not player:
        return jsonify({'error': 'Jogador não encontrado'}), 404
    
    stats = {
        'player_id': player_id,
        'username': player['username'],
        'level': player['level'],
        'experience': player['experience'],
        'experience_to_next_level': (player['level'] + 1) * 3000 - player['experience'],
        'gold': player['gold'],
        'class': player['class'],
        'guild': player['guild'],
        'status': player['status']
    }
    
    return jsonify(stats), 200

if __name__ == '__main__':
    print("=" * 60)
    print("👤 PLAYER SERVICE - Microsserviço de Jogadores")
    print("=" * 60)
    print("🚀 Serviço rodando na porta 8002")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8002, debug=False)
