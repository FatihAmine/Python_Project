#  ShopVerse : E-Commerce Analytics Platform

A full-stack e-commerce demo that doesn't just sell products : it **tracks everything**. Every click, every page view, every "Add to Cart" is captured, analyzed, and visualized through a custom-built analytics pipeline.

I built this to explore how real e-commerce companies handle user behavior data end-to-end: from raw event collection → data processing → dashboards → machine learning predictions.

---

## What It Does

**ShopVerse** is a fake online store (30 products, full cart system) wired up with a serious analytics backend:

- **Frontend store** : Browse products, view details, add to cart, manage your basket. It looks and feels like a real shop.
- **Event tracking** : Every user interaction gets logged as a JSON file on the server. No third-party dependency required.
- **Google Analytics integration** : GA4 runs alongside the custom tracker so you can compare the two.
- **Python analytics engine** : Parses the raw logs, calculates metrics, and generates reports automatically.
- **Streamlit dashboard** : Interactive charts showing traffic, popular products, conversion funnels, and more.
- **ML predictions** : A Random Forest model trained on user sessions to predict who's likely to convert (visit cart).
- **Apache NiFi** : Data flow automation for processing logs at scale.
- **Marquez** : Data lineage tracking so you can see where your data came from and where it went.

---

## Architecture

Here's how the pieces fit together:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ Homepage │  │ Product  │  │   Cart   │                      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                      │
│       │              │             │                            │
│       └──────────────┼─────────────┘                            │
│                      │                                          │
│              tracker.js + ga-tracker.js                         │
│              (captures every interaction)                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │   Express.js Server    │
          │   POST /api/log-event  │──────────► Google Analytics 4
          └────────┬───────────────┘
                   │
                   ▼
          ┌────────────────────┐
          │   logs/YYYYMMDD/   │   ◄── Raw JSON events
          │   *.json files     │       (one file per event)
          └────────┬───────────┘
                   │
        ┌──────────┼──────────────┐
        ▼          ▼              ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │   NiFi   │ │  Python  │ │  Marquez │
  │ Data Flow│ │ Pipeline │ │ Lineage  │
  └──────────┘ └────┬─────┘ └──────────┘
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
   ┌──────────┐ ┌────────┐ ┌────────────┐
   │ Metrics  │ │  CSVs  │ │  ML Model  │
   │ summary  │ │ charts │ │ prediction │
   └──────────┘ └────────┘ └────────────┘
                    │
                    ▼
          ┌────────────────────┐
          │ Streamlit Dashboard│
          │  (3 themes, live)  │
          └────────────────────┘
```

---

## Data Pipeline Flow

```
   Raw Events          Parse & Clean        Aggregate            Visualize
  ┌─────────┐         ┌─────────────┐      ┌──────────┐        ┌───────────┐
  │  JSON   │────────►│ log_parser  │─────►│ metrics  │───────►│ dashboard │
  │  files  │         │    .py      │      │   .py    │        │    .py    │
  └─────────┘         └─────────────┘      └──────────┘        └───────────┘
                                                │
                                                ▼
                                          ┌──────────┐
                                          │  ML      │
                                          │ analysis │
                                          │   .py    │
                                          └──────────┘
```

1. **log_parser.py** : Reads all JSON event files from `logs/`, parses timestamps, and loads everything into a Pandas DataFrame.
2. **metrics.py** : Takes the DataFrame and calculates: events by type, events by page, traffic over time, conversion funnel, e-commerce metrics (add-to-cart counts per product).
3. **generate_analytics.py** : Orchestrates the pipeline: calls the parser, runs the metrics, saves CSV files and a summary JSON to `analytics/output/`.
4. **ml_analysis.py** : Builds user-level features (total events, unique pages, product views, session duration, clicks) and trains a Random Forest to predict cart conversion.
5. **dashboard.py** : Streamlit app that loads the generated CSVs and renders interactive Plotly charts. Supports 3 themes, Google Analytics comparison view, and live ML results.

---

## Project Structure

```
shopverse/
├── server.js                  # Express server — serves the store + logs events
├── package.json               # Node.js dependencies (express, cors)
├── docker-compose.yml         # NiFi container setup
│
├── public/                    # Frontend (served as static files)
│   ├── index.html             # Homepage — product grid
│   ├── product.html           # Product detail page
│   ├── cart.html              # Shopping cart page
│   ├── css/
│   │   └── style.css          # All the styling
│   └── js/
│       ├── products.js        # Product catalog (30 items with images)
│       ├── app.js             # Main app logic — rendering, cart, toasts
│       ├── tracker.js         # Custom event tracker (sends to /api/log-event)
│       └── ga-tracker.js      # Google Analytics 4 event bridge
│
├── analytics/                 # Python analytics pipeline
│   ├── log_parser.py          # JSON log file → Pandas DataFrame
│   ├── metrics.py             # Metric calculations (funnel, e-commerce, time)
│   ├── generate_analytics.py  # Runs the full pipeline, saves CSVs
│   ├── ml_analysis.py         # Random Forest conversion prediction
│   ├── dashboard.py           # Streamlit dashboard (3 themes, 4 views)
│   ├── ga_fetcher.py          # Pulls data from Google Analytics API
│   ├── deploy_nifi.py         # NiFi flow deployment helper
│   ├── nifi_flow.json         # NiFi flow definition
│   └── requirements.txt       # Python dependencies
│
├── marquez/                   # Data lineage tracking
│   ├── docker-compose.yml     # Marquez + Postgres setup
│   ├── lineage_event.json     # Sample OpenLineage event
│   └── register_lineage.sh    # Script to register lineage with Marquez API
│
└── logs/                      # Runtime event logs (auto-generated)
    └── YYYYMMDD/              # Organized by date
        └── *.json             # One JSON file per event
