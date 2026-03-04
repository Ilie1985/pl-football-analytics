⚽ Premier League Multi-Season Analytics & Match Prediction
📌 Project Overview

This project builds a complete football analytics pipeline using Premier League data across multiple seasons.

It demonstrates:

API data extraction

Data cleaning & transformation

Exploratory Data Analysis (EDA)

Feature engineering using rolling team performance

Multi-class and binary predictive modelling

Model evaluation and interpretation

The project follows a real-world data science workflow from raw data ingestion to predictive modelling.

📂 Data Source

Data was collected using the football-data.org API.

Seasons included:

2023

2024

2025

Current season (ongoing)

Data extracted:

Match results

League standings

Top scorers

🛠 Project Structure
PL-football-analytics/
│
├── data/
│ ├── raw/ # Raw JSON from API
│ └── processed/ # Cleaned CSV datasets
│
├── notebooks/
│ └── 03_eda_visuals.ipynb
│
├── src/
│ ├── api_client.py
│ ├── extract.py
│ └── clean.py
│
├── requirements.txt
└── README.md
🔄 Data Pipeline
1️⃣ Extraction

Connected to football-data.org API

Pulled multi-season JSON data

Saved raw files for reproducibility

2️⃣ Cleaning & Transformation

Normalized JSON structure

Extracted:

Full-time home/away goals

Match result (H / D / A)

Goal difference

Total goals

Created processed CSV files

3️⃣ Feature Engineering

Created rolling pre-match features:

home_avg_scored

home_avg_conceded

away_avg_scored

away_avg_conceded

Derived matchup features:

home_attack_strength

away_attack_strength

All rolling features use shift() to avoid data leakage.

Chronological train-test split was used to simulate real-world forecasting.

📊 Exploratory Data Analysis

Key findings:

Home Advantage

Home wins consistently represent ~41–46% of results.

Strong structural home advantage across seasons.

Draw Trends

Draw percentage increased from 21.6% (2023) to 26.3% (recent seasons).

Goal Trends

Average goals per match declined:

2023: 3.28

2024: 2.93

2025: 2.79

Suggests increasingly tight and competitive matches.

🤖 Predictive Modelling
Multi-Class Model (H / D / A)

Model: Multinomial Logistic Regression
Features: Rolling goal performance metrics
Split: Chronological (80% train, 20% test)

Accuracy: 42.9%
Baseline: 35.1%

Draw outcomes were difficult to predict — consistent with known structural uncertainty in football.

Random Forest model did not improve performance significantly.

Balanced logistic regression improved class fairness but slightly reduced overall accuracy.

Binary Model (Home Win vs Not Home Win)

Simplified prediction problem:

1 = Home Win

0 = Not Home Win

Binary Logistic Regression Accuracy: 62.5%

Baseline: ~57%

This demonstrates meaningful predictive signal in rolling performance metrics.

📈 Feature Importance (Binary Model)

Most influential features:

Positive Impact on Home Win

home_avg_scored

away_avg_conceded

Negative Impact on Home Win

home_avg_conceded

away_avg_scored

Interpretation:
Teams that score more and concede less in recent matches have higher probability of winning at home.

📦 Technologies Used

Python

pandas

requests

matplotlib

scikit-learn

Jupyter Notebook

VS Code

Git & GitHub

🔬 Key Modelling Practices Demonstrated

Rolling window feature engineering

Avoidance of data leakage

Chronological train-test split

Class imbalance handling

Model comparison (Logistic vs Random Forest)

Baseline benchmarking

Coefficient interpretation

🚀 Future Improvements

Potential extensions:

Include betting odds as market expectations

Add rolling points-per-game features

Use Elo ratings

Try gradient boosting models

Hyperparameter tuning

Deploy as a Streamlit dashboard

🏁 Conclusion

This project demonstrates a complete football analytics pipeline:

From raw API ingestion to interpretable predictive modelling.

While match outcome prediction remains inherently uncertain — especially for draw results — rolling performance indicators provide measurable predictive signal, particularly for home win forecasting
