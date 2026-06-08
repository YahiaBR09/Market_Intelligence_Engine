# 🚀 Automated E-Commerce Price Intelligence & Semantic Matching Engine

An enterprise-grade Market Intelligence platform engineered to perform deep-web catalog scraping, bypass advanced anti-bot mitigation matrices, and run context-aware multi-variable product matching. This system orchestrates production-ready data pipelines to track real-time price discrepancies between a **Leading National E-Commerce Retailer** (Client Baseline) and its **Primary Regional Market Competitor** across high-density tool and hardware inventories.

---

## 🛠️ The Technical Challenges & Engineering Solutions

Building this platform required solving complex real-world web scraping and data alignment challenges:

### 1. Advanced Anti-Bot Countermeasures & IP Rate-Limiting (`HTTP 429`)
* **The Challenge:** The competitor website employs aggressive edge network firewalls (e.g., Cloudflare/Sucuri), which triggered sudden `HTTP 429 Too Many Requests` blockers and infinite loop honey-pots after scraping sequential pagination boundaries.
* **The Solution:** Engineered a multi-tiered defense system leveraging `requests.Session` state persistence, randomized human-like navigation delay matrices (`random.uniform`), and dynamic HTTP header mutation. Integrated operational support for real-time cellular gateway IP network rotation (Mobile Hotspot orchestration) to gracefully slip past persistent blacklists without pipeline breaks.

### 2. Obstructive Dynamic Interstitials & Hidden UI Modals
* **The Challenge:** The client site utilized viewport-blocking newsletter subscription overlays and geo-location prompt modals that dynamically interrupted element visibility, causing standard automation scripts to crash due to blocked click pathways.
* **The Solution:** Built the core ingestion layer using `Playwright` with robust asynchronous element wait-states (`wait_for_selector`). Utilized forced-action event dispatches (`click(force=True)`) to programmatically punch through obstructive layout containers, ensuring seamless background data flow.

### 3. Duplicated HTML Markup Artifacts (Price Data Corruption)
* **The Challenge:** The competitor's front-end code often rendered dual overlapping currency nodes inside a single element layout wrapper (one visible for users, one hidden for search engines), causing extracted texts to append corruptly (e.g., extracting `$13.76` as `13.7613.76`).
* **The Solution:** Developed automated downstream text-parsing patterns that validate decimal counts. Integrated fractional-split sequence logic to instantly slice string metrics symmetrically if duplicate signatures are detected, outputting pure, accurate numerical floats.

### 4. Semantic Matching Ambiguity (Screwdrivers vs. Screw Extractors)
* **The Challenge:** Basic text-similarity distance functions (like Levenshtein Ratio) easily cross-contaminated unrelated stock profiles due to high lexical overlap (e.g., matching a `Screwdriver` with a `Screw Extractor` simply because both share the token "Screw"), ruining report integrity.
* **The Solution:** Programmed a **Strict Category Guardrail** pattern inside the `Pandas` matching script. The system parses product contexts to append explicit category "stamps" (`extractor`, `screwdriver`, `pliers`, `spanner`). If a baseline tool group contradicts a candidate match, the score is instantly zeroed out, enforcing 100% domain matching accuracy.

---

## 📁 System Architecture & Directory Blueprint

Market_Intelligence_Engine/
│
├── data/                         # Secure Data Ingestion Directory
│   ├── client_catalog_cache.csv  # Clean baseline product data
│   ├── competitor_prices.csv     # Extracted competitor raw index
│   └── Market_Pricing_Report.xlsx# Final interactive analysis dashboard
│
├── src/                          # Optimized Python Execution Workspace
│   ├── client_harvester.py       # Playwright-driven dynamic catalog engine
│   ├── competitor_crawler.py     # Lightweight search-endpoint parallel spider
│   └── smart_matcher.py          # Unified semantic matching & formatting engine
│
├── .gitignore                    # Local package & runtime exclusion guidelines
├── README.md                     # Technical project documentation
└── requirements.txt              # Production dependency manifests


---

## 💻 Installation & Environment Provisioning

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Market_Intelligence_Engine.git](https://github.com/YOUR_USERNAME/Market_Intelligence_Engine.git)
   cd Market_Intelligence_Engine
Initialize and Activate Virtual Environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies & Browser Dependencies:

Bash
pip install -r requirements.txt
playwright install chromium
📈 Execution Pipeline
To refresh live market pricing indices and synthesize the final analytical matrix, execute the modular processing nodes sequentially within the project root:

Bash
# Step 1: Harvest dynamic baseline inventory data
python src/Customer_web_scrape.py

# Step 2: Extract corresponding competitor catalog layers
python src/competitor_web_scrape.py

# Step 3: Run semantic correlation mapping & generate styled report
python src/matcher.py
📊 Strategic Deliverable Features
The processing sequence automatically builds a beautifully formatted, executive-ready dashboard saved to data/Market_Pricing_Report.xlsx. Leveraged openpyxl to inject corporate thematic styling and conditional fills:

🟢 We are Cheaper (Green Fill): Instantly highlights stock profiles where the client holds a distinct price-advantage over the competitor.

🟠 Competitor is Cheaper (Orange Fill): Isolates margin optimization risks and critical pricing markdown blind spots.

🔵 Unique Product (Blue Fill): Maps unique catalog structures entirely uncontested by rival regional retail infrastructure, highlighting key market exclusivity opportunities.

Disclaimer: Project code and variables have been completely generalized, sanitized, and scrubbed of specific production domains/private keys to preserve intellectual confidentiality and proprietary client data agreements.
