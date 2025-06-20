# Portfolio Management System

An AI-powered portfolio management system with real-time market analysis, sentiment analysis, and intelligent recommendations using Google ADK.

## Features

- **Portfolio Analysis**: Comprehensive portfolio performance and risk assessment
- **Market Data Integration**: Real-time market data using Alpha Vantage API
- **Sentiment Analysis**: News sentiment analysis for portfolio stocks with real-time news aggregation
- **AI Insights**: Natural language Q&A about portfolios and markets with intelligent responses
- **News Summary**: Automated news summarization and sentiment trends for portfolio stocks
- **Risk Assessment**: Advanced risk metrics and volatility calculations
- **Goal-based Forecasting**: Investment projections based on goals and time horizon
- **Interactive Dashboard**: Beautiful web interface with real-time updates
- **Report Generation**: Comprehensive PDF and JSON reports with visualizations
- **Historical Comparison**: Portfolio performance tracking over time

## Quick Start

### Prerequisites

- Python 3.9+
- Poetry (for dependency management)
- Google Cloud credentials

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Google-Hackathon_Backend
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```bash
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
NEWS_API_KEY=your_news_api_key_here
GOOGLE_CLOUD_API_KEY=your_google_cloud_api_key_here
```

4. Run the application:
```bash
poetry run uvicorn app:app --host 0.0.0.0 --port 8000
```

5. Open your browser and go to `http://localhost:8000`

## API Endpoints

- `GET /` - Web dashboard with interactive portfolio analysis
- `POST /analyze-portfolio` - Comprehensive portfolio analysis with AI insights
- `POST /ai-insights` - Natural language Q&A about portfolios and markets
- `POST /export-report` - Export detailed reports in PDF/JSON format
- `POST /historical-comparison` - Historical data comparison and trends
- `GET /health` - Health check endpoint

## Architecture

The system uses a multi-agent architecture with Google ADK:

- **Market Data Agent**: Fetches real-time and historical market data from Alpha Vantage API
- **Sentiment Analysis Agent**: Analyzes news sentiment for stocks with real-time news aggregation
- **Risk Assessment Agent**: Calculates portfolio risk metrics and volatility analysis
- **Reporting Agent**: Generates comprehensive reports with visualizations
- **AI Insights Agent**: Provides natural language Q&A and intelligent portfolio recommendations
- **Personalization Agent**: Goal-based forecasting and personalized recommendations

## AI Features

### Natural Language Q&A
- Ask questions about your portfolio performance
- Get investment advice and market insights
- Receive personalized recommendations based on your goals

### News Sentiment Analysis
- Real-time news aggregation for portfolio stocks
- Sentiment scoring and trend analysis
- Automated news summaries with key insights

### Risk Assessment
- Portfolio volatility calculations
- Concentration risk analysis
- Diversification scoring
- Risk level classification

### Portfolio Forecasting
- Goal-based investment projections
- Multiple scenario analysis (conservative, moderate, aggressive)
- Time horizon-based planning

## Project Structure

```
Google-Hackathon_Backend/
├── agent/
│   ├── sentiment_analysis_agent.py
│   ├── market_data_agent.py
│   ├── risk_assessment_agent.py
│   ├── reporting_agent.py
│   ├── personalization_agent.py
│   └── ai_insights_agent.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── reports/
├── app.py
├── pyproject.toml
├── .env
└── README.md
```

## Deployment

### Google Cloud Run
1. Set environment variables in Cloud Run:
   - `ALPHA_VANTAGE_API_KEY`
   - `NEWS_API_KEY`
   - `GOOGLE_CLOUD_API_KEY`

2. Deploy using gcloud:
```bash
gcloud run deploy portfolio-manager --source .
```

### Local Development
```bash
poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
