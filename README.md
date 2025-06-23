# QuantumFin AI Backend

This repository contains the server-side components of **QuantumFin AI**, developed as part of the Agent Development Kit Hackathon with Google Cloud. The backend implements a multi-agent architecture that powers real-time portfolio analysis, market sentiment scoring, risk assessment, and report generation. Front end Repo:- https://github.com/singh2626ss/portfolio-frontend

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Installation](#installation)

   * [Prerequisites](#prerequisites)
   * [Setup](#setup)
   * [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)

   * [Start the Server](#start-the-server)
   * [Access the UI](#access-the-ui)
7. [API Endpoints](#api-endpoints)

   * [Main Endpoints](#main-endpoints)
   * [Agent Endpoints](#agent-endpoints)
8. [Multi-Agent Workflow](#multi-agent-workflow)

   * [Communication Flow](#communication-flow)
   * [Data Flow Example](#data-flow-example)
9. [Data Richness](#data-richness)

   * [Available Data](#available-data)
   * [Visualization Capabilities](#visualization-capabilities)
10. [Configuration](#configuration)

    * [API Rate Limits](#api-rate-limits)
    * [Fallback Mechanisms](#fallback-mechanisms)
11. [Testing](#testing)
12. [Project Structure](#project-structure)
13. [Key Achievements](#key-achievements)
14. [Contributing](#contributing)
15. [License](#license)
16. [Deployment](#deployment)

    * [Local Development](#local-development)
    * [Production Deployment](#production-deployment)

---

## Overview

The backend is built with FastAPI and Python 3.9+. It orchestrates six specialized agents using Google’s Agent Development Kit (ADK), each responsible for a core aspect of the portfolio analysis pipeline:

* Fetching live and historical market data
* Analyzing news sentiment
* Computing risk metrics
* Calculating portfolio performance
* Generating structured reports
* Producing AI-driven recommendations

All functionality is exposed via RESTful endpoints and designed for real-time responsiveness.

---

## Features

* Real-time market data ingestion and caching
* Natural language sentiment analysis of financial news
* Quantitative risk metrics including VaR, drawdown, and concentration
* Portfolio performance calculations and historical returns
* Exportable PDF and JSON report generation
* AI-powered recommendation engine for personalized insights

---

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │◄──►│   FastAPI App   │◄──►│  Alpha Vantage  │
│   (6 Cards)     │    │   (6 Agents)    │    │     API         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   NewsAPI       │
                       │   (Sentiment)   │
                       └─────────────────┘
```

---

## Technology Stack

* **Programming Language**: Python 3.9+
* **Web Framework**: FastAPI
* **Agent Framework**: Google Agent Development Kit (ADK)
* **Data Processing**: pandas, NumPy
* **HTTP Server**: Uvicorn
* **Reporting**: ReportLab (PDF), built-in JSON serializers
* **Testing**: pytest
* **Deployment**: Google Cloud Run

---

## Installation

### Prerequisites

* Python 3.9 or higher
* Poetry (for dependency management)

### Setup

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/Google-Hackathon_Backend.git
   cd Google-Hackathon_Backend
   ```
2. Install dependencies

   ```bash
   poetry install
   ```
3. Prepare environment

   ```bash
   cp .env.example .env
   # edit .env with your API keys and settings
   ```

### Environment Variables

In your `.env` file, set:

```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FINNHUB_API_KEY=your_finnhub_api_key
NEWS_API_KEY=your_news_api_key
GOOGLE_API_KEY=your_google_api_key
DEBUG=True
LOG_LEVEL=INFO
API_RATE_LIMIT=60
CACHE_DURATION=3600
```

---

## Running the Application

### Start the Server

```bash
export ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
poetry run uvicorn app:app --host 0.0.0.0 --port 8000
```

### Access the UI

Navigate to `http://localhost:8000` in your browser.

---

## API Endpoints

### Main Endpoints

* **POST** `/analyze-portfolio`
  Submit portfolio data and receive complete analysis
* **GET** `/`
  Serve the frontend dashboard

### Agent Endpoints

* **GET** `/market-data/{symbol}`
  Real-time quote and historical series for a stock
* **GET** `/sentiment-analysis`
  Aggregated sentiment scores for a list of symbols
* **POST** `/risk-assessment`
  Portfolio risk metrics (VaR, drawdown, concentration)
* **GET** `/health`
  Health check

---

## Multi-Agent Workflow

### Communication Flow

1. Market Data Agent → Fetch prices from Alpha Vantage / Finnhub
2. Sentiment Analysis Agent → Retrieve headlines and score via NewsAPI
3. Risk Assessment Agent → Calculate risk metrics from market data
4. Portfolio Analysis Agent → Compute performance and returns
5. Reporting Agent → Generate PDF and JSON reports
6. AI Insights Agent → Create personalized recommendations

### Data Flow Example

```python
market_data = await market_data_agent.get_quote(symbol)
risk_metrics = await risk_agent.calculate(portfolio, market_data)
sentiment = await sentiment_agent.summarize(symbols)
report = await reporting_agent.create_report(
    portfolio=portfolio,
    market_data=market_data,
    risk=risk_metrics,
    sentiment=sentiment
)
```

---

## Data Richness

### Available Data

* 30-day historical prices per symbol
* Live quotes with caching
* Sentiment from 100+ news articles per symbol
* Risk metrics: VaR, drawdown, HHI
* Portfolio performance and allocation breakdown

### Visualization Capabilities

* Line charts for price history and growth
* Pie charts for allocation and concentration
* Bar charts for risk breakdown
* Timelines for sentiment shifts

---

## Configuration

### API Rate Limits

* Alpha Vantage: 25 calls/day (free), 500 calls/day (premium)
* Finnhub: 60 calls/minute
* NewsAPI: 1000 requests/day

### Fallback Mechanisms

* Caching to avoid rate limits
* Synthetic data when APIs fail
* Graceful error handling

---

## Testing

Run the full test suite:

```bash
poetry run pytest
```

* **test\_system.py**: end-to-end agent and API integration
* **test\_market\_data.py**, **test\_sentiment.py**, **test\_risk.py**: individual agents

---

## Project Structure

```
Google-Hackathon_Backend/
├── agent/
│   ├── market_data_agent.py
│   ├── sentiment_analysis_agent.py
│   ├── risk_assessment_agent.py
│   ├── portfolio_analysis_agent.py
│   ├── reporting_agent.py
│   └── ai_insights_agent.py
├── app.py
├── .env.example
├── requirements.txt
├── reports/
├── static/
└── README.md
```

---

## Key Achievements

* Six agents collaborating in real time
* End-to-end portfolio analysis pipeline
* PDF & JSON report generation
* AI-driven recommendations
* Deployed on Google Cloud Run

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Describe feature"`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

---


**QuantumFin AI Backend**
Part of the Agent Development Kit Hackathon with Google Cloud
