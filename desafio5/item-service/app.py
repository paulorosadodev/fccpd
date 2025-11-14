from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

ITEMS_DATA = [
    {
        'id': 1,
        'name': 'Espada Lendária do Dragão',
        'type': 'Arma',
        'rarity': 'Lendária',
        'power': 95,
        'price': 50000,
        'owner_id': 1,
        'purchased_at': '2023-06-15T10:00:00',
        'status': 'equipped'
    },
    {
        'id': 2,
        'name': 'Cajado dos Anciões',
        'type': 'Arma',
        'rarity': 'Épica',
        'power': 88,
        'price': 45000,
        'owner_id': 2,
        'purchased_at': '2023-08-20T14:30:00',
        'status': 'equipped'
    },
    {
        'id': 3,
        'name': 'Adagas das Sombras',
        'type': 'Arma',
        'rarity': 'Rara',
        'power': 75,
        'price': 30000,
        'owner_id': 3,
        'purchased_at': '2024-01-10T09:15:00',
        'status': 'equipped'
    },
    {
        'id': 4,
        'name': 'Armadura de Mithril',
        'type': 'Armadura',
        'rarity': 'Épica',
        'power': 82,
        'price': 40000,
        'owner_id': 1,
        'purchased_at': '2023-07-05T11:20:00',
        'status': 'equipped'
    },
    {
        'id': 5,
        'name': 'Manto Místico',
        'type': 'Armadura',
        'rarity': 'Lendária',
        'power': 90,
        'price': 55000,
        'owner_id': 2,
        'purchased_at': '2023-09-12T16:45:00',
        'status': 'equipped'
    },
    {
        'id': 6,
        'name': 'Poção de Vida Superior',
        'type': 'Consumível',
        'rarity': 'Comum',
        'power': 50,
        'price': 500,
        'owner_id': 4,
        'purchased_at': '2025-11-10T10:00:00',
        'status': 'inventory'
    },
    {
        'id': 7,
        'name': 'Anel de Poder',
        'type': 'Acessório',
        'rarity': 'Rara',
        'power': 65,
        'price': 25000,
        'owner_id': 5,
        'purchased_at': '2024-03-18T13:30:00',
        'status': 'equipped'
    },
    {
        'id': 8,
        'name': 'Escudo do Guardião',
        'type': 'Escudo',
        'rarity': 'Épica',
        'power': 78,
        'price': 38000,
        'owner_id': 6,
        'purchased_at': '2023-11-25T15:00:00',
        'status': 'equipped'
    },
    {
        'id': 9,
        'name': 'Arco Longo Élfico',
        'type': 'Arma',
        'rarity': 'Rara',
        'power': 80,
        'price': 35000,
        'owner_id': 5,
        'purchased_at': '2024-02-14T12:00:00',
        'status': 'equipped'
    },
    {
        'id': 10,
        'name': 'Grimório de Feitiços Arcanos',
        'type': 'Livro',
        'rarity': 'Lendária',
        'power': 92,
        'price': 60000,
        'owner_id': 2,
        'purchased_at': '2023-10-30T09:00:00',
        'status': 'equipped'
    }
]

@app.route('/')
def home():
    return jsonify({
        'service': 'Item Service',
        'version': '1.0.0',
        'description': 'Microsserviço de gerenciamento de itens e equipamentos',
        'endpoints': {
            '/items': 'Lista todos os itens',
            '/items/<id>': 'Detalhes de um item específico',
            '/items/player/<player_id>': 'Itens de um jogador',
            '/items/type/<type>': 'Itens por tipo',
            '/health': 'Health check do serviço'
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'item-service',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/items')
def get_items():
    return jsonify({
        'total': len(ITEMS_DATA),
        'items': ITEMS_DATA
    }), 200

@app.route('/items/<int:item_id>')
def get_item(item_id):
    item = next((i for i in ITEMS_DATA if i['id'] == item_id), None)
    
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    
    return jsonify(item), 200

@app.route('/items/player/<int:player_id>')
def get_player_items(player_id):
    player_items = [item for item in ITEMS_DATA if item['owner_id'] == player_id]
    
    return jsonify({
        'player_id': player_id,
        'total_items': len(player_items),
        'items': player_items
    }), 200

@app.route('/items/type/<type>')
def get_items_by_type(type):
    items_by_type = [item for item in ITEMS_DATA if item['type'].lower() == type.lower()]
    
    return jsonify({
        'type': type,
        'total': len(items_by_type),
        'items': items_by_type
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("⚔️ ITEM SERVICE - Microsserviço de Itens")
    print("=" * 60)
    print("🚀 Serviço rodando na porta 8003")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8003, debug=False)
