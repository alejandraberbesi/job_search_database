# Remote Job Aggregator for LATAM Tech Roles

A modular data pipeline to collect, enrich, and store **remote job listings** in Data, AI, and Machine Learning — with a focus on **LATAM** and compatible remote time zones.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
---

## 🔭 Key Goals

- **Multi-source ingestion**: Integrate APIs like Remotive, RemoteOK, etc.
- **Fast NLP enrichment**: Extract key skills and tags from job descriptions
- **SQLite storage**: Store all jobs in a persistent, queryable database
- **Automation**: Orchestrate with Apache Airflow for regular scraping
- **Query-ready data**: Enable search via SQL tools

---

## 🗂️ Core Components

| File                | Purpose                                              |
|---------------------|------------------------------------------------------|
| `search_automation.py` | Fetches, filters, and enriches jobs from APIs     |
| `filling_db.py`        | Deduplicates and inserts jobs into SQLite  |

---

## 🚧 Active Development

This project is under continuous improvement — models, sources, and structure are evolving. 



