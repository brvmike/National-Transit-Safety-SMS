import pandas as pd
import xgboost as xgb
import shap
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# --- 1. CLOUD CONNECTION ---
server = 'transit-safety-server-xyz.database.windows.net'
database = 'TransitSafetyDB'
username = 'YOUR_USERNAME' # Update this
password = 'YOUR_PASSWORD' # Update this

connection_url = URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    database=database,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
        "Encrypt": "yes",
        "Authentication": "SqlPassword"
    },
)
engine = create_engine(connection_url)

# --- 2. EXTRACT HISTORICAL DATA ---
print("Fetching historical safety data from Azure SQL...")
query = """
    SELECT AgencyID, ModeID, IncidentDate, EventType, LocationDescription, 
           WorkerFatalities, WorkerInjuries
    FROM Fact_SafetyIncidents
"""
df = pd.read_sql(query, engine)

# --- 3. FEATURE ENGINEERING ---
print("Engineering predictive features...")
# Create Temporal Features
df['IncidentDate'] = pd.to_datetime(df['IncidentDate'])
df['Month'] = df['IncidentDate'].dt.month

# Define the "Target" (What the AI is trying to predict)
# We weigh fatalities much heavier than injuries to reflect severe risk
df['HistoricalSeverity'] = (df['WorkerFatalities'] * 50) + (df['WorkerInjuries'] * 10)

# Select the features the AI will learn from
features = ['ModeID', 'Month', 'EventType', 'LocationDescription']
X = df[features]
y = df['HistoricalSeverity']

# Convert text columns (EventType, Location) into numbers using One-Hot Encoding
X_encoded = pd.get_dummies(X, columns=['EventType', 'LocationDescription'])

# Split into training and testing sets to validate accuracy
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# --- 4. TRAIN THE XGBOOST MODEL ---
print("Training XGBoost AI Model (Industry Standard)...")
# We use XGBRegressor because we are predicting a continuous risk score
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

# --- 5. GENERATE PREDICTIONS & RISK SCORES ---
print("Calculating National Risk Scores...")
# Predict on the entire dataset to generate future baseline scores
raw_predictions = model.predict(X_encoded)

# Normalize the raw predictions into a clean 0-100 Risk Score
scaler = MinMaxScaler(feature_range=(0, 100))
df['PredictedWorkerRiskScore'] = scaler.fit_transform(raw_predictions.reshape(-1, 1)).round(2)

# Categorize the risk for the Streamlit Dashboard
def categorize_risk(score):
    if score >= 75: return 'Critical'
    elif score >= 40: return 'Warning'
    else: return 'Stable'

df['RiskCategory'] = df['PredictedWorkerRiskScore'].apply(categorize_risk)
df['ModelVersion'] = 'XGBoost-v1.0'
df['PredictionDate'] = pd.Timestamp.today().date()

# --- 6. SHAP: EXPLAINABLE AI (Crucial for Government Adoption) ---
print("Running SHAP analysis to explain AI logic...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_encoded)
# In a full deployment, we save these SHAP values to explain the dashboard. 
# For now, we confirm the explainer ran successfully.
print("SHAP Explainer initialized successfully.")

# --- 7. LOAD PREDICTIONS TO AZURE SQL ---
print("Uploading predictive scores to Azure Fact_PredictiveRiskScores...")
df_predictions = df[['AgencyID', 'ModeID', 'PredictionDate', 
                     'PredictedWorkerRiskScore', 'RiskCategory', 'ModelVersion']]

df_predictions.to_sql('Fact_PredictiveRiskScores', con=engine, if_exists='append', index=False)

print("SUCCESS: AI Predictions generated and uploaded to the cloud.")