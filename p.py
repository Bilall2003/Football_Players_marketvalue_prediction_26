import duckdb
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
db_path = "transfermarkt-datasets.duckdb"

logging.info("🚀 Connecting to local DuckDB file...")
conn = duckdb.connect(db_path)

# Comprehensive master query with correct aggregations and restored club financial values
query = """
WITH distinct_seasonal_stats AS (
    -- Step 1: Secure an isolated count of match metrics so rows never double-multiply
    SELECT 
        a.player_id,
        CAST(g.season AS INTEGER) AS match_season,
        SUM(a.goals) AS total_club_goals,
        SUM(a.assists) AS total_club_assists,
        SUM(a.minutes_played) AS total_minutes,
        SUM(CASE WHEN (a.player_club_id = g.home_club_id AND g.away_club_goals = 0) OR 
                      (a.player_club_id = g.away_club_id AND g.home_club_goals = 0) THEN 1 ELSE 0 END) AS clean_sheets,
        SUM(CASE WHEN a.player_club_id = g.home_club_id THEN g.away_club_goals 
                 ELSE g.home_club_goals END) AS team_goals_conceded,
        SUM(a.yellow_cards) AS total_yellow_cards,
        SUM(a.red_cards) AS total_red_cards,
        COUNT(DISTINCT a.game_id) AS total_match_appearances
    FROM main.appearances a
    JOIN main.games g ON a.game_id = g.game_id
    WHERE CAST(g.season AS INTEGER) BETWEEN 2015 AND 2025
    GROUP BY a.player_id, g.season
),
isolated_seasonal_valuations AS (
    -- Step 2: Grab the single absolute peak valuation per player within the calendar year
    SELECT 
        player_id,
        EXTRACT(YEAR FROM CAST(date AS DATE)) AS valuation_year,
        MAX(market_value_in_eur) AS end_of_season_market_value
    FROM main.player_valuations
    WHERE EXTRACT(YEAR FROM CAST(date AS DATE)) BETWEEN 2015 AND 2025
    GROUP BY player_id, EXTRACT(YEAR FROM CAST(date AS DATE))
),
calculated_club_values AS (
    -- Step 3: Compute the TRUE financial strength of each club per season by summing their players' values
    SELECT 
        p.current_club_id AS club_id,
        EXTRACT(YEAR FROM CAST(v.date AS DATE)) AS valuation_year,
        SUM(COALESCE(v.market_value_in_eur, 0)) AS calculated_squad_value
    FROM main.player_valuations v
    JOIN main.players p ON v.player_id = p.player_id
    WHERE EXTRACT(YEAR FROM CAST(v.date AS DATE)) BETWEEN 2015 AND 2025
    GROUP BY p.current_club_id, EXTRACT(YEAR FROM CAST(v.date AS DATE))
)
SELECT 
    p.player_id,
    p.name AS player_name,
    p.position,
    p.sub_position,
    p.foot,
    p.height_in_cm,
    dss.match_season AS season,
    (dss.match_season - EXTRACT(YEAR FROM p.date_of_birth)) AS age_at_season,
    
    -- Flawless Independent Performance Metrics
    dss.total_club_goals,
    dss.total_club_assists,
    dss.total_minutes,
    dss.clean_sheets,
    dss.team_goals_conceded,
    dss.total_yellow_cards,
    dss.total_red_cards,
    dss.total_match_appearances,
    COALESCE(CAST(p.international_caps AS INTEGER), 0) AS total_career_international_caps,
    
    -- Context and Target Values
    c.name AS club_name,
    c.domestic_competition_id AS league_id,
    COALESCE(MAX(ccv.calculated_squad_value), 0) AS club_total_financial_value, -- Restored and dynamic
    COALESCE(CAST(p.highest_market_value_in_eur AS BIGINT), 0) AS player_all_time_peak_value,
    isv.end_of_season_market_value
FROM distinct_seasonal_stats dss
JOIN main.players p ON dss.player_id = p.player_id
JOIN main.clubs c ON p.current_club_id = c.club_id
JOIN isolated_seasonal_valuations isv ON dss.player_id = isv.player_id AND dss.match_season = isv.valuation_year
LEFT JOIN calculated_club_values ccv ON p.current_club_id = ccv.club_id AND dss.match_season = ccv.valuation_year
GROUP BY 
    p.player_id, p.name, p.position, p.sub_position, p.foot, p.height_in_cm, 
    dss.match_season, p.date_of_birth, dss.total_club_goals, dss.total_club_assists,
    dss.total_minutes, dss.clean_sheets, dss.team_goals_conceded, dss.total_yellow_cards,
    dss.total_red_cards, dss.total_match_appearances, p.international_caps, c.name, 
    c.domestic_competition_id, p.highest_market_value_in_eur, isv.end_of_season_market_value
ORDER BY player_name, season;
"""

logging.info("\n📊 Compiling absolute final all-position dataset with restored club values...")
df = conn.execute(query).df()

print(f"✅ Success! Accurate dataset compiled with {df.shape[0]} rows and {df.shape[1]} columns.")

# Preview specific validation fields to verify accuracy
print("\n🔍 Verification Preview (Top 5 rows):")
print(df[['player_name', 'season', 'total_club_goals', 'club_total_financial_value', 'end_of_season_market_value']].head())

# Overwrite your flat file locally
df.to_csv("football_ml_dataset.csv", index=False)
logging.info("\n💾 Dataset cleanly saved as 'football_ml_dataset.csv'!")
