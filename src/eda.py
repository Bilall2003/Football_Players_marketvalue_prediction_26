import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(
    
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    
)

def clean(df_path):
    
    try:
    
        df=pd.read_csv(df_path)
        
        print(df.head(10))
        print(df.columns)
        print(df.isnull().sum().sum())

        df_new=df.copy()

        print(df_new.columns)
        print(df_new.head())
        print(df_new.isnull().sum())

        # 1. Fill missing sub_positions with a safe fallback string
        df_new["sub_position"] = df_new["sub_position"].fillna("Unknown")

        # 2. Fill missing foot preference using the single top mode value (usually 'right')
        most_common_foot = df_new["foot"].mode()[0]
        df_new["foot"] = df_new["foot"].fillna(most_common_foot)

        # 3. Fill missing height with the median height value (fixed your spelling typo)
        median_height = df_new["height_in_cm"].median()
        df_new["height_in_cm"] = df_new["height_in_cm"].fillna(median_height)

        # 4. Fill the 4 missing ages using the median age of the players
        median_age = df_new["age_at_season"].median()
        df_new["age_at_season"] = df_new["age_at_season"].fillna(median_age)

        print(df_new.isnull().sum().sum())
        print(df_new.duplicated().sum())
    
    except Exception as e:
        logging.error(e)
        
    return df_new

def insights(df):
    
    try:
        
        # Most goals by player in a single season
        df_sorted = df.sort_values(by=['season', 'total_club_goals'], ascending=[True, False])
        top_scorers = df_sorted.drop_duplicates(subset=['season'])
        print(top_scorers[['season', 'player_name', 'total_club_goals']])
        
        sns.barplot(x="season",y="total_club_goals",hue="player_name",data=top_scorers)
        plt.show()
        
        # highest market value per season by player 
        gr2=df.sort_values(by=["season","end_of_season_market_value"],ascending=[True,False])
        market_value=gr2.drop_duplicates(subset=['season'])
        print(market_value[['season','player_name','end_of_season_market_value']])
        
        sns.barplot(x="season", y="end_of_season_market_value", hue="player_name", data=market_value)
        plt.show()
        
        # Most assist by player in a single season
        gr3 = df.sort_values(by=['season', 'total_club_assists'], ascending=[True, False])
        top_assist = gr3.drop_duplicates(subset=['season'])
        print(top_assist[['season', 'player_name', 'total_club_assists']])
        
        sns.barplot(x="season",y="total_club_assists",hue="player_name",data=top_assist)
        plt.show()
        
    except Exception as e:
        logging.error(e)
        
if __name__=="__main__":
    
    obj=clean(df_path=r"D:\Bilal folder\AIML\ML practice\playermarketvalue\football_ml_dataset.csv")
    insights(obj)
    
    
    
    