from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
from dateutil import parser

app = Flask(__name__)

GUILD_SERVICE_URL = 'http://guild-service:8000'

def get_guild_service_data(endpoint):
    try:
        response = requests.get(f'{GUILD_SERVICE_URL}{endpoint}', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao conectar ao Guild Service: {str(e)}'}

@app.route('/')
def home():
    return jsonify({
        'service': 'Guild Reporter',
        'version': '1.0.0',
        'description': 'Microsserviço que consome Guild Service e gera relatórios combinados',
        'guild_service_url': GUILD_SERVICE_URL,
        'endpoints': {
            '/report': 'Relatório completo de todas as guildas',
            '/report/<guild_id>': 'Relatório detalhado de uma guilda',
            '/summary': 'Resumo executivo das guildas',
            '/activity': 'Análise de atividade das guildas',
            '/health': 'Health check (inclui verificação do Guild Service)'
        }
    }), 200

@app.route('/health')
def health():
    guild_service_health = get_guild_service_data('/health')
    
    return jsonify({
        'reporter_status': 'healthy',
        'guild_service_status': guild_service_health.get('status', 'unreachable'),
        'timestamp': datetime.now().isoformat()
    }), 200 if guild_service_health.get('status') == 'healthy' else 503

@app.route('/report')
def get_full_report():
    guilds_data = get_guild_service_data('/guilds')
    
    if 'error' in guilds_data:
        return jsonify(guilds_data), 503
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_guilds': guilds_data.get('total', 0),
        'guilds_report': []
    }
    
    for guild in guilds_data.get('guilds', []):
        guild_id = guild['id']
        
        founded_date = parser.parse(guild['founded_date'])
        days_active = (datetime.now() - founded_date).days
        
        total_members = len(guild['members'])
        total_levels = sum(m['level'] for m in guild['members'])
        avg_level = total_levels / total_members if total_members > 0 else 0
        
        guild_report = {
            'guild_id': guild_id,
            'guild_name': guild['name'],
            'status': f"Ativa há {days_active} dias",
            'founded_date': guild['founded_date'],
            'days_active': days_active,
            'members_summary': {
                'total': total_members,
                'average_level': round(avg_level, 2),
                'highest_level': max((m['level'] for m in guild['members']), default=0),
                'lowest_level': min((m['level'] for m in guild['members']), default=0)
            },
            'guild_stats': {
                'level': guild['guild_level'],
                'reputation': guild['reputation'],
                'quests_completed': guild['total_quests_completed'],
                'quests_per_member': round(guild['total_quests_completed'] / total_members, 2) if total_members > 0 else 0
            },
            'members': []
        }
        
        for member in guild['members']:
            joined_date = parser.parse(member['joined_date'])
            days_member = (datetime.now() - joined_date).days
            
            guild_report['members'].append({
                'name': member['name'],
                'class': member['class'],
                'level': member['level'],
                'status': f"Membro há {days_member} dias",
                'joined_date': member['joined_date'],
                'days_as_member': days_member
            })
        
        report['guilds_report'].append(guild_report)
    
    return jsonify(report), 200

@app.route('/report/<int:guild_id>')
def get_guild_report(guild_id):
    guild_data = get_guild_service_data(f'/guilds/{guild_id}')
    
    if 'error' in guild_data:
        return jsonify(guild_data), 404 if 'não encontrada' in guild_data.get('error', '') else 503
    
    founded_date = parser.parse(guild_data['founded_date'])
    days_active = (datetime.now() - founded_date).days
    
    total_members = len(guild_data['members'])
    total_levels = sum(m['level'] for m in guild_data['members'])
    avg_level = total_levels / total_members if total_members > 0 else 0
    
    classes_distribution = {}
    for member in guild_data['members']:
        classes_distribution[member['class']] = classes_distribution.get(member['class'], 0) + 1
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'guild_id': guild_id,
        'guild_name': guild_data['name'],
        'overview': {
            'status': f"Guilda ativa há {days_active} dias",
            'founded': guild_data['founded_date'],
            'reputation': guild_data['reputation'],
            'guild_level': guild_data['guild_level']
        },
        'members_analysis': {
            'total_members': total_members,
            'average_level': round(avg_level, 2),
            'level_range': {
                'min': min((m['level'] for m in guild_data['members']), default=0),
                'max': max((m['level'] for m in guild_data['members']), default=0)
            },
            'classes_distribution': classes_distribution
        },
        'activity_metrics': {
            'total_quests_completed': guild_data['total_quests_completed'],
            'quests_per_member': round(guild_data['total_quests_completed'] / total_members, 2) if total_members > 0 else 0,
            'quests_per_day': round(guild_data['total_quests_completed'] / days_active, 2) if days_active > 0 else 0
        },
        'members_detail': []
    }
    
    for member in guild_data['members']:
        joined_date = parser.parse(member['joined_date'])
        days_member = (datetime.now() - joined_date).days
        
        report['members_detail'].append({
            'name': member['name'],
            'class': member['class'],
            'level': member['level'],
            'membership': {
                'joined_date': member['joined_date'],
                'days_as_member': days_member,
                'status': f"Membro há {days_member} dias"
            }
        })
    
    return jsonify(report), 200

