from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

GUILDS_DATA = [
    {
        'id': 1,
        'name': 'Ordem dos Cavaleiros Sagrados',
        'founded_date': '2020-01-15',
        'members': [
            {'id': 101, 'name': 'Sir Lancelot', 'class': 'Paladino', 'level': 45, 'joined_date': '2020-01-20'},
            {'id': 102, 'name': 'Lady Guinevere', 'class': 'Clérigo', 'level': 42, 'joined_date': '2020-02-10'},
            {'id': 103, 'name': 'Galahad o Puro', 'class': 'Cavaleiro', 'level': 38, 'joined_date': '2020-03-05'},
            {'id': 104, 'name': 'Percival Destemido', 'class': 'Guerreiro', 'level': 40, 'joined_date': '2020-04-12'}
        ],
        'guild_level': 85,
        'total_quests_completed': 1247,
        'reputation': 'Lendária'
    },
    {
        'id': 2,
        'name': 'Círculo dos Magos Arcanos',
        'founded_date': '2019-11-22',
        'members': [
            {'id': 201, 'name': 'Merlin o Sábio', 'class': 'Arquimago', 'level': 50, 'joined_date': '2019-11-25'},
            {'id': 202, 'name': 'Morgana das Sombras', 'class': 'Necromante', 'level': 48, 'joined_date': '2019-12-01'},
            {'id': 203, 'name': 'Gandalf Cinzento', 'class': 'Mago', 'level': 46, 'joined_date': '2020-01-08'},
            {'id': 204, 'name': 'Saruman o Branco', 'class': 'Mago', 'level': 44, 'joined_date': '2020-02-15'},
            {'id': 205, 'name': 'Radagast o Marrom', 'class': 'Druida', 'level': 41, 'joined_date': '2020-03-20'}
        ],
        'guild_level': 92,
        'total_quests_completed': 2156,
        'reputation': 'Mítica'
    },
    {
        'id': 3,
        'name': 'Irmandade dos Assassinos',
        'founded_date': '2021-05-10',
        'members': [
            {'id': 301, 'name': 'Altair Ibn-La-Ahad', 'class': 'Assassino', 'level': 47, 'joined_date': '2021-05-12'},
            {'id': 302, 'name': 'Ezio Auditore', 'class': 'Ladino', 'level': 45, 'joined_date': '2021-06-01'},
            {'id': 303, 'name': 'Connor Kenway', 'class': 'Ranger', 'level': 43, 'joined_date': '2021-07-10'},
            {'id': 304, 'name': 'Edward Kenway', 'class': 'Corsário', 'level': 44, 'joined_date': '2021-08-05'}
        ],
        'guild_level': 78,
        'total_quests_completed': 892,
        'reputation': 'Épica'
    },
    {
        'id': 4,
        'name': 'Clã dos Bárbaros do Norte',
        'founded_date': '2020-08-30',
        'members': [
            {'id': 401, 'name': 'Conan o Bárbaro', 'class': 'Bárbaro', 'level': 49, 'joined_date': '2020-09-01'},
            {'id': 402, 'name': 'Thorin Escudo de Carvalho', 'class': 'Anão Guerreiro', 'level': 46, 'joined_date': '2020-09-15'},
            {'id': 403, 'name': 'Gimli Filho de Glóin', 'class': 'Anão', 'level': 44, 'joined_date': '2020-10-20'},
            {'id': 404, 'name': 'Dwalin o Destemido', 'class': 'Guerreiro', 'level': 42, 'joined_date': '2020-11-10'}
        ],
        'guild_level': 88,
        'total_quests_completed': 1567,
        'reputation': 'Lendária'
    },
    {
        'id': 5,
        'name': 'Aliança dos Elfos Silvestres',
        'founded_date': '2019-03-14',
        'members': [
            {'id': 501, 'name': 'Legolas Folha Verde', 'class': 'Arqueiro Élfico', 'level': 48, 'joined_date': '2019-03-15'},
            {'id': 502, 'name': 'Arwen Undómiel', 'class': 'Elfa Nobre', 'level': 46, 'joined_date': '2019-04-01'},
            {'id': 503, 'name': 'Galadriel a Sábia', 'class': 'Elfa Mágica', 'level': 50, 'joined_date': '2019-05-10'},
            {'id': 504, 'name': 'Thranduil Rei dos Elfos', 'class': 'Elfo Real', 'level': 49, 'joined_date': '2019-06-20'},
            {'id': 505, 'name': 'Haldir de Lórien', 'class': 'Guarda Élfico', 'level': 45, 'joined_date': '2019-08-15'}
        ],
        'guild_level': 95,
        'total_quests_completed': 2890,
        'reputation': 'Mítica'
    }
]

@app.route('/')
def home():
    return jsonify({
        'service': 'Guild Service',
        'version': '1.0.0',
        'description': 'Microsserviço de gerenciamento de guildas',
        'endpoints': {
            '/guilds': 'Lista todas as guildas',
            '/guilds/<id>': 'Detalhes de uma guilda específica',
            '/guilds/<id>/members': 'Membros de uma guilda',
            '/health': 'Health check do serviço'
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'guild-service',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/guilds')
def get_guilds():
    return jsonify({
        'total': len(GUILDS_DATA),
        'guilds': GUILDS_DATA
    }), 200

@app.route('/guilds/<int:guild_id>')
def get_guild(guild_id):
    guild = next((g for g in GUILDS_DATA if g['id'] == guild_id), None)
    
    if not guild:
        return jsonify({'error': 'Guilda não encontrada'}), 404
    
    return jsonify(guild), 200

@app.route('/guilds/<int:guild_id>/members')
def get_guild_members(guild_id):
    guild = next((g for g in GUILDS_DATA if g['id'] == guild_id), None)
    
    if not guild:
        return jsonify({'error': 'Guilda não encontrada'}), 404
    
    return jsonify({
        'guild_id': guild_id,
        'guild_name': guild['name'],
        'total_members': len(guild['members']),
        'members': guild['members']
    }), 200

@app.route('/guilds/<int:guild_id>/stats')
def get_guild_stats(guild_id):
    guild = next((g for g in GUILDS_DATA if g['id'] == guild_id), None)
    
    if not guild:
        return jsonify({'error': 'Guilda não encontrada'}), 404
    
    total_levels = sum(m['level'] for m in guild['members'])
    avg_level = total_levels / len(guild['members']) if guild['members'] else 0
    
    classes_count = {}
    for member in guild['members']:
        classes_count[member['class']] = classes_count.get(member['class'], 0) + 1
    
    return jsonify({
        'guild_id': guild_id,
        'guild_name': guild['name'],
        'stats': {
            'total_members': len(guild['members']),
            'average_level': round(avg_level, 2),
            'guild_level': guild['guild_level'],
            'total_quests': guild['total_quests_completed'],
            'reputation': guild['reputation'],
            'classes_distribution': classes_count
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🏰 GUILD SERVICE - Microsserviço de Guildas")
    print("=" * 60)
    print("🚀 Serviço rodando na porta 8000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000, debug=False)
