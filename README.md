# � Price Intelligence Tool - Smart Market Comparison

### Never lose a sale due to competitive pricing again!

This smart tool automatically compares your product prices against competitors and highlights opportunities to win more customers. Get real-time price insights, identify your competitive advantages, and make data-driven pricing decisions—all in seconds.

---

## ✨ What This Tool Does

**Automatically collect and compare prices** from your store and competitor websites, then generate a beautiful report that shows:

- 🟢 **Your Price Wins** — Products where you're cheaper and gaining competitive advantage
- 🟠 **Price Gaps** — Where competitors are undercutting you (and what to do about it)
- 🔵 **Your Exclusive Products** — Items only you carry (premium positioning opportunity)

No manual data entry. No spreadsheet headaches. Just smart automation that saves you time and increases profits.

---

## 🚀 Get Started in 3 Steps

### Step 1: Set Up
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Collect Data
Run these commands to gather your pricing data:
```bash
python src/Customer_web_scrape.py
python src/competitor_web_scrape.py
```

### Step 3: Get Your Report
```bash
python src/matcher.py
```

Your beautiful, color-coded comparison report will appear in the data folder. Done!

---

## 📊 What You Get

- **Instant Price Comparison** — See all pricing differences at a glance
- **Color-Coded Report** — Easy-to-read visual indicators (no training needed)
- **Actionable Insights** — Know exactly where to adjust prices to win more sales
- **Automated & Smart** — Handles complex matching, so you don't have to
- **Ready to Present** — Professional reports that impress your team and investors

---

## 📁 Project Structure

```
├── data/                          # Your price data goes here
│   ├── competitor_prices.csv
│   └── client_real_prices.csv
│
├── src/                           # The automation scripts
│   ├── Customer_web_scrape.py
│   ├── competitor_web_scrape.py
│   └── matcher.py
│
└── requirements.txt               # Everything needed to run
```

---

## 💡 Why This Matters

- **Stay Competitive** — Don't let price mismatches hurt your business
- **Make Smart Decisions** — Use real data, not guesses
- **Save Time** — Automation handles what takes hours manually
- **Increase Profits** — Identify pricing opportunities instantly

---

## 📝 Requirements

See `requirements.txt` for all dependencies. Installation is straightforward—just follow the setup steps above.

---

## 🎯 Perfect For

Retail business owners, e-commerce managers, and teams that want to understand their competitive position without the complexity.

Start comparing. Start winning. 🏆
