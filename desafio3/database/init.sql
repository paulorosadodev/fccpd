CREATE TABLE IF NOT EXISTS heroes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    class VARCHAR(50) NOT NULL,
    level INTEGER DEFAULT 1,
    attack_power INTEGER NOT NULL,
    defense_power INTEGER NOT NULL,
    health_points INTEGER NOT NULL,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    total_damage_dealt INTEGER DEFAULT 0,
    total_damage_received INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS battles (
    id SERIAL PRIMARY KEY,
    hero1_id INTEGER REFERENCES heroes(id),
    hero2_id INTEGER REFERENCES heroes(id),
    winner_id INTEGER REFERENCES heroes(id),
    hero1_damage_dealt INTEGER NOT NULL,
    hero2_damage_dealt INTEGER NOT NULL,
    rounds INTEGER NOT NULL,
    battle_log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_battles_hero1 ON battles(hero1_id);
CREATE INDEX idx_battles_hero2 ON battles(hero2_id);
CREATE INDEX idx_battles_winner ON battles(winner_id);
CREATE INDEX idx_battles_created ON battles(created_at DESC);

INSERT INTO heroes (name, class, level, attack_power, defense_power, health_points) VALUES
('Dragão Vermelho', 'Monstro', 50, 95, 80, 500),
('Cavaleiro Sagrado', 'Paladino', 45, 85, 90, 450),
('Arquimago Sombrio', 'Mago', 40, 100, 60, 350),
('Bárbaro Furioso', 'Guerreiro', 42, 90, 70, 480),
('Assassino Letal', 'Ladino', 38, 88, 65, 380),
('Druida Anciã', 'Druida', 43, 75, 85, 420),
('Necromante', 'Mago Negro', 44, 92, 68, 400),
('Guardião de Aço', 'Tank', 46, 70, 95, 520);

CREATE OR REPLACE VIEW hero_stats AS
SELECT 
    h.id,
    h.name,
    h.class,
    h.level,
    h.attack_power,
    h.defense_power,
    h.health_points,
    h.wins,
    h.losses,
    h.draws,
    h.total_damage_dealt,
    h.total_damage_received,
    CASE 
        WHEN (h.wins + h.losses + h.draws) = 0 THEN 0
        ELSE ROUND(h.wins::NUMERIC / (h.wins + h.losses + h.draws) * 100, 2)
    END as win_rate,
    (h.wins * 3 + h.draws) as ranking_points
FROM heroes h
ORDER BY ranking_points DESC, wins DESC, total_damage_dealt DESC;

SELECT '⚔️ ARENA DE BATALHAS - DATABASE INITIALIZED!' as status;
SELECT COUNT(*) as total_heroes FROM heroes;
