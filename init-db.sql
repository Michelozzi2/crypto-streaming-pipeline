-- Script d'initialisation de la base PostgreSQL
-- Création des tables pour stocker les données crypto

-- Table pour les données brutes (raw)
CREATE TABLE IF NOT EXISTS crypto_raw (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    price_usd DECIMAL(20, 8),
    volume_24h DECIMAL(20, 2),
    market_cap_usd DECIMAL(20, 2),
    change_percent_24h DECIMAL(10, 4),
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_symbol_timestamp UNIQUE (symbol, timestamp)
);

-- Index pour améliorer les performances de requêtes
CREATE INDEX idx_crypto_raw_symbol ON crypto_raw(symbol);
CREATE INDEX idx_crypto_raw_timestamp ON crypto_raw(timestamp);
CREATE INDEX idx_crypto_raw_created_at ON crypto_raw(created_at);

-- Table pour les données agrégées par 5 minutes
CREATE TABLE IF NOT EXISTS crypto_aggregated_5m (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    price_open DECIMAL(20, 8),
    price_close DECIMAL(20, 8),
    price_high DECIMAL(20, 8),
    price_low DECIMAL(20, 8),
    price_avg DECIMAL(20, 8),
    volume_total DECIMAL(20, 2),
    trade_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_symbol_window UNIQUE (symbol, window_start)
);

CREATE INDEX idx_crypto_agg_5m_symbol ON crypto_aggregated_5m(symbol);
CREATE INDEX idx_crypto_agg_5m_window_start ON crypto_aggregated_5m(window_start);

-- Table pour les alertes (variations importantes)
CREATE TABLE IF NOT EXISTS crypto_alerts (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    alert_type VARCHAR(50) NOT NULL, -- 'price_spike', 'price_drop', 'volume_spike'
    current_value DECIMAL(20, 8),
    previous_value DECIMAL(20, 8),
    change_percent DECIMAL(10, 4),
    threshold_percent DECIMAL(10, 4),
    message TEXT,
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crypto_alerts_symbol ON crypto_alerts(symbol);
CREATE INDEX idx_crypto_alerts_created_at ON crypto_alerts(created_at);
CREATE INDEX idx_crypto_alerts_type ON crypto_alerts(alert_type);

-- Table pour les moyennes mobiles
CREATE TABLE IF NOT EXISTS crypto_moving_averages (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    ma_5m DECIMAL(20, 8),   -- Moyenne mobile 5 minutes
    ma_15m DECIMAL(20, 8),  -- Moyenne mobile 15 minutes
    ma_1h DECIMAL(20, 8),   -- Moyenne mobile 1 heure
    ma_4h DECIMAL(20, 8),   -- Moyenne mobile 4 heures
    current_price DECIMAL(20, 8),
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_ma_symbol_timestamp UNIQUE (symbol, timestamp)
);

CREATE INDEX idx_crypto_ma_symbol ON crypto_moving_averages(symbol);
CREATE INDEX idx_crypto_ma_timestamp ON crypto_moving_averages(timestamp);

-- Table pour les métadonnées des cryptos
CREATE TABLE IF NOT EXISTS crypto_metadata (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100),
    rank INTEGER,
    supply DECIMAL(30, 8),
    max_supply DECIMAL(30, 8),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vue pour les données récentes (dernière heure)
CREATE OR REPLACE VIEW crypto_recent AS
SELECT 
    symbol,
    price_usd,
    volume_24h,
    market_cap_usd,
    change_percent_24h,
    timestamp,
    to_timestamp(timestamp/1000) as datetime
FROM crypto_raw
WHERE created_at > NOW() - INTERVAL '1 hour'
ORDER BY created_at DESC;

-- Vue pour le résumé par crypto
CREATE OR REPLACE VIEW crypto_summary AS
SELECT 
    symbol,
    COUNT(*) as data_points,
    MIN(price_usd) as min_price,
    MAX(price_usd) as max_price,
    AVG(price_usd) as avg_price,
    MIN(created_at) as first_seen,
    MAX(created_at) as last_seen
FROM crypto_raw
GROUP BY symbol;

-- Fonction pour nettoyer les données anciennes (> 30 jours)
CREATE OR REPLACE FUNCTION cleanup_old_data()
RETURNS void AS $$
BEGIN
    DELETE FROM crypto_raw WHERE created_at < NOW() - INTERVAL '30 days';
    DELETE FROM crypto_aggregated_5m WHERE created_at < NOW() - INTERVAL '30 days';
    DELETE FROM crypto_alerts WHERE created_at < NOW() - INTERVAL '30 days';
    DELETE FROM crypto_moving_averages WHERE created_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- Informations sur les tables créées
DO $$
BEGIN
    RAISE NOTICE 'Base de données crypto_data initialisée avec succès!';
    RAISE NOTICE 'Tables créées:';
    RAISE NOTICE '  - crypto_raw: données brutes';
    RAISE NOTICE '  - crypto_aggregated_5m: agrégations 5 minutes';
    RAISE NOTICE '  - crypto_alerts: alertes de variations';
    RAISE NOTICE '  - crypto_moving_averages: moyennes mobiles';
    RAISE NOTICE '  - crypto_metadata: métadonnées des cryptos';
END $$;
