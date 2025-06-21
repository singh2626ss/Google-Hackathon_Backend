# 🤖 AI-Powered Portfolio Management System

A sophisticated **multi-agent AI workflow** system that provides real-time portfolio analysis, market sentiment, risk assessment, and intelligent insights using 6 specialized AI agents.

## 🚀 Features

### **6 Interactive Dashboard Cards**
- 📊 **Portfolio Performance** - Real-time value tracking and performance metrics
- 📈 **Market Sentiment** - AI-powered sentiment analysis with recent events
- ⚠️ **Risk Metrics** - Advanced risk assessment and volatility analysis
- 📰 **Market News Summary** - Latest market news and insights
- 🎯 **Recent Events** - Company-specific impactful events extraction
- 🤖 **AI Q&A** - Interactive portfolio queries and insights

### **Multi-Agent AI Architecture**
- **Market Data Agent** - Real-time stock prices and historical data
- **Sentiment Analysis Agent** - News sentiment analysis with recent events
- **Risk Assessment Agent** - Portfolio risk metrics and volatility
- **Portfolio Analysis Agent** - Performance calculations and returns
- **Reporting Agent** - Comprehensive report generation
- **AI Insights Agent** - Intelligent portfolio recommendations

## 🏗️ Architecture

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

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **AI/ML**: TextBlob, Multi-agent workflow
- **APIs**: Alpha Vantage (Market Data), NewsAPI (Sentiment)
- **Deployment**: Poetry, Uvicorn

## 📦 Installation

### Prerequisites
- Python 3.9+
- Poetry (package manager)

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Google-Hackathon_Backend

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables
```env
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
NEWS_API_KEY=your_news_api_key
NEWSDATA_API_KEY=your_newsdata_key
```

## 🚀 Running the Application

### Start the Server
```bash
export ALPHA_VANTAGE_API_KEY=your_key
poetry run uvicorn app:app --host 0.0.0.0 --port 8000
```

### Access the UI
Open your browser and navigate to: `http://localhost:8000`

## 📊 API Endpoints

### Main Endpoints
- `POST /analyze-portfolio` - Complete portfolio analysis
- `GET /` - Frontend dashboard

### Individual Agent Endpoints
- `GET /market-data/{symbol}` - Real-time stock data
- `GET /sentiment-analysis` - Market sentiment analysis
- `POST /risk-assessment` - Portfolio risk metrics
- `GET /health` - Health check

## 🎯 Multi-Agent Workflow

### Agent Communication Flow
1. **Market Data Agent** → Fetches real-time prices and historical data
2. **Sentiment Analysis Agent** → Analyzes news sentiment and extracts recent events
3. **Risk Assessment Agent** → Calculates portfolio risk using market data
4. **Portfolio Analysis Agent** → Computes performance metrics
5. **Reporting Agent** → Generates comprehensive reports
6. **AI Insights Agent** → Provides intelligent recommendations

### Data Flow Example
```python
# Market Data Agent → Risk Assessment Agent
market_data = await market_data_agent.get_stock_quote(symbol)
risk_metrics = await risk_agent.calculate_portfolio_risk(portfolio, market_data)

# Sentiment Analysis Agent → Reporting Agent
sentiment_analysis = await sentiment_agent.get_portfolio_sentiment_summary(symbols)
report = await reporting_agent.generate_portfolio_report(
    portfolio=portfolio,
    market_data=market_data,
    risk_assessment=risk_metrics,
    sentiment_analysis=sentiment_analysis
)
```

## 📈 Data Richness

### Available Data for Visualizations
- **30-day historical price data** per stock
- **Real-time market quotes** with fallback mechanisms
- **Sentiment analysis** with 100+ news articles per stock
- **Risk metrics** including volatility and concentration analysis
- **Recent events** with impact level assessment
- **Portfolio performance** tracking and returns calculation

### Visualization Capabilities
- **Performance Charts** - Line charts showing portfolio growth
- **Risk Distribution** - Pie charts for portfolio allocation
- **Sentiment Timeline** - Sentiment changes over time
- **Volatility Analysis** - Daily returns and risk metrics
- **Event Impact** - Recent events visualization

## 🔧 Configuration

### API Rate Limits
- **Alpha Vantage**: 25 calls/day (free tier), 500 calls/day (premium)
- **NewsAPI**: 1000 requests/day (free tier)

### Fallback Mechanisms
- Dummy data generation when APIs are rate-limited
- Cached responses for improved performance
- Graceful error handling for all endpoints

## 🧪 Testing

### Run System Tests
```bash
# Test all agents and endpoints
poetry run python test_system.py

# Test individual components
poetry run python test_recent_events.py
poetry run python test_market_data.py
```

### Test Portfolio Analysis
```bash
curl -X POST "http://localhost:8000/analyze-portfolio" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio": [
      {"symbol": "AAPL", "quantity": 10, "purchase_price": 150.0},
      {"symbol": "MSFT", "quantity": 5, "purchase_price": 300.0}
    ],
    "risk_tolerance": "moderate",
    "investment_goals": ["growth"],
    "time_horizon": "5-10 years"
  }'
```

## 📋 Project Structure

```
Google-Hackathon_Backend/
├── agent/                          # AI Agents
│   ├── market_data_agent.py       # Real-time market data
│   ├── sentiment_analysis_agent.py # Sentiment analysis
│   ├── risk_assessment_agent.py   # Risk metrics
│   ├── reporting_agent.py         # Report generation
│   ├── personalization_agent.py   # User personalization
│   └── ai_insights_agent.py       # AI insights
├── templates/                      # Frontend templates
│   └── index.html                 # Main dashboard
├── static/                        # Static assets
├── reports/                       # Generated reports
├── app.py                         # FastAPI application
├── requirements.txt               # Dependencies
├── pyproject.toml                # Poetry configuration
└── README.md                     # This file
```

## 🎉 Key Achievements

### **Multi-Agent AI Workflow**
- ✅ 6 specialized AI agents working in harmony
- ✅ Real-time data processing and analysis
- ✅ Intelligent agent communication and data sharing
- ✅ Comprehensive portfolio insights

### **Production-Ready Features**
- ✅ Real-time market data integration
- ✅ Advanced sentiment analysis with recent events
- ✅ Professional risk assessment metrics
- ✅ Beautiful, responsive frontend UI
- ✅ Robust error handling and fallbacks

### **Hackathon Ready**
- ✅ Complete end-to-end functionality
- ✅ Rich data for compelling visualizations
- ✅ Professional-grade architecture
- ✅ Comprehensive documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🚀 Deployment

### Local Development
```bash
poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Production Deployment
```bash
# Set production environment variables
export ALPHA_VANTAGE_API_KEY=your_production_key
export NEWS_API_KEY=your_production_key

# Start production server
poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

---

**Built with ❤️ for Google Hackathon 2024**

*Multi-Agent AI Portfolio Management System - Where Intelligence Meets Investment*
