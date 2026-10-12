# MoveInSync Play Store Review Intelligence & Action System

> **Forward Deployed Engineer (Intern to FTE) Candidate Assignment**  
> *Objective:* Diagnose MoveInSync's Google Play Store ratings, identify root causes, deliver next-day engineering recommendations, and establish a reusable monitoring capability for the recurring question: *"How are our Play Store ratings?"*

---

## 📌 Quick Access Deliverables

| Document / Tool | Description |
| :--- | :--- |
| 📄 **[RECOMMENDATION_REPORT.md](RECOMMENDATION_REPORT.md)** | **The Primary Submission:** Complete Executive & Product Recommendation Report with root causes, version regressions, 30-60-90 day roadmap, and Jira-ready tickets. |
| 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** | Full System Architecture, sequence diagrams, taxonomy taxonomy schema, and data pipeline design. |
| 📊 **`app.py`** | Interactive **Streamlit Executive Dashboard** for ongoing sentiment tracking, version regression auditing, and review slicing. |

---

## 🔍 Key Findings: Why Are Ratings Where They Are?

Across **756 analyzed reviews** from `com.moveinsync.ets` (4.32★ over 114,880 lifetime ratings):

1. **48.2% Tech & Mobile Bugs:**
   - **App Crash & Infinite Splash Screen on Update:** Cache and Room DB schema migration errors force users to uninstall and reinstall (most upvoted bug, 67+ upvotes).
   - **Map Camera State Reset:** Map auto-zooms out every 3 seconds during coordinate polling, infuriating commuters trying to track approaching cabs (51+ upvotes).
   - **Boarding OTP Delivery Latency:** Seatbelt safety modal pops up over the "View OTP" button, blocking commuters in a hurry.
2. **24.6% Routing & Tracking Friction:**
   - Commuters report ETA discrepancies where MoveInSync displays 15 minutes while Google Maps displays 45 minutes ("cross-country pilgrimage / Bharat Darshan").
3. **5.4% UX Policy Blunder (Direct Cause of 1-Star Spite Reviews):**
   - The app has an unskippable post-trip feedback dialog. Frustrated users who cannot bypass it head directly to the Play Store to leave 1-star reviews out of spite.

---

## 🛠️ Prioritized Engineering Backlog: What to Fix First

We formulated concrete Jira user stories so the engineering and product teams can start tomorrow:

| Ticket ID | Priority | Team | Core Fix |
| :--- | :--- | :--- | :--- |
| **MIS-TECH-P0-01** | `P0 - Blocker` | Mobile Android | Fix Splash Screen Freeze post-update via Room DB fallback migration |
| **MIS-TECH-P0-02** | `P0 - Blocker` | Mobile & Backend | Decouple Boarding OTP from blocking modals; cache OTP offline |
| **MIS-PROD-P1-01** | `P1 - High` | Product UX | Add "Skip" button to post-trip rating dialog to eliminate spite reviews |
| **MIS-TECH-P1-02** | `P1 - High` | Mobile Maps | Latch user map gesture to suppress automatic zoom-out re-centering |
| **MIS-ALGO-P1-03** | `P1 - High` | Routing Algo | Cap pooling detour ratios to max 1.35x of direct point-to-point duration |
| **MIS-TECH-P2-01** | `P2 - Medium` | Mobile Android | Fix false-positive "Update Required" nag screen using Google In-App Update API |

---

## 📈 The Play Store Reputation Hack: 4.32★ $\rightarrow$ 4.70★

MoveInSync runs **1.5 Million rides daily**. Satisfied commuters do not spontaneously open the Play Store to rate 5 stars. Frustrated commuters do.

By integrating the **Google Play In-App Review API**:
1. Target commuters who complete $\ge 5$ consecutive on-time rides with 5-star driver feedback.
2. Trigger the native Google in-app rating bottom sheet.
3. Capturing just **0.5%** of daily satisfied rides generates **~7,500 organic 5-star ratings/month**, lifting the public score to **4.65+★ within 60 days**.

---

## 🚀 Reusable Pipeline: Solving the Recurring Ask

The assignment notes: *“‘How are our Play Store ratings?’ - this is a question we'll keep asking from time to time. It is not a one-time ask.”*

This repository is built as an end-to-end, reusable monitoring engine:

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Ingest Fresh Reviews from Play Store
```bash
python src/scraper.py --count 400
```
*Pulls newest and most-relevant reviews, deduplicates by ID, and stores raw data in `data/`.*

### 3. Run Taxonomy & Severity Classifier
```bash
python src/analyzer.py
```
*Classifies reviews into 6 functional categories, 7 journey touchpoints, and 4 severity levels.*

### 4. Re-generate Executive Report
```bash
python src/report_generator.py
```
*Generates an updated `RECOMMENDATION_REPORT.md`.*

### 5. Launch Interactive Executive Dashboard
```bash
streamlit run app.py
```
*Opens an interactive visual dashboard with version regression charts, touchpoint breakdowns, and ticket filters.*

---

## 📁 Repository Structure
```
MoveInSync/
├── .gitignore
├── README.md                      # Project overview and quickstart
├── ARCHITECTURE.md                # System design & architecture deep-dive
├── RECOMMENDATION_REPORT.md       # Full executive recommendation document
├── requirements.txt               # Python package dependencies
├── app.py                         # Streamlit Interactive Monitoring Dashboard
├── data/
│   ├── app_metadata.json          # Live Play Store app metadata
│   ├── raw_reviews.json           # Raw ingested Play Store reviews
│   ├── raw_reviews.csv            # Raw reviews in tabular format
│   ├── analyzed_reviews.json      # Structured reviews with taxonomy & drag scores
│   └── analyzed_reviews.csv       # Analyzed reviews in tabular format
└── src/
    ├── __init__.py
    ├── scraper.py                 # Automated Google Play ingestion module
    ├── analyzer.py                # Multi-dimensional taxonomy & root cause classifier
    ├── prioritization.py          # RICE prioritization & Jira ticket generator
    └── report_generator.py        # Executive report markdown generator
```
