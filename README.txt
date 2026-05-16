# National Transit Worker Safety Risk SMS

## Executive Summary
This solution was engineered in direct response to the Federal Transit Administration’s (FTA) General Directive 24-1 and the Public Transportation Agency Safety Plan (PTASP) Final Rule. This open-source data engineering and AI framework transforms disparate National Transit Database (NTD) records into actionable, predictive risk scores. 

By utilizing XGBoost and SHAP explainable AI, this system provides the Department of Transportation and regional transit authorities with a modernized, scalable infrastructure to proactively predict and mitigate transit worker fatalities, injuries, and assaults across the United States.

---

## System Architecture
This pipeline represents a complete transition from legacy, manual spreadsheet risk matrices to a fully automated, cloud-based Safety Management System (SMS).

1. **Data Engineering (ETL):** An automated Python pipeline extracts raw safety, security, and geographic data from the federal NTD portal, cleanses it of duplicates and missing fields, and loads it into a relational Azure SQL Database.
2. **Predictive Engine:** An XGBoost Regressor trained on historical incident severity (fatalities and injuries) calculates forward-looking risk probabilities based on temporal, environmental, and operational features.
3. **Public Deployment:** A dynamic Streamlit web application provides transit directors with a Tier-1 interactive dashboard for resource allocation.

---

## Key Industry-Standard Features
* **Explainable AI (SHAP):** Eliminates "Black Box" algorithms. The system dynamically generates waterfall visualizations to explain the exact operational drivers (e.g., Worker Fatigue, Recent Assaults) influencing an agency's risk score.
* **Longitudinal Trend Analysis:** Real-time 12-month trailing time-series data to track mitigation effectiveness and seasonal anomalies.
* **Peer Benchmarking:** Contextualizes local agency risk against the national federal aggregate to assist in targeted DOT grant funding requests.
* **Automated Data Cleansing:** Strict schema validation during the ingestion phase prevents dirty federal data (such as duplicate event logging) from artificially inflating risk scores.

---

## Technical Stack
* **Database:** Microsoft Azure SQL (ODBC Driver 18)
* **Data Processing:** Pandas, NumPy, SQLAlchemy
* **Machine Learning:** XGBoost, Scikit-Learn, SHAP
* **Frontend Visualization:** Streamlit, Plotly Express, Plotly Graph Objects

---

## Federal Compliance & Impact
This repository demonstrates a scalable framework that allows mid-to-large-sized transit agencies to comply with federal data-driven safety mandates without requiring massive internal data engineering departments. It establishes a transparent, adoptable national standard for predictive transit safety.

---

## Local Installation & Execution
To replicate this environment locally for independent review or regional adoption, please follow these steps:

**0. 
Download the latest Major Safety and Security Events file and the Agency Information master file from the Federal Transit Administration NTD Data Portal. Place both .csv files directly into the root directory of this project:
https://data.transportation.gov/Public-Transit/Major-Safety-and-Security-Events/9ivb-8ae9/data_preview
https://www.transit.dot.gov/ntd/data-product/2024-annual-database-agency-information

**1. Clone the Repository**
Bash:
git clone [https://github.com/brvmike/National-Transit-Safety-SMS.git](https://github.com/brvmike/National-Transit-Safety-SMS.git)
cd National-Transit-Safety-SMS

2. Install Dependencies
Ensure you have Python 3.10 or higher installed. Install the required packages by running:

Bash: 
pip install -r requirements.txt

3. Database Configuration
This framework relies on Azure SQL. You will need an active Azure SQL Database to host the data.
Open app.py, ingest_ntd_data.py, and train_risk_model.py.

Locate the Cloud Connection sections in each file.
Update the server, database, username, and password variables with your active credentials.

4. Execute the Data Pipeline & ML Model
Before launching the dashboard, you must ingest the raw federal data and generate the predictive risk scores:

Bash:
python ingest_ntd_data.py
python train_risk_model.py


5. Launch the Dashboard
Once the database is populated, start the interactive Streamlit application:

Bash:
streamlit run app.py
