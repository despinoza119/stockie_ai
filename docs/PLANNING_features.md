# Stockie AI — Stock Buying Assistant

## Phase 1: Feature Definition & Project Analysis

> Status: **Planning doc, pre-implementation.** This document defines *what* we are building and *why*, plus the risks we need to design around. A separate technical implementation plan will follow.

---

## 1. Project Vision

Stockie AI is a web-based stock buying assistant that aggregates **fundamental, technical, sentiment, and macro** signals into actionable, **horizon-aware** recommendations (short, mid, long term) for retail-style investors.

The product must work across:

- **US equities** (NYSE, NASDAQ) — best data availability, primary launch market.
- **International equities** — major European/Asian exchanges via vendor APIs.
- **ETFs & index funds** — passive instruments and sector ETFs.
- **Peruvian market (BVL — Bolsa de Valores de Lima)** — strategic differentiator with poor existing tooling; requires custom data sourcing.

### Design principles

1. **Transparency over black-box predictions.** Every recommendation must expose the underlying signals (this is also a regulatory shield — we are an *analysis* tool, not an advisor).
2. **Horizon-aware.** A short-term technical signal and a long-term fundamental thesis are scored and presented separately, never blended into one opaque number.
3. **Source diversity.** Multiple data providers per asset class; graceful degradation when a source fails.
4. **Local-relevance for Peru.** Spanish-language UI option, BVL coverage, and PEN-denominated reporting are first-class, not afterthoughts.

---

## 2. MVP Core Features

These are the features required for a usable v1.0. If any of these are missing, the product is not viable.

### 2.1 Asset universe & data ingestion

- **Ticker search and resolution** across US, international, ETF, and BVL symbols, with disambiguation (e.g., `BAP` on NYSE vs. BVL listings).
- **Daily OHLCV history** ingestion for every covered ticker, stored locally for fast querying and backtesting.
- **Intraday quotes** (15-min delayed acceptable for MVP) for active monitoring.
- **Fundamentals**: income statement, balance sheet, cash flow, key ratios — at least quarterly.
- **Corporate actions**: splits, dividends, ticker changes — required for correct backtesting.
- **FX rates** (USD/PEN, USD/EUR at minimum) for cross-currency portfolio valuation.
- **Macroeconomic series**: interest rates, CPI, GDP, unemployment for US and Peru.
- **Data freshness indicators**: every datapoint shown in the UI carries an "as of" timestamp.

### 2.2 Fundamental analysis module

- Valuation ratios: P/E, P/B, P/S, EV/EBITDA, PEG, dividend yield.
- Quality metrics: ROE, ROIC, gross/operating/net margins, debt-to-equity, interest coverage.
- Growth metrics: revenue, EPS, FCF growth (1Y, 3Y, 5Y CAGR).
- Simplified **DCF valuation** with adjustable assumptions (growth rate, discount rate, terminal value).
- **Peer comparison**: auto-pick 3–5 peers by sector/size, side-by-side ratio table.
- **Fundamental score (0–100)** per ticker, decomposed into Value / Quality / Growth subscores.

### 2.3 Technical analysis module

- Core indicators: SMA/EMA, RSI, MACD, Bollinger Bands, ATR, volume profile.
- Chart pattern detection: support/resistance levels, trend lines, breakouts (rules-based for MVP).
- Multi-timeframe view: daily, weekly, monthly on the same ticker.
- **Technical score (0–100)** combining trend strength, momentum, and mean-reversion signals.
- Customizable indicator overlays in the chart UI.

### 2.4 Sentiment & news module

- **News aggregation** from financial sources (Reuters, Bloomberg via API or RSS where licensed, Yahoo Finance, Investing.com, plus local Peruvian sources like Gestión, Semana Económica).
- **Sentiment scoring** per article using an NLP model (FinBERT or similar finance-tuned LLM).
- **Social signal tracking** (lightweight in MVP): Reddit (r/stocks, r/investing, r/wallstreetbets) mention volume and sentiment.
- Analyst rating aggregation (consensus buy/hold/sell, price targets) where available.
- **Sentiment score (-100 to +100)** per ticker, with the underlying article list one click away.
- Earnings call transcript summarization (LLM-generated) for covered tickers.

### 2.5 Macro & sector module

- Macro dashboard for US and Peru: rates, inflation, currency, key indices (S&P 500, IGBVL/S&P/BVL Peru General).
- Sector heatmap (US 11 GICS sectors + BVL sectors): performance, valuation, momentum.
- **Macro regime indicator** (e.g., "risk-on / neutral / risk-off") derived from rates curve, credit spreads, and equity volatility.
- Sector rotation signals to flag which sectors are leading/lagging the broader market.

