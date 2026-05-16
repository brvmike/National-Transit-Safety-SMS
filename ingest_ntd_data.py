import pandas as pd
import pgeocode
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# --- 1. CLOUD CONNECTION SETUP ---
server = 'transit-safety-server-xyz.database.windows.net'
database = 'TransitSafetyDB'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Using SQLAlchemy's URL builder prevents string parsing errors
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

# Create the engine using the safe URL object
engine = create_engine(connection_url)

# --- 2. DATA EXTRACTION & GEOCODING ---
print("Reading raw NTD CSVs...")
df_raw = pd.read_csv("C:\\Users\\Brave\\Downloads\\Major_Safety_and_Security_Events_20260514.csv", low_memory=False)

# Update this path to exactly where your Agency Info file is saved
df_agency_info = pd.read_csv("C:\\Users\\Brave\\Downloads\\2024 Agency Information_250922.csv", encoding='latin1') 

print("Merging Geospatial Data...")
# Extract only the location data we care about
df_locations = df_agency_info[['NTD ID', 'City', 'State', 'Zip Code']].drop_duplicates(subset=['NTD ID'])

# --- THE FIX: Force both keys to be strings to prevent int64/object mismatch ---
df_raw['NTD ID'] = df_raw['NTD ID'].astype(str)
df_locations['NTD ID'] = df_locations['NTD ID'].astype(str)
# Merge the location data into your main safety pipeline
df_raw = pd.merge(df_raw, df_locations, on='NTD ID', how='left')

print("Geocoding Zip Codes (This may take a moment)...")
nomi = pgeocode.Nominatim('us') 
df_raw['Clean_Zip'] = df_raw['Zip Code'].astype(str).str.zfill(5).str[:5] 
geo_data = nomi.query_postal_code(df_raw['Clean_Zip'].tolist())

df_raw['Latitude'] = geo_data.latitude
df_raw['Longitude'] = geo_data.longitude

# --- 3. DATA ENGINEERING & TRANSFORMATION ---
print("Transforming and cleaning data for national safety analysis...")

# Normalize Agency Data - NOW INCLUDES GEOSPATIAL COLUMNS
df_agency = df_raw[['NTD ID', 'Agency', 'City', 'State', 'Latitude', 'Longitude']].drop_duplicates(subset=['NTD ID'], keep='first').dropna(subset=['NTD ID'])
df_agency.columns = ['NTDID', 'AgencyName', 'City', 'State', 'Latitude', 'Longitude']

# Normalize Mode Data - Force uniqueness strictly on Mode
df_mode = df_raw[['Mode', 'Mode Name']].drop_duplicates(subset=['Mode'], keep='first').dropna()
df_mode.columns = ['ModeCode', 'ModeName']

# Process Fact Table 
df_fact = pd.DataFrame()
df_fact['NTDID'] = df_raw['NTD ID']
df_fact['ModeCode'] = df_raw['Mode']
df_fact['IncidentDate'] = pd.to_datetime(df_raw['Event Date'], errors='coerce')
df_fact['EventType'] = df_raw['Event Type']
df_fact['LocationDescription'] = df_raw['Location Type'].fillna('Unknown')

# AGGREGATION LOGIC
worker_fatality_cols = [
    'Transit Vehicle Operator Fatalities', 
    'Non-Operator Transit Employee Fatalities', 
    'Other Worker Fatalities'
]
df_fact['WorkerFatalities'] = df_raw[worker_fatality_cols].fillna(0).sum(axis=1)

worker_injury_cols = [
    'Transit Vehicle Operator Injuries', 
    'Non-Operator Transit Employee Injuries', 
    'Other Worker Injuries',
    'Transit Vehicle Operator Serious Injuries',
    'Non-Operator Transit Employee Serious Injuries',
    'Other Worker Serious Injuries'
]
df_fact['WorkerInjuries'] = df_raw[worker_injury_cols].fillna(0).sum(axis=1)

# Public Impacts (Total minus Workers)
df_fact['PublicFatalities'] = df_raw['Total Fatalities'].fillna(0) - df_fact['WorkerFatalities']
df_fact['PublicInjuries'] = df_raw['Total Injuries'].fillna(0) - df_fact['WorkerInjuries']

# Clean up any bad dates or missing IDs
df_fact = df_fact.dropna(subset=['IncidentDate', 'NTDID', 'ModeCode'])

# --- 4. DATA LOADING (The "L" in ETL) ---
print("Uploading Dimensions to Azure...")

# --- THE FIX: Generate the ID columns dynamically in Python ---
df_agency.insert(0, 'AgencyID', range(1, 1 + len(df_agency)))
df_mode.insert(0, 'ModeID', range(1, 1 + len(df_mode)))
# --------------------------------------------------------------

# Use 'replace' instead of 'append' so Pandas builds the tables with the new IDs
df_agency.to_sql('Dim_TransitAgency', con=engine, if_exists='replace', index=False)
df_mode.to_sql('Dim_TransitMode', con=engine, if_exists='replace', index=False)

print("Mapping IDs and Uploading Fact Table...")
# Pull back the auto-generated IDs to maintain relational integrity
db_agencies = pd.read_sql("SELECT AgencyID, NTDID FROM Dim_TransitAgency", engine)
db_modes = pd.read_sql("SELECT ModeID, ModeCode FROM Dim_TransitMode", engine)

# Force all join keys to be strings to prevent int64/object mismatch 
df_fact['NTDID'] = df_fact['NTDID'].astype(str)
db_agencies['NTDID'] = db_agencies['NTDID'].astype(str)

df_fact['ModeCode'] = df_fact['ModeCode'].astype(str)
db_modes['ModeCode'] = db_modes['ModeCode'].astype(str)

df_fact = df_fact.merge(db_agencies, on='NTDID', how='inner')
df_fact = df_fact.merge(db_modes, on='ModeCode', how='inner')

# Final selection for Azure SQL table
df_fact_final = df_fact[['AgencyID', 'ModeID', 'IncidentDate', 'EventType', 
                         'WorkerFatalities', 'WorkerInjuries', 'PublicFatalities', 
                         'PublicInjuries', 'LocationDescription']]

# Use 'replace' here as well for a clean slate
df_fact_final.to_sql('Fact_SafetyIncidents', con=engine, if_exists='replace', index=False)

print("SUCCESS: Data pipeline run complete. Your Azure SQL DB is now populated with Geospatial Data.")