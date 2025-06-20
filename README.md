# Portfolio Management System

An AI-powered portfolio management system with real-time market analysis, sentiment analysis, and intelligent recommendations using Google ADK.

## Features

- **Portfolio Analysis**: Comprehensive portfolio performance and risk assessment
- **Market Data Integration**: Real-time market data using Alpha Vantage API
- **Sentiment Analysis**: News sentiment analysis for portfolio stocks
- **AI Insights**: Natural language Q&A about portfolios and markets
- **Risk Assessment**: Advanced risk metrics and volatility calculations
- **Goal-based Forecasting**: Investment projections based on goals and time horizon
- **Interactive Dashboard**: Beautiful web interface with real-time updates

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

- `GET /` - Web dashboard
- `POST /analyze-portfolio` - Portfolio analysis
- `POST /ai-insights` - AI-powered insights
- `POST /export-report` - Export reports
- `POST /historical-comparison` - Historical data comparison
- `GET /health` - Health check

## Architecture

The system uses a multi-agent architecture with Google ADK:

- **Market Data Agent**: Fetches real-time and historical market data from Alpha Vantage
- **Sentiment Analysis Agent**: Analyzes news sentiment for stocks
- **Risk Assessment Agent**: Calculates portfolio risk metrics
- **Reporting Agent**: Generates comprehensive reports
- **AI Insights Agent**: Provides natural language Q&A
- **Personalization Agent**: Goal-based forecasting and recommendations

## Project Structure

```
portfolio_manager_adk/
├── agent/
│   ├── sentiment_analysis_agent.py
│   ├── market_data_agent.py
│   ├── risk_assessment_agent.py
│   ├── reporting_agent.py
│   └── personalization_agent.py
├── app.py
├── test_api.py
├── pyproject.toml
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
