-- Script d'initialisation de ClickHouse
-- Base de données optimisée pour les time-series

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS crypto;

-- Table principale pour les données time-series
-- Utilise MergeTree engine optimisé pour l'insertion et les requêtes analytiques
CREATE TABLE IF NOT EXISTS crypto.prices (
    symbol String,
    price Float64,
    volume_24h Float64,
    market_cap Float64,
    change_percent_24h Float32,
    timestamp DateTime64(3),
    ingestion_time DateTime DEFAULT now()
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (symbol, timestamp)
TTL timestamp + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

-- Table pour les agrégations OHLC (Open, High, Low, Close)
CREATE TABLE IF NOT EXISTS crypto.ohlc_5m (
    symbol String,
    window_start DateTime,
    price_open Float64,
    price_high Float64,
    price_low Float64,
    price_close Float64,
    volume_sum Float64,
    trade_count UInt32,
    price_avg Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(window_start)
ORDER BY (symbol, window_start)
TTL window_start + INTERVAL 90 DAY;

-- Table pour les moyennes mobiles
CREATE TABLE IF NOT EXISTS crypto.moving_averages (
    symbol String,
    timestamp DateTime,
    ma_5m Float64,
    ma_15m Float64,
    ma_1h Float64,
    ma_4h Float64,
    price Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (symbol, timestamp)
TTL timestamp + INTERVAL 90 DAY;

-- Vue matérialisée pour les agrégations en temps réel (5 minutes)
CREATE MATERIALIZED VIEW IF NOT EXISTS crypto.ohlc_5m_mv
TO crypto.ohlc_5m
AS SELECT
    symbol,
    toStartOfInterval(timestamp, INTERVAL 5 MINUTE) as window_start,
    argMin(price, timestamp) as price_open,
    max(price) as price_high,
    min(price) as price_low,
    argMax(price, timestamp) as price_close,
    sum(volume_24h) as volume_sum,
    count() as trade_count,
    avg(price) as price_avg
FROM crypto.prices
GROUP BY symbol, window_start;

-- Vue matérialisée pour OHLC 1 heure
CREATE TABLE IF NOT EXISTS crypto.ohlc_1h (
    symbol String,
    window_start DateTime,
    price_open Float64,
    price_high Float64,
    price_low Float64,
    price_close Float64,
    volume_sum Float64,
    trade_count UInt32,
    price_avg Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(window_start)
ORDER BY (symbol, window_start)
TTL window_start + INTERVAL 180 DAY;

CREATE MATERIALIZED VIEW IF NOT EXISTS crypto.ohlc_1h_mv
TO crypto.ohlc_1h
AS SELECT
    symbol,
    toStartOfHour(timestamp) as window_start,
    argMin(price, timestamp) as price_open,
    max(price) as price_high,
    min(price) as price_low,
    argMax(price, timestamp) as price_close,
    sum(volume_24h) as volume_sum,
    count() as trade_count,
    avg(price) as price_avg
FROM crypto.prices
GROUP BY symbol, window_start;

-- Table pour les statistiques par crypto
CREATE TABLE IF NOT EXISTS crypto.stats_summary (
    symbol String,
    date Date,
    min_price Float64,
    max_price Float64,
    avg_price Float64,
    stddev_price Float64,
    total_volume Float64,
    data_points UInt32,
    price_volatility Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (symbol, date);

-- Vue matérialisée pour les statistiques quotidiennes
CREATE MATERIALIZED VIEW IF NOT EXISTS crypto.stats_summary_mv
TO crypto.stats_summary
AS SELECT
    symbol,
    toDate(timestamp) as date,
    min(price) as min_price,
    max(price) as max_price,
    avg(price) as avg_price,
    stdDevPop(price) as stddev_price,
    sum(volume_24h) as total_volume,
    count() as data_points,
    (stdDevPop(price) / avg(price)) * 100 as price_volatility
FROM crypto.prices
GROUP BY symbol, date;

-- Table pour les alertes et anomalies
CREATE TABLE IF NOT EXISTS crypto.alerts (
    symbol String,
    alert_type String,
    severity String,
    message String,
    current_value Float64,
    threshold_value Float64,
    timestamp DateTime DEFAULT now()
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (symbol, timestamp)
TTL timestamp + INTERVAL 30 DAY;

-- Dictionnaire pour les métadonnées des cryptos (cache)
CREATE DICTIONARY IF NOT EXISTS crypto.crypto_metadata_dict (
    symbol String,
    name String,
    rank UInt16
)
PRIMARY KEY symbol
SOURCE(CLICKHOUSE(
    HOST 'localhost'
    PORT 9000
    USER 'default'
    TABLE 'crypto_metadata'
    DB 'crypto'
))
LAYOUT(HASHED())
LIFETIME(MIN 3600 MAX 7200);

-- Table pour les métadonnées
CREATE TABLE IF NOT EXISTS crypto.crypto_metadata (
    symbol String,
    name String,
    rank UInt16,
    updated_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY symbol;