### 2.6 Recommendation engine (the core differentiator)

- **Per-ticker recommendation card** showing:
  - Horizon: short (days–weeks), mid (1–6 months), long (1+ years).
  - Action: Strong Buy / Buy / Hold / Reduce / Sell.
  - Confidence (0–100%).
  - The four sub-scores (fundamental, technical, sentiment, macro/sector) that drove the verdict.
  - A plain-language explanation (2–3 sentences) of *why*.
- **Rule-based scoring engine for MVP** (weights configurable per horizon). ML/LLM layering belongs in nice-to-haves so we don't ship a black box on day one.
- Mandatory **disclaimer** on every recommendation: "Informational only, not financial advice."

### 2.7 Portfolio & watchlist

- User can create one or more **watchlists** (e.g., "Tech US," "BVL mining").
- User can create one or more **portfolios** with manual position entry (ticker, shares, cost basis, date).
- Portfolio analytics: total return, time-weighted return, allocation by sector/region/asset class, top contributors/detractors.
- Multi-currency portfolios (USD and PEN at minimum) with daily FX revaluation.

### 2.8 Alerts

- Price alerts (above/below threshold, % change).
- Indicator alerts (RSI crosses 70, MACD crossover, etc.).
- News/sentiment alerts (sudden sentiment drop, breaking news on a watched ticker).
- Delivery via in-app notification and email; push/SMS comes later.

### 2.9 Dashboard & UX

- Landing dashboard summarizing: portfolio status, watchlist movers, top recommendations today, macro snapshot.
- Per-ticker detail page bringing all four analysis modules together.
- **Bilingual UI** (English + Spanish) — essential for the Peru market.
- Light/dark mode.

### 2.10 Accounts & access

- Email/password + OAuth (Google) signup.
- Per-user data isolation, encrypted credentials, password reset flow.
- Free tier with limits (e.g., 1 portfolio, 1 watchlist, 20 tickers) and a paid tier outline — even if monetization comes later, design the data model for it from the start.

---

## 3. Nice-to-Have Features (post-MVP)

Ordered roughly by "biggest user impact ÷ implementation cost."

### 3.1 LLM-powered chat assistant
Natural-language interface: *"Is AAPL a buy right now?"* / *"Compare BAP and CREDICORP on fundamentals."* Implemented as RAG over our own structured data plus a tool-use LLM that calls our scoring endpoints.

### 3.2 Backtesting engine
Let users define rule-based strategies ("buy when RSI < 30 and fundamental score > 70, sell when RSI > 70") and backtest over historical data with realistic transaction costs and slippage. Critical for trust in the recommendation engine.

### 3.3 Paper trading
Simulated portfolios with live prices so users can test recommendations without real money. Big retention driver.

### 3.4 Machine-learning recommendation layer
Once we have enough historical signal-vs-outcome data, train models (gradient boosting first, then sequence models) that learn weights between the four sub-scores per horizon and per market regime. Always presented alongside the rule-based view, never replacing it.

### 3.5 Strategy builder (no-code)
Visual builder for combining indicators and fundamentals into custom screens and signals. Power-user feature, very sticky.

### 3.6 Earnings calendar & event tracking
Upcoming earnings, ex-dividend dates, splits, FDA approvals, BVL-specific events (mining production reports, election calendars).

### 3.7 Crypto coverage
Logical extension if user demand appears; reuses most of the technical/sentiment infrastructure but needs different data providers.

### 3.8 Broker integration / one-click trade
Connect to brokers (Interactive Brokers, Alpaca for US; local Peruvian brokers if APIs exist) to execute recommendations. Major compliance jump — keep behind a clear feature flag.

### 3.9 Mobile app
Either React Native sharing the API, or progressive web app. Mostly relevant after the web product proves itself.

### 3.10 Community & social
Shareable watchlists, published model portfolios, comment threads. Powerful for growth but a moderation burden — defer until product-market fit.

### 3.11 Tax reporting helpers
Realized gain/loss reports per jurisdiction (US 1099-style, Peru SUNAT-aligned). Valuable for retention, low glamour.

### 3.12 Insider trading & institutional flow
Form 4 filings (US), 13F holdings, BVL hechos de importancia. Strong differentiator for serious users.

---

## 4. Non-functional Requirements & Risk Areas

These often kill projects more than missing features do.

### 4.1 Legal & compliance
- We are **not** a registered investment advisor. Every page that shows a recommendation must carry a disclaimer.
- Terms of Service and Privacy Policy required before the first external user.
- Peru (SMV) and US (SEC) both regulate investment advice — staying on the "tools and information" side of the line is non-negotiable.
- Data licensing: many "free" feeds prohibit redistribution. Read every TOS, document which fields can be shown to users.

### 4.2 Data quality
- BVL data is the highest-risk source. Plan for: manual scraping of BVL's website as a fallback, a daily QA report comparing sources, and explicit "data uncertain" badges on the UI when sources disagree.
- Survivorship bias matters for backtesting — keep delisted tickers in the dataset.
- Adjust for splits and dividends consistently across modules.

### 4.3 Performance & scale
- The dashboard must load in under ~2 seconds for a returning user. Pre-compute scores; don't recompute on each page view.
- Sentiment pipeline is the heaviest workload — batch it on a schedule, not on user request.

### 4.4 Security
- Financial data attracts attackers. Treat the auth, session, and (future) broker-token surfaces as production-grade from day one.
- Secrets in env vars or a secret manager, never in the repo. Rotate API keys.
- Rate-limit public endpoints.

### 4.5 Cost
- Bloomberg/Reuters/Refinitiv are out of budget for v1. Build the data layer with provider abstractions so we can swap (yfinance → Polygon → Alpaca → paid vendor) without rewriting the app.
- LLM inference costs (sentiment, chat) can balloon — cache aggressively and use small finance-tuned models where possible.

### 4.6 BVL-specific data gaps
- No clean free API as of writing. Likely approach: a scheduled scraper of BVL's official site (`bvl.com.pe`) for prices and disclosures, plus manual fundamentals for the top ~50 tickers initially. Treat BVL as a separate ingestion pipeline with its own SLA.

---

## 5. Suggested Tech Direction (preview)

Full implementation plan will be a separate document. Brief preview so we share vocabulary:

- **Python 3.12** as the runtime — current stable, mature library support, good typing.
- **FastAPI** for the API layer (async, OpenAPI for free, great for the chat-assistant tool calling later).
- **PostgreSQL + TimescaleDB extension** for time-series price data alongside relational user/portfolio data in one engine.
- **Redis** for caching scores and rate limiting.
- **Celery (or RQ / Dramatiq)** for scheduled ingestion and the sentiment pipeline.
- **Pandas / Polars** for analytics; Polars where datasets get large.
- **TA-Lib or `pandas-ta`** for technical indicators.
- **FinBERT or a small open-weights finance LLM** for sentiment.
- **Frontend**: Next.js + React + TypeScript + a charting library (TradingView Lightweight Charts or Plotly).
- **Auth**: Auth.js / Authlib + JWT for the API.
- **Deployment**: Docker Compose locally; Fly.io / Render / AWS for production. Keep cloud-portable.

---

## 6. Suggested MVP Scope Cut (recommendation)

If we tried to ship everything in section 2 at once we would not ship. A realistic v1.0 cut:

- US equities + ETFs only at launch. BVL added in v1.1 once the US pipeline is stable.
- Fundamental + technical scoring fully implemented; sentiment limited to news headlines + FinBERT (skip Reddit social).
- Macro module reduced to a static dashboard (no regime indicator yet).
- Recommendation engine is rules-based only.
- Watchlists yes, portfolios yes, alerts limited to price + RSI/MACD.
- English UI only at launch; Spanish localization ships with BVL in v1.1.

This buys us a coherent, shippable product in roughly 3–4 months of part-time work, and a clear path to differentiation in v1.1.

---

## 7. Open Questions for Us To Resolve

1. **Monetization model.** Free + premium tiers, one-time license, or fully free for now? Affects data-provider choices (paid feeds vs. scraping).
2. **Hosting budget.** Determines whether we self-host Postgres or use a managed provider, and how aggressively we use LLM APIs.
3. **Who owns what.** Roughly split between frontend/UX, data engineering, and modeling — decide before we start so we don't both build the same module.
4. **Peru-first vs. US-first launch.** Section 6 assumes US-first for data availability. If marketing into Peru matters more, the order flips and BVL becomes v1.0.
5. **LLM dependency.** Are we willing to depend on a paid LLM API (OpenAI/Anthropic) for the chat assistant later, or do we want everything self-hostable?

---

*Next deliverable: a technical implementation plan covering repository structure, module boundaries, data pipelines, schema, scoring formulas, and a phased build timeline.*