@app.route('/summary')
def get_summary():
    guilds_data = get_guild_service_data('/guilds')
    
    if 'error' in guilds_data:
        return jsonify(guilds_data), 503
    
    total_members = 0
    total_quests = 0
    total_guild_level = 0
    reputation_count = {}
    
    for guild in guilds_data.get('guilds', []):
        total_members += len(guild['members'])
        total_quests += guild['total_quests_completed']
        total_guild_level += guild['guild_level']
        reputation_count[guild['reputation']] = reputation_count.get(guild['reputation'], 0) + 1
    
    avg_guild_level = total_guild_level / len(guilds_data.get('guilds', [])) if guilds_data.get('guilds') else 0
    
    summary = {
        'generated_at': datetime.now().isoformat(),
        'overview': {
            'total_guilds': guilds_data.get('total', 0),
            'total_members': total_members,
            'average_members_per_guild': round(total_members / guilds_data.get('total', 1), 2),
            'total_quests_completed': total_quests,
            'average_guild_level': round(avg_guild_level, 2)
        },
        'reputation_distribution': reputation_count,
        'top_guilds': {
            'by_level': sorted(
                [{'id': g['id'], 'name': g['name'], 'level': g['guild_level']} 
                for g in guilds_data.get('guilds', [])],
                key=lambda x: x['level'],
                reverse=True
            )[:3],
            'by_quests': sorted(
                [{'id': g['id'], 'name': g['name'], 'quests': g['total_quests_completed']} 
                for g in guilds_data.get('guilds', [])],
                key=lambda x: x['quests'],
                reverse=True
            )[:3]
        }
    }
    
    return jsonify(summary), 200

@app.route('/activity')
def get_activity_analysis():
    guilds_data = get_guild_service_data('/guilds')
    
    if 'error' in guilds_data:
        return jsonify(guilds_data), 503
    
    activity_report = {
        'generated_at': datetime.now().isoformat(),
        'guilds_activity': []
    }
    
    for guild in guilds_data.get('guilds', []):
        founded_date = parser.parse(guild['founded_date'])
        days_active = (datetime.now() - founded_date).days
        
        activity_score = round(
            (guild['total_quests_completed'] / days_active) * (guild['guild_level'] / 100),
            2
        ) if days_active > 0 else 0
        
        activity_report['guilds_activity'].append({
            'guild_id': guild['id'],
            'guild_name': guild['name'],
            'days_active': days_active,
            'total_quests': guild['total_quests_completed'],
            'quests_per_day': round(guild['total_quests_completed'] / days_active, 2) if days_active > 0 else 0,
            'activity_score': activity_score,
            'status': 'Muito Ativa' if activity_score > 10 else 'Ativa' if activity_score > 5 else 'Moderada'
        })
    
    activity_report['guilds_activity'].sort(key=lambda x: x['activity_score'], reverse=True)
    
    return jsonify(activity_report), 200

if __name__ == '__main__':
    print("=" * 60)
    print("📊 GUILD REPORTER - Microsserviço de Relatórios")
    print("=" * 60)
    print(f"🔗 Conectando ao Guild Service: {GUILD_SERVICE_URL}")
    print("🚀 Serviço rodando na porta 8001")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8001, debug=False)
