# AI-Powered Threat Intelligence Aggregation Platform

## Overview

This project aims to proactively assist Security Operations Centers (SOCs) by aggregating, analyzing, and visualizing Cyber Threat Intelligence (CTI) from multiple sources. It enables real-time detection of Indicators of Compromise (IOCs), vulnerabilities (CVEs), threat actors, and TTPs (Tactics, Techniques, Procedures), leveraging AI and NLP for automated intelligence enrichment and classification.

## Features

- Automatic CTI data collection from:
  - Open-source feeds (AlienVault, MISP, URLHaus, NVD, etc.)
- Named Entity Recognition (NER) to extract:
  - IOCs (IPs, domains, hashes)
  - CVEs with severity and vector info
  - Threat actors and techniques
- Threat classification and MITRE ATT&CK mapping (SOON)
- Centralized storage in MongoDB / Elasticsearch (SOON)
- Interactive dashboard (React + Flask)
- Custom alerting (email)
- SIEM integration (Wazuh, QRadar, etc.) (SOON)

## Tech Stack

- **Backend**: Python (Flask, requests, spaCy, transformers)
- **Frontend**: React.js
- **Database**: MongoDB / Elasticsearch
- **Deployment**: Local

## Project Structure

```bash
└── soc-assistant
    ├── README.md
    ├── data
    │   ├── *.json
    └── src
        ├── AI_NLP
        │   ├── build_training_data.py
        │   ├── ner_config.cfg
        │   ├── ner_cti_model
        │   │   ├── model-best/
        │   │   └── model-last/
        │   ├── test.py
        │   ├── train.spacy
        │   ├── train_ner_model.py
        │   └── waking_model.py
        ├── dashboard
        │   ├── README.md
        │   ├── package-lock.json
        │   ├── package.json
        │   ├── public/
        │   └── src
        │       ├── App.css
        │       ├── App.js
        │       ├── App.test.js
        │       ├── components
        │       │   ├── AbuseDetail.js
        │       │   ├── CveList.css
        │       │   ├── CveList.js
        │       │   ├── EventList.css
        │       │   ├── EventList.js
        │       │   ├── Home.css
        │       │   ├── Home.js
        │       │   ├── IOCDetail.css
        │       │   ├── IOCDetail.js
        │       │   ├── MaliciousURLs.js
        │       │   ├── VTCheckForm.js
        │       │   ├── VTDetail.js
        │       │   └── aiModel.js
        │       ├── index.css
        │       ├── index.js
        │       ├── logo.svg
        │       ├── reportWebVitals.js
        │       └── setupTests.js
        └── data_collection
            ├── Malshare
            │   └── data_extraction.py
            ├── NVD
            │   └── data_extraction.py
            ├── URLhaus
            │   └── data_extraction.py
            ├── X-Twitter
            │   └── data_extraction.py
            ├── abuseipdb
            │   └── data_extraction.py
            ├── alerting.py
            ├── alienvault
            │   ├── data_extraction.py
            │   └── normalize_data.py
            ├── auto_collection.py
            ├── dashboard_builder.py
            ├── launch.py
            ├── misp
            │   ├── data_extraction.py
            │   └── normalize_data.py
            └── virus_total
                └── data_extraction.py
```

## Getting Started

### IMPORTANT

If you're encountring an OpenSSL error, please run this command:
```bash
NODE_OPTIONS=--openssl-legacy-provider npm start
```

### 0. Prerequisites

```bash
sudo apt install python3-pip
sudo apt install python3.12-venv
python3 -m venv soc_env
source soc_env/bin/activate
git clone git@github.com:1MrazorT1/soc-assistant.git
cd soc-assistant/
pip install -r requirements.txt
```

### 1. Start backend

```bash
python fetch_all.py
python launch.py 
```

### 2. Start frontend

```bash
cd src/dashboard
npm install
npm start
```
