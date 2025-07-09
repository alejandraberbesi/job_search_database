import requests
import pandas as pd
from datetime import datetime
import re
from bs4 import BeautifulSoup


# locations allowed
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

SCRAPE_DATE = datetime.now().date()

SKILLS = ["python", "sql", "machine learning", "data analytics"]

EXPERIENCE_PATTERN = re.compile(r"(\d+)\+?\s+(?:years?|yrs?)\s+", re.IGNORECASE)

INCLUDE_KEYWORDS = [
    "data analytics",
    "data analysis",
    "data scientist",
    "data science",
    "machine learning engineer",
]
EXCLUDE_KEYWORDS = [
    "head",
    "manager",
    "lead",
    "director",
    "intern",
    "trainee",
]

INCLUDE_PATTERN = re.compile(
    r"\b(?:%s)\b" % "|".join(map(re.escape, INCLUDE_KEYWORDS)), re.IGNORECASE
)
EXCLUDE_PATTERN = re.compile(
    r"\b(?:%s)\b" % "|".join(map(re.escape, EXCLUDE_KEYWORDS)), re.IGNORECASE
)


# description needs preprocessing from html to normal text
def html_to_text(html_content):
    return BeautifulSoup(html_content, "html.parser").get_text(separator="\n").strip()


def fetch_remotive_jobs():
    url = "https://remotive.com/api/remote-jobs"

    try:
        response = requests.get(url)
        response.raise_for_status()
        jobs_data = response.json()["jobs"]
    except Exception as e:
        print("Error fetching jobs:", e)
        exit(1)

    df_jobs = pd.DataFrame(jobs_data)

    # --- FILTER ---
    df_jobs = df_jobs[
        df_jobs["title"].str.contains(INCLUDE_PATTERN, na=False)
        & ~df_jobs["title"].str.contains(EXCLUDE_PATTERN, na=False)
    ]

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
        description_lower = description.lower()

        # Skill presence flags
        skill_flags = {
            f"{skill.replace(' ', '_')}": int(skill in description_lower)
            for skill in SKILLS
        }

        # Years of experience (extract first match if any)
        exp_match = EXPERIENCE_PATTERN.search(description_lower)
        years_experience = int(exp_match.group(1)) if exp_match else None

        rows.append(
            {
                "title": row["title"],
                "company": row["company_name"],
                "url": row["url"],
                "days_since_publication": row["days_since_publication"],
                "years_experience": years_experience,
                **skill_flags,
                "location": row.get("candidate_required_location", "").lower(),
                "publication_date": row["publication_date"].strftime("%d-%m-%Y"),
                "date_added": SCRAPE_DATE.strftime("%d-%m-%Y"),
            }
        )
        return rows


def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        jobs_data = response.json()[1:]
    except Exception as e:
        print("Error fetching jobs:", e)
        return []

    df_jobs = pd.DataFrame(jobs_data)

    # --- Apply filters ---
    # df_jobs = df_jobs[
    #         df_jobs["title"].str.contains(INCLUDE_PATTERN, na=False)
    #         & ~df_jobs["title"].str.contains(EXCLUDE_PATTERN, na=False)
    #     ]

    # df_jobs = df_jobs[
    #         df_jobs["candidate_required_location"]
    #         .str.lower()
    #         .str.contains("|".join(LATAM_KEYWORDS), na=False)
    #     ]

    # df_jobs["publication_date"] = pd.to_datetime(
    #         df_jobs["publication_date"], errors="coerce"
    #     )
    # df_jobs = df_jobs.dropna(
    #         subset=["publication_date"]
    #     )  # remove rows with invalid dates

    # df_jobs["days_since_publication"] = (
    #         pd.Timestamp(SCRAPE_DATE) - df_jobs["publication_date"]
    #     ).dt.days
    # df_jobs = df_jobs[df_jobs["days_since_publication"] <= 30]

    #     # --- Process and summarize ---
    rows = []

    for _, row in df_jobs.iterrows():
        description = row.get("description", "")
        description_lower = description.lower()

        #     skill_flags = {
        #             f"{skill.replace(' ', '_')}": int(skill in description_lower)
        #             for skill in SKILLS
        #         }

        #     exp_match = EXPERIENCE_PATTERN.search(description_lower)
        #     years_experience = int(exp_match.group(1)) if exp_match else None

        rows.append(
            {
                "title": row["title"],
                #                 "company": row["company_name"],
                #                 "url": row["url"],
                #                 "days_since_publication": row["days_since_publication"],
                #                 "years_experience": years_experience,
                #                 **skill_flags,
                #                 "location": row.get("candidate_required_location", "").lower(),
                #                 "publication_date": row["publication_date"].strftime("%d-%m-%Y"),
                #                 "date_added": SCRAPE_DATE.strftime("%d-%m-%Y"),
            }
        )
    return df_jobs


# saving for manual inspection
# remotive_jobs = fetch_remotive_jobs()
remoteok_jobs = fetch_remoteok_jobs()

df_final = pd.DataFrame(
    # remotive_jobs
    # +
    remoteok_jobs
)
df_final.to_string("latest_jobs.txt", index=False)

# saving for later passing to database
df_final.to_pickle("jobs_scraped.pkl")
