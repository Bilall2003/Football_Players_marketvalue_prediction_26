import duckdb
import pandas as pd

# Since the file is now directly in your workspace folder!
db_path = "transfermarkt-datasets.duckdb"

print("🚀 Connecting to local DuckDB file...")
conn = duckdb.connect(db_path)

print("\n--- Available Tables ---")
print(conn.execute("SHOW TABLES;").df())

# Master SQL Query to select and merge columns across tables
# Master SQL Query with fixed explicit data types
query = """
SELECT 
    p.player_id,
    p.name,
    p.position,
    p.sub_position,
    p.foot,
    p.height_in_cm,
    CAST(g.season AS INTEGER) AS season,
    -- Calculate approximate age during that season
    (CAST(g.season AS INTEGER) - EXTRACT(YEAR FROM p.date_of_birth)) AS age_at_season,
    -- Aggregate performance metrics per season
    SUM(a.goals) AS total_goals,
    SUM(a.assists) AS total_assists,
    SUM(a.minutes_played) AS total_minutes,
    SUM(a.yellow_cards) AS total_yellow_cards,
    SUM(a.red_cards) AS total_red_cards,
    -- Contextual data from clubs and competitions
    c.name AS club_name,
    c.domestic_competition_id AS league_id,
    -- Target Variable: The market value at the end of that specific season
    v.market_value_in_eur AS end_of_season_market_value
FROM appearances a
JOIN games g ON a.game_id = g.game_id
JOIN players p ON a.player_id = p.player_id
JOIN clubs c ON p.current_club_id = c.club_id
JOIN player_valuations v ON a.player_id = v.player_id 
    -- Match the valuation update that occurred right at the end of that season (June/July)
    AND v.date BETWEEN CAST(CAST(g.season AS INTEGER) || '-05-15' AS DATE) AND CAST(CAST(g.season AS INTEGER) || '-07-15' AS DATE)
WHERE CAST(g.season AS INTEGER) BETWEEN 2020 AND 2025
GROUP BY 
    p.player_id, p.name, p.position, p.sub_position, p.foot, p.height_in_cm, 
    g.season, p.date_of_birth, c.name, c.domestic_competition_id, v.market_value_in_eur
ORDER BY p.name, g.season;
"""


print("\n📊 Extracting and merging dataset...")
df = conn.execute(query).df()

print(f"✅ Success! Generated a matrix with {df.shape[0]} rows and {df.shape[1]} columns.")
print(df.head())

# Save dataset next to your script
df.to_csv("football_ml_dataset2.csv", index=False)
print("\n💾 Dataset saved as 'football_ml_dataset.csv'!")