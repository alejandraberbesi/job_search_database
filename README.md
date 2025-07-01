# 🌎 Remote Job Aggregator for LATAM Data Roles

This project builds a structured, queryable database of **remote job postings** in **data, AI, and machine learning**, with a focus on **LATAM-friendly** geographies and time zones.

---

## 🎯 Purpose

The goal is to create a modular, automated pipeline that continuously ingests job postings from multiple APIs, filters them for relevance, enriches the content (e.g., summaries, tags), and stores them in a persistent database.

This dataset can be used for:
- Market analysis and job trends
- Dashboards and career intelligence tools
- Alert systems and recommender models

---

## 🧱 Architecture Overview

- **Ingestion:** Fetch jobs from APIs (currently Remotive; more coming)
- **Filtering:** Based on job titles and LATAM-compatible locations
- **Enrichment:**
  - HTML parsing
  - Text summarization (NLP model under revision)
- **Storage:**
  - Intermediate: Pickle + human-readable `.txt`
  - Final: Deduplicated SQLite database (`jobs.db`)
- **Automation-ready:** Designed for future cron or cloud scheduling

---

## 📦 Components

| File              | Description                                         |
|-------------------|-----------------------------------------------------|
| `search_automation.py` | Ingests + filters + summarizes jobs from Remotive |
| `filling_db.py`        | Inserts new, deduplicated records into SQLite DB  |
| `jobs_scraped.pkl`     | Serialized DataFrame of current scraped jobs      |
| `latest_jobs.txt`      | Text summary output for quick inspection          |
| `jobs.db`              | Central job postings database (SQLite)            |

---

## 🔄 Roadmap

- ✅ Core Remotive API pipeline
- 🔁 Replace and improve summarization (LLM or custom heuristic)
- ➕ Add new APIs (e.g. WeWorkRemotely, RemoteOK, Jobspresso)
- 🧹 Add job deduplication across sources
- 📤 Export options (CSV, JSON, GSheets)
- 🕒 Schedule with cron or GitHub Actions
- 📊 Create data dashboard (e.g., Streamlit, Superset)

---

## 📌 Example Use Cases

- **Data engineers** building automated job tracking systems
- **Researchers** analyzing market demand for AI/data roles in emerging markets
- **Job boards or newsletters** that need structured, fresh job feeds

---

## ⚠️ Status

> 🚧 In active development. Expect frequent changes as new APIs and features are integrated.

