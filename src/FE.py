import pandas as pd
import numpy as np

def feature_engineering(df):
    
    df["goal_contribution"] = (df["total_club_goals"] + df["total_club_assists"]).div(df["total_minutes"]).fillna(0) * 90
    
    
    print(df.columns)
    print(df.head(10))
    
    return df
    

if __name__=="__main__":
    
    try:
        
        df=pd.read_csv("football_ml_dataset.csv")
        obj=feature_engineering(df)
    
    except Exception as e:
        print(e )