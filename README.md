<div align="center">
  <!-- Badges -->
  <img src="https://shields.io" alt="Python Version" />
  <img src="https://shields.io" alt="Scikit-Learn" />
  <img src="https://shields.io" alt="License" />

  <br /><br />

  <!-- Main Title -->
  <h1>⚽ Football Market Value Predictor</h1>
  <p><strong>An Intelligent Machine Learning Inference Pipeline using Column Transformers & Advanced Feature Alignment</strong></p>
</div>

---


---

## 📋 Project Overview

This project delivers a robust **Predictive Inference Engine** built to evaluate and estimate football player market values based on real-world on-pitch performance metrics and club financial parameters. 

The pipeline uses a pre-trained **Scikit-Learn Pipeline** featuring an integrated `ColumnTransformer` to handle both categorical alignments (e.g., player position nuances) and continuous scaling metrics. It features a custom **fail-safe verification pipeline** designed to ingest raw unseen data from global sources (like FBref and Transfermarkt), dynamically match feature maps, handle missing attributes, and cleanly output precise valuations.

---

## 🚀 Key Architectural Features

* **Dynamic Feature Verification:** Automatically extracts target schemas directly from the `ColumnTransformer` binary to map features dynamically.
* **Case & String Insensitivity:** Normalizes real-world input columns safely into unified `lowercase` and `snake_case` formats.
* **Fault-Tolerant Alignment:** Uses a smart alias mapping schema to resolve structural variations like translating `total_goal_scored` into the model-expected `total_club_goals`.
* **Zero-Crash Fail-safe:** Dynamically synthesizes missing dimensional inputs on the fly to protect live inference pipelines from shape mismatches.

---

## 📊 Model Feature Schema

The underlying predictive model scales performance and economic data across **16 core features**:

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Model Feature Expected Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2"><b>Biometrics / Profile</b></td>
      <td><code>position</code></td>
      <td>Primary playing sector (e.g., DF, MF, FW)</td>
    </tr>
    <tr>
      <td><code>sub_position</code></td>
      <td>Specific tactical role (e.g., Centre-Back, Left Winger)</td>
    </tr>
    <tr>
      <td rowspan="3"><b>Temporal Variables</b></td>
      <td><code>height_in_cm</code></td>
      <td>Physical height scaling</td>
    </tr>
    <tr>
      <td><code>season</code></td>
      <td>Target evaluation calendar year (e.g., 2025/2026)</td>
    </tr>
    <tr>
      <td><code>age_at_season</code></td>
      <td>Player age during the target evaluation cycle</td>
    </tr>
    <tr>
      <td rowspan="4"><b>Attacking & Presence</b></td>
      <td><code>total_club_goals</code></td>
      <td>Total goals across all domestic/continental club fixtures</td>
    </tr>
    <tr>
      <td><code>total_club_assists</code></td>
      <td>Total goal-scoring assists distributed</td>
    </tr>
    <tr>
      <td><code>total_minutes</code></td>
      <td>Cumulative on-pitch playing time</td>
    </tr>
    <tr>
      <td><code>total_match_appearances</code></td>
      <td>Total appearances logged</td>
    </tr>
    <tr>
      <td rowspan="3"><b>Defensive / Discipline</b></td>
      <td><code>clean_sheets</code></td>
      <td>Shutouts logged (primarily scaled for GK/DF metrics)</td>
    </tr>
    <tr>
      <td><code>team_goals_conceded</code></td>
      <td>Defensive stability metric during appearance spans</td>
    </tr>
    <tr>
      <td><code>total_yellow_cards</code> / <code>total_red_cards</code></td>
      <td>Disciplinary records across the evaluation cycle</td>
    </tr>
    <tr>
      <td rowspan="3"><b>Economic & Int'l Realized Value</b></td>
      <td><code>total_career_international_caps</code></td>
      <td>Total career matches played for senior national team</td>
    </tr>
    <tr>
      <td><code>club_total_financial_value</code></td>
      <td>Overall squad financial valuation index</td>
    </tr>
    <tr>
      <td><code>player_all_time_peak_value</code></td>
      <td>The highest historical market evaluation reached by the player</td>
    </tr>
  </tbody>
</table>

---

## 💻 Core Pipeline Code

The unified validation and inference block safely transforms disparate external data frames prior to model prediction:

```python
import joblib
import pandas as pd

def model_verify(df):
    # Load binary artifact
    model_saved = joblib.load("football_market_value_model.joblib")
    
    # 1. Standardize column cases and remove spaces
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # 2. Map known global data variations to expected schemas
    column_aliases = {
        'total_goal_scored': 'total_club_goals',
        'goals_scored': 'total_club_goals',
        'player_age': 'age_at_season',
        'height': 'height_in_cm',
        'main_position': 'sub_position'
    }
    df = df.rename(columns=column_aliases)
    
    # 3. Pull required features directly from ColumnTransformer
    expected_features = [col.lower() for col in model_saved.steps[0][1].feature_names_in_]
    
    # 4. Fill missing features gracefully to prevent structural crashes
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
            
    # 5. Isolate inference frame and generate prediction
    final_input = df[expected_features].iloc[[0]]
    prediction = model_saved.predict(final_input)
    
    print(f"⚽ Predicted Player Market Value: {prediction[0]}")
    return prediction[0]
```

---

## 🛠️ Getting Started

### Prerequisites
Make sure your working environment has the required scientific computing libraries installed:
```bash
pip install numpy pandas scikit-learn joblib
```

### Quick Execution
1. Clone this repository to your local runtime ecosystem.
2. Ensure your trained file `football_market_value_model.joblib` is saved in the root workspace folder.
3. Call `model_verify(your_dataframe)` with any real-world player payload.

---
<div align="center">
  <p>Built for Data Verification & Predictive Stability</p>
</div>
