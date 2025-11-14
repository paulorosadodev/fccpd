from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

PLAYER_SERVICE_URL = 'http://player-service:8002'
ITEM_SERVICE_URL = 'http://item-service:8003'

def call_service(service_url, endpoint, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(f'{service_url}{endpoint}', timeout=5)
        elif method == 'POST':
            response = requests.post(f'{service_url}{endpoint}', json=data, timeout=5)
        else:
            return {'error': f'Método {method} não suportado'}
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f'Erro ao conectar ao serviço: {str(e)}'}

@app.route('/')
def home():
    return jsonify({
        'service': 'API Gateway',
        'version': '1.0.0',
        'description': 'Gateway centralizado para acesso aos microsserviços',
        'endpoints': {
            '/players': 'Lista todos os jogadores (via Player Service)',
            '/players/<id>': 'Detalhes de um jogador (via Player Service)',
            '/items': 'Lista todos os itens (via Item Service)',
            '/items/<id>': 'Detalhes de um item (via Item Service)',
            '/players/<id>/items': 'Itens de um jogador (combina Player + Item Service)',
            '/health': 'Health check de todos os serviços',
            '/stats': 'Estatísticas agregadas'
        }
    }), 200

@app.route('/health')
def health():
    player_health = call_service(PLAYER_SERVICE_URL, '/health')
    item_health = call_service(ITEM_SERVICE_URL, '/health')
    
    gateway_status = 'healthy'
    all_healthy = (
        player_health.get('status') == 'healthy' and
        item_health.get('status') == 'healthy'
    )
    
    return jsonify({
        'gateway': gateway_status,
        'player_service': player_health.get('status', 'unreachable'),
        'item_service': item_health.get('status', 'unreachable'),
        'all_services_healthy': all_healthy,
        'timestamp': datetime.now().isoformat()
    }), 200 if all_healthy else 503

@app.route('/players')
def get_players():
    result = call_service(PLAYER_SERVICE_URL, '/players')
    
    if 'error' in result:
        return jsonify(result), 503
    
    return jsonify({
        'source': 'player-service',
        'gateway_timestamp': datetime.now().isoformat(),
        **result
    }), 200

@app.route('/players/<int:player_id>')
def get_player(player_id):
    result = call_service(PLAYER_SERVICE_URL, f'/players/{player_id}')
    
    if 'error' in result:
        status_code = 404 if 'não encontrado' in result.get('error', '') else 503
        return jsonify(result), status_code
    
    return jsonify({
        'source': 'player-service',
        'gateway_timestamp': datetime.now().isoformat(),
        **result
    }), 200

@app.route('/items')
def get_items():
    result = call_service(ITEM_SERVICE_URL, '/items')
    
    if 'error' in result:
        return jsonify(result), 503
    
    return jsonify({
        'source': 'item-service',
        'gateway_timestamp': datetime.now().isoformat(),
        **result
    }), 200

@app.route('/items/<int:item_id>')
def get_item(item_id):
    result = call_service(ITEM_SERVICE_URL, f'/items/{item_id}')
    
    if 'error' in result:
        status_code = 404 if 'não encontrado' in result.get('error', '') else 503
        return jsonify(result), status_code
    
    return jsonify({
        'source': 'item-service',
        'gateway_timestamp': datetime.now().isoformat(),
        **result
    }), 200

@app.route('/players/<int:player_id>/items')
def get_player_with_items(player_id):
    player_result = call_service(PLAYER_SERVICE_URL, f'/players/{player_id}')
    
    if 'error' in player_result:
        status_code = 404 if 'não encontrado' in player_result.get('error', '') else 503
        return jsonify(player_result), status_code
    
    items_result = call_service(ITEM_SERVICE_URL, f'/items/player/{player_id}')
    
    if 'error' in items_result:
        items_result = {'total_items': 0, 'items': []}
    
    return jsonify({
        'player': player_result,
        'items': items_result.get('items', []),
        'total_items': items_result.get('total_items', 0),
        'gateway_timestamp': datetime.now().isoformat(),
        'orchestrated_by': 'api-gateway'
    }), 200

@app.route('/stats')
def get_stats():
    players_result = call_service(PLAYER_SERVICE_URL, '/players')
    items_result = call_service(ITEM_SERVICE_URL, '/items')
    
    stats = {
        'generated_at': datetime.now().isoformat(),
        'summary': {}
    }
    
    if 'error' not in players_result:
        players = players_result.get('players', [])
        total_gold = sum(p.get('gold', 0) for p in players)
        avg_level = sum(p.get('level', 0) for p in players) / len(players) if players else 0
        online_count = sum(1 for p in players if p.get('status') == 'online')
        
        stats['summary']['players'] = {
            'total': len(players),
            'online': online_count,
            'offline': len(players) - online_count,
            'total_gold': total_gold,
            'average_level': round(avg_level, 2)
        }
    
    if 'error' not in items_result:
        items = items_result.get('items', [])
        total_value = sum(i.get('price', 0) for i in items)
        rarity_count = {}
        for item in items:
            rarity = item.get('rarity', 'Unknown')
            rarity_count[rarity] = rarity_count.get(rarity, 0) + 1
        
        stats['summary']['items'] = {
            'total': len(items),
            'total_value': total_value,
            'rarity_distribution': rarity_count
        }
    
    return jsonify(stats), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🚪 API GATEWAY - Ponto Único de Entrada")
    print("=" * 60)
    print(f"🔗 Player Service: {PLAYER_SERVICE_URL}")
    print(f"🔗 Item Service: {ITEM_SERVICE_URL}")
    print("🚀 Gateway rodando na porta 8000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000, debug=False)
