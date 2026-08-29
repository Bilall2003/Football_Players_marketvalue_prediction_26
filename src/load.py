import duckdb
import pandas as pd

# Since the file is now directly in your workspace folder!
db_path = "transfermarkt-datasets.duckdb"

print("🚀 Connecting to local DuckDB file...")
conn = duckdb.connect(db_path)

print("\n--- Available Tables ---")
print(conn.execute("SHOW TABLES;").df())

# Master SQL Query to select and merge columns across tables
query = """
SELECT 
    p.player_id,
    p.name,
    p.position,
    p.sub_position,
    p.foot,
    p.height_in_cm,
    a.season,
    (a.season - EXTRACT(YEAR FROM p.date_of_birth)) AS age_at_season,
    SUM(a.goals) AS total_goals,
    SUM(a.assists) AS total_assists,
    SUM(a.minutes_played) AS total_minutes,
    SUM(a.yellow_cards) AS total_yellow_cards,
    SUM(a.red_cards) AS total_red_cards,
    c.name AS club_name,
    c.domestic_competition_id AS league_id,
    v.market_value_in_eur AS end_of_season_market_value
FROM appearances a
JOIN players p ON a.player_id = p.player_id
JOIN clubs c ON p.current_club_id = c.club_id
JOIN player_valuations v ON a.player_id = v.player_id 
    AND v.date BETWEEN CAST(a.season || '-05-15' AS DATE) AND CAST(a.season || '-07-15' AS DATE)
WHERE a.season BETWEEN 2020 AND 2025
GROUP BY 
    p.player_id, p.name, p.position, p.sub_position, p.foot, p.height_in_cm, 
    a.season, p.date_of_birth, c.name, c.domestic_competition_id, v.market_value_in_eur
ORDER BY p.name, a.season;
"""

print("\n📊 Extracting and merging dataset (2020-2025)...")
df = conn.execute(query).df()

print(f"✅ Success! Generated a matrix with {df.shape[0]} rows and {df.shape[1]} columns.")
print(df.head())

# Save dataset next to your script
df.to_csv("football_ml_dataset.csv", index=False)
print("\n💾 Dataset saved as 'football_ml_dataset.csv'!")
