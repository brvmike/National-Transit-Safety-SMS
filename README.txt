# 🚂 National Transit Worker Safety Risk SMS (AI-Driven)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Azure SQL](https://img.shields.io/badge/Azure-SQL_Database-0089D6)
![XGBoost](https://img.shields.io/badge/Machine_Learning-XGBoost-orange)
![Streamlit](https://img.shields.io/badge/Deployment-Streamlit-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active_Prototype-success)

## 📌 Statement of Proposed Endeavor
Engineered in direct response to the **Federal Transit Administration’s (FTA) General Directive 24-1** and the **Public Transportation Agency Safety Plan (PTASP) Final Rule**, this open-source data engineering and AI framework transforms disparate National Transit Database (NTD) records into actionable, predictive risk scores. 

By utilizing XGBoost and SHAP explainable AI, this system provides the Department of Transportation and regional transit authorities with a modernized, scalable infrastructure to proactively predict and mitigate transit worker fatalities, injuries, and assaults across the United States.

---

## 🏗️ System Architecture
This pipeline represents a complete transition from legacy, manual spreadsheet risk matrices to a fully automated, cloud-based Safety Management System (SMS).

1. **Data Engineering (ETL):** Automated Python pipeline extracts raw safety, security, and geographic data from the federal NTD portal, cleanses it of duplicates and missing fields, and loads it into a relational **Azure SQL Database**.
2. **Predictive Engine:** An **XGBoost Regressor** trained on historical incident severity (fatalities/injuries) calculates forward-looking risk probabilities based on temporal, environmental, and operational features.
3. **Public Deployment:** A dynamic **Streamlit** web application provides transit directors with a Tier-1 interactive dashboard.

---

## 🚀 Key Industry-Standard Features
* **Explainable AI (SHAP):** Eliminates "Black Box" algorithms. The system dynamically generates waterfall visualizations to explain the exact operational drivers (e.g., Worker Fatigue, Recent Assaults) influencing an agency's risk score.
* **Longitudinal Trend Analysis:** Real-time 12-month trailing time-series data to track mitigation effectiveness and seasonal anomalies.
* **Peer Benchmarking:** Contextualizes local agency risk against the national federal aggregate to assist in targeted DOT grant funding requests.
* **Automated Data Cleansing:** Strict schema validation during the ingestion phase prevents dirty federal data (duplicate event logging) from artificially inflating risk scores.

---

## 🛠️ Technical Stack
* **Database:** Microsoft Azure SQL (ODBC Driver 18)
* **Data Processing:** Pandas, NumPy, SQLAlchemy
* **Machine Learning:** XGBoost, Scikit-Learn, SHAP
* **Frontend Visualization:** Streamlit, Plotly Express, Plotly Graph Objects

---

## 📊 Federal Compliance & Impact
This repository demonstrates a scalable framework that allows mid-to-large-sized transit agencies to comply with federal data-driven safety mandates without requiring massive internal data engineering departments. It establishes a transparent, adoptable national standard for predictive transit safety.