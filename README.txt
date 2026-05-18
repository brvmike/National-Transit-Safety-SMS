National Transit Worker Safety Risk SMS Dashboard

Executive Summary
This solution was engineered in direct response to the Federal Transit Administration’s (FTA) General Directive 24-1 and the Public Transportation Agency Safety Plan (PTASP) Final Rule. This open-source data engineering and AI framework transforms live web-streamed National Transit Database (NTD) records into actionable, predictive risk scores. 

By utilizing XGBoost and SHAP explainable AI, this system provides the Department of Transportation and regional transit authorities with a modernized, cloud-scalable infrastructure to proactively predict and mitigate transit worker fatalities, injuries, and assaults across the United States.

The System Architecture
This pipeline represents a complete transition from legacy, manual spreadsheet risk matrices to a fully automated, cloud-backed Safety Management System (SMS) utilizing a clean separation of concerns:

1. Automated Data Ingestion (ETL): An automated Python pipeline (`ingest_ntd_data.py`) establishes a direct network socket to the FTA's public REST API gateway to pull the entire historical series of over 111,000+ incident logs. It dynamically joins this transactional stream against a localized static reference dataset to geocode municipal targets via `pgeocode` before dropping a clean relational schema into an Azure SQL Database.
2. Predictive Engine: An XGBoost Regressor trained on multi-year incident severity profiles calculates forward-looking risk probabilities based on temporal, environmental, and operational features.
3. Public Deployment: A lightweight, performant Streamlit web application connects securely to the cloud database, providing transit directors with a Tier-1 interactive dashboard for executive resource allocation.

Key Industry-Standard Features
* Live REST API Ingestion: Eliminates manual data maintenance. The ingestion script handles enterprise-scale JSON payloads directly from the federal data gateway, implementing automatic connection timeouts and request constraints.
* Explainable AI (SHAP): Eliminates "Black Box" algorithms. The system dynamically generates waterfall visualizations to explain the exact operational drivers (e.g., Worker Fatigue, Recent Assaults) influencing an agency's risk score.
* Longitudinal Trend Analysis: Real-time 12-month trailing time-series data to track mitigation effectiveness and seasonal anomalies.
* Peer Benchmarking: Contextualizes local agency risk against the national federal aggregate to assist in targeted DOT grant funding requests.
* Defensive Data Auditing: Type casting via `pd.to_numeric` with string coercion shields the downstream machine learning engine from corrupt data or schema skewing on the public web stream.

Technical Stack
* Language: Python 3.9+
* Data Ingestion: Requests (Socrata Open Data REST API)
* Predictive Modeling: XGBoost Regressor, Scikit-Learn
* Explainable AI: SHAP (SHapley Additive exPlanations)
* Data Engineering (ETL): Pandas, NumPy, Pgeocode, SQLAlchemy
* Database Management: Microsoft Azure SQL (via PyODBC)
* Front-End / UI: Streamlit, Plotly (Geospatial & Time-Series Visualizations)
* Alerting Integrations: Twilio API, Azure Logic Apps

Repository Structure
```text
├── app.py                       # Main Streamlit Executive Dashboard
├── ingest_ntd_data.py           # Automated Live API Ingestion & ETL Pipeline
├── train_risk_model.py          # XGBoost Training & SHAP Core Engine
├── WHITEPAPER.pdf               # Strategic Technical White Paper for Adjudication
└── data/                        # Isolated Reference Directory
    └── 2024_Agency_Information.csv   # Local Static Master Reference Metadata


Federal Compliance & Impact
This repository demonstrates a scalable framework that allows mid-to-large-sized transit agencies to comply with federal data-driven safety mandates without requiring massive internal data engineering departments. It establishes a transparent, adoptable national standard for predictive transit safety.


Local Installation & Execution
To replicate this environment locally for independent review or regional adoption, please follow these steps:

0. Acquire Raw Federal Data
Download the latest *Agency Information* master file from the Federal Transit Administration NTD Data Portal. Place the `.csv` file directly into the root directory of this project:
* [2024 Annual Database Agency Information](https://www.transit.dot.gov/ntd/data-product/2024-annual-database-agency-information)

1. Clone this Repository
git clone [https://github.com/brvmike/National-Transit-Safety-SMS.git](https://github.com/brvmike/National-Transit-Safety-SMS.git)
cd National-Transit-Safety-SMS

2. Install Dependencies
Ensure you have Python 3.10 or higher installed. Install the required packages by running:
pip install -r requirements.txt

3. Database Configuration
This framework relies on Azure SQL. You will need an active Azure SQL Database to host the data.
Open app.py, ingest_ntd_data.py, and train_risk_model.py.

Locate the Cloud Connection sections in each file.
Update the server, database, username, and password variables with your active credentials.

4. Execute the Data Pipeline & ML Model
Before launching the dashboard, you must ingest the raw federal data and generate the predictive risk scores:
python ingest_ntd_data.py
python train_risk_model.py

5. Launch the Dashboard
Once the database is populated, start the interactive Streamlit application:
streamlit run app.py
