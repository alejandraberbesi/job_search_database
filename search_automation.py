import requests
import pandas as pd
from datetime import datetime
from transformers import pipeline
import re
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
KEYWORDS_PATTERN = re.compile(r"\b(?:data|ai|machine learning)\b", re.IGNORECASE)

LATAM_KEYWORDS = [
    "latam",
    "latin america",
    "south america",
    "mexico",
    "colombia",
    "argentina",
    "chile",
    "worldwide",
    "remote",
    "usa timezones",
    "americas",
]
API_URL = "https://remotive.com/api/remote-jobs"
SCRAPE_DATE = datetime.now().date()
SUMMARY_MODEL = "facebook/bart-large-cnn"
MAX_INPUT_TOKENS = 1024

# --- INITIALIZE ---
summarizer = pipeline("summarization", model=SUMMARY_MODEL)
tokenizer = summarizer.tokenizer


def html_to_text(html_content):
    return BeautifulSoup(html_content, "html.parser").get_text(separator="\n").strip()


def safe_summarize(text, max_length=80, min_length=30):
    try:
        # Truncate text to ~1024 tokens worth (~4000 characters conservatively)
        safe_text = text[:4000]
        return summarizer(
            safe_text, max_length=max_length, min_length=min_length, do_sample=False
        )[0]["summary_text"]
    except Exception as e:
        return f"[SUMMARY ERROR] {type(e).__name__}: {str(e)}"


# --- FETCH JOBS ---
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    jobs_data = response.json()["jobs"]
except Exception as e:
    print("Error fetching jobs:", e)
    exit(1)

# --- LOAD TO DATAFRAME ---
df_jobs = pd.DataFrame(jobs_data)

# --- FILTER ---
df_jobs = df_jobs[df_jobs["title"].str.contains(KEYWORDS_PATTERN, na=False)]

df_jobs = df_jobs[
    df_jobs["candidate_required_location"]
    .str.lower()
    .str.contains("|".join(LATAM_KEYWORDS), na=False)
]

df_jobs["publication_date"] = pd.to_datetime(df_jobs["publication_date"])
df_jobs["days_since_publication"] = (
    pd.Timestamp(SCRAPE_DATE) - df_jobs["publication_date"]
).dt.days

df_jobs = df_jobs[df_jobs["days_since_publication"] <= 30]

# --- PROCESS AND SUMMARIZE ---
rows = []
for _, row in df_jobs.iterrows():
    description = html_to_text(row.get("description", ""))
    summary = safe_summarize(description)

    rows.append(
        {
            "title": row["title"],
            "company": row["company_name"],
            "url": row["url"],
            "location": row.get("candidate_required_location", "").lower(),
            "publication_date": row["publication_date"].strftime("%d-%m-%Y"),
            "days_since_publication": row["days_since_publication"],
            "date_added": SCRAPE_DATE.strftime("%d-%m-%Y"),
            "description_summary": summary,
        }
    )

# --- SAVE TO FILE ---
df_final = pd.DataFrame(rows)
print(df_final.head())

df_final.to_string("latest_jobs.txt", index=False)

df_final.to_pickle("jobs_scraped.pkl")
