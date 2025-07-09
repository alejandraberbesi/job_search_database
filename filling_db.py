# df_to_sql.py

import pandas as pd
import sqlite3

# --- CONFIGURATION ---
DB_NAME = "jobs.db"
DF_FILE = "jobs_scraped.pkl"

# --- LOAD DATAFRAME ---
try:
    df = pd.read_pickle(DF_FILE)
except Exception as e:
    print("Could not load DataFrame:", e)
    exit(1)

if df.empty:
    print("DataFrame is empty. Nothing to insert.")
    exit(0)

# --- CONNECT TO DATABASE ---
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        row_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        url TEXT,
        days_since_publication INTEGER,
        years_experience INTEGER,
        python INTEGER,
        sql INTEGER,
        machine_learning INTEGER,
        data_analytics INTEGER,
        location TEXT,
        publication_date TEXT,
        date_added TEXT,
        UNIQUE(title, company, date_added)
    )
""")
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_title_company_date ON jobs(title, company, date_added)"
)
conn.commit()

# --- CHECK FOR DUPLICATES ---
existing_rows = pd.read_sql_query("SELECT title, company, date_added FROM jobs", conn)

if not existing_rows.empty:
    df = df.merge(
        existing_rows, on=["title", "company", "date_added"], how="left", indicator=True
    )
    df = df[df["_merge"] == "left_only"].drop(columns=["_merge"])

# --- INSERT NEW ROWS ---
if not df.empty:
    df.to_sql("jobs", conn, if_exists="append", index=False)
    print(f"Inserted {len(df)} new rows into '{DB_NAME}'")
else:
    print("No new jobs to add. All rows were already present.")

conn.close()
