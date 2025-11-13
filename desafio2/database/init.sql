CREATE TABLE IF NOT EXISTS heroes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(50) NOT NULL,
    level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    health_points INTEGER DEFAULT 100,
    mana_points INTEGER DEFAULT 50,
    gold INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    reward_xp INTEGER NOT NULL,
    reward_gold INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    hero_id INTEGER REFERENCES heroes(id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    quantity INTEGER DEFAULT 1,
    power INTEGER DEFAULT 0,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS achievements (
    id SERIAL PRIMARY KEY,
    hero_id INTEGER REFERENCES heroes(id) ON DELETE CASCADE,
    achievement_name VARCHAR(100) NOT NULL,
    achievement_description TEXT,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO heroes (name, class, level, experience, health_points, mana_points, gold) VALUES
('Aragorn o Bravo', 'Guerreiro', 15, 2250, 180, 30, 1500),
('Gandalf o Sábio', 'Mago', 25, 6000, 120, 250, 3000),
('Legolas Arqueiro', 'Ranger', 18, 3100, 140, 80, 2000),
('Thalia Curandeira', 'Clérigo', 12, 1500, 110, 180, 1200),
('Thorin Machado', 'Anão Guerreiro', 20, 4500, 200, 40, 2500);

INSERT INTO quests (title, description, difficulty, reward_xp, reward_gold, status) VALUES
('Defesa da Vila', 'Proteja a vila dos goblins invasores', 'Fácil', 150, 100, 'available'),
('O Tesouro Perdido', 'Encontre o tesouro escondido nas Minas Antigas', 'Médio', 500, 500, 'available'),
('Dragão das Montanhas', 'Derrote o temível dragão que aterroriza o reino', 'Difícil', 2000, 5000, 'available'),
('Resgate Real', 'Resgate a princesa capturada pelo bruxo maligno', 'Médio', 800, 1000, 'in_progress'),
('Caçada aos Lobos', 'Elimine a alcateia que ameaça os viajantes', 'Fácil', 200, 150, 'completed');

INSERT INTO inventory (hero_id, item_name, item_type, quantity, power) VALUES
(1, 'Espada de Aço Élfico', 'Arma', 1, 85),
(1, 'Escudo de Mithril', 'Escudo', 1, 60),
(1, 'Poção de Vida', 'Consumível', 5, 50),
(2, 'Cajado dos Anciões', 'Arma', 1, 120),
(2, 'Manto Místico', 'Armadura', 1, 70),
(2, 'Grimório de Feitiços Arcanos', 'Livro', 1, 100),
(2, 'Poção de Mana', 'Consumível', 8, 75),
(3, 'Arco Longo Élfico', 'Arma', 1, 95),
(3, 'Flechas Encantadas', 'Munição', 50, 15),
(3, 'Capa da Invisibilidade', 'Armadura', 1, 40);

INSERT INTO achievements (hero_id, achievement_name, achievement_description) VALUES
(1, '🏆 Primeira Vitória', 'Venceu sua primeira batalha'),
(1, '⚔️ Matador de Dragões', 'Derrotou um dragão'),
(2, '📚 Mestre dos Feitiços', 'Aprendeu 50 feitiços diferentes'),
(2, '🌟 Sábio da Taverna', 'Alcançou nível 25'),
(3, '🎯 Olho de Águia', 'Acertou 100 tiros críticos'),
(5, '💎 Caçador de Tesouros', 'Encontrou 10 tesouros lendários');

CREATE OR REPLACE VIEW hero_ranking AS
SELECT 
    name,
    class,
    level,
    experience,
    gold,
    RANK() OVER (ORDER BY level DESC, experience DESC) as ranking
FROM heroes
ORDER BY level DESC, experience DESC;

CREATE OR REPLACE VIEW tavern_stats AS
SELECT 
    COUNT(*) as total_heroes,
    AVG(level)::NUMERIC(10,2) as average_level,
    SUM(gold) as total_gold,
    MAX(level) as highest_level,
    (SELECT COUNT(*) FROM quests WHERE status = 'available') as available_quests,
    (SELECT COUNT(*) FROM quests WHERE status = 'completed') as completed_quests
FROM heroes;

SELECT '🏰 TAVERNA DOS HERÓIS - DATABASE INITIALIZED!' as status;
SELECT * FROM tavern_stats;