```

---

## How to Run It

### Prerequisites

- **Node.js** (v16+) : for the web server
- **Python** (3.9+) : for the analytics pipeline
- **Docker** (optional) : only if you want NiFi or Marquez

### 1. Start the Web Store

```bash
# Clone the repo
git clone https://github.com/FatihAmine/Python_Project.git
cd Python_Project

# Install Node dependencies
npm install

# Start the server
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser. Browse around, click products, add stuff to your cart — every interaction gets saved to the `logs/` folder.

### 2. Run the Analytics Pipeline

```bash
# Install Python dependencies
pip install -r analytics/requirements.txt

# Generate analytics from your logs
python analytics/generate_analytics.py

# Train the ML model
python analytics/ml_analysis.py
```

This reads all the event logs, crunches the numbers, and saves the results to `analytics/output/`.

### 3. Launch the Dashboard

```bash
streamlit run analytics/dashboard.py
```

Open [http://localhost:8501](http://localhost:8501) and you'll see:
- **Local Logs** : KPI cards + traffic charts from your server logs
- **Google Analytics** : Compare with GA4 data (needs credentials)
- **Comparison View** : Side-by-side: server logs vs Google Analytics
- **Predictions (ML)** : Model accuracy, feature importance, confusion matrix

### 4. Start NiFi (Optional)

```bash
docker-compose up -d
```

NiFi will be available at [https://localhost:8443](https://localhost:8443) (login: `admin` / `ShopVerseAnalytics2026!`).

### 5. Start Marquez (Optional)

```bash
cd marquez
docker-compose up -d
```

Marquez UI at [http://localhost:3002](http://localhost:3002), API at [http://localhost:5000](http://localhost:5000).

---

## Tech Stack

| Layer          | Technology                                            |
|----------------|-------------------------------------------------------|
| Frontend       | HTML, CSS, Vanilla JavaScript                         |
| Backend        | Node.js, Express.js                                   |
| Tracking       | Custom JS tracker + Google Analytics 4                |
| Analytics      | Python, Pandas, Plotly                                |
| Dashboard      | Streamlit                                             |
| ML             | scikit-learn (Random Forest)                          |
| Data Pipeline  | Apache NiFi                                           |
| Lineage        | Marquez (OpenLineage)                                 |
| Containers     | Docker, Docker Compose                                |

---

## The ML Model

The conversion prediction model works like this:

1. **Group events by user** : Each user's session becomes one row
2. **Extract features:**
   - Total number of events
   - Number of unique pages visited
   - Number of product detail views
   - Session duration (seconds)
   - Total clicks
3. **Target variable** : Did the user visit the cart page? (yes = 1, no = 0)
4. **Model** : Random Forest Classifier (100 trees)
5. **Split** : 80% train, 20% test with stratification

The dashboard shows accuracy, precision, recall, F1-score, and which features matter most for predicting conversions.

---

## Screenshots

Once you have the dashboard running, you'll see something like:

- **KPI Cards** : Total actions, unique visitors, cart additions, page views
- **Traffic Over Time** : Line chart showing when users are most active
- **Popular Products** : Horizontal bar chart of most-added-to-cart items
- **Shopping Funnel** : Home → Product View → Add to Cart → Cart (with drop-off %)
- **ML Results** : Model performance metrics + feature importance chart

The dashboard supports 3 themes: **Clean Light**, **Midnight (Dark)**, and **Ocean Blue**.

---
