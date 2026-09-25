import joblib
from flask import Flask,request,jsonify
import pandas as pd

app=Flask(__name__)

model=joblib.load("football_market_value_model2.joblib")

@app.route("/")
def home():
    return "Prediction is runinng!!!!!!!!!!!!"

#step4: post api
@app.route("/predict", methods=["POST"])

def predict():
    
    try:
        
        cols_to_predict=[
                'position',
                'sub_position',
                'height_in_cm',
                'season',
                'age_at_season',
                'total_club_goals',
                'total_club_assists',
                'total_minutes',
                'clean_sheets',
                'team_goals_conceded',
                'total_yellow_cards',
                'total_red_cards',
                'total_match_appearances',
                'total_career_international_caps',
                'club_total_financial_value',  # Leverkusen squad value
                'player_all_time_peak_value',     # Real baseline value
                'goal_contribution'
            
        ]
        data=request.get_json()
        
        if not data:
            
            return jsonify({
                "error":"request body is empty..."
            }),400
        
        if any(col not in data for col in cols_to_predict):
                return jsonify({
                    "error": "Data Missing inside request body payload."
                }), 400
    
        features = pd.DataFrame([data])
    
            # Prediction
        prediction = model.predict(features)[0]
    
        return jsonify({
                "status": "Success",
                "prediction": str(prediction)
            }),200
        
    
    except Exception as e:
        return jsonify({
            "status":"Failed",
            "error":str(e)
        }),500
        

if __name__=="__main__":
    app.run(debug=False)
    
