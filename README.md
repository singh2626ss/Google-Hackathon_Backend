# Portfolio Management API

A FastAPI-based portfolio management system that provides comprehensive analysis of investment portfolios using various agents for market data, sentiment analysis, risk assessment, and personalized recommendations.

## Features

- **Portfolio Analysis**: Analyze investment portfolios with detailed performance metrics
- **Market Data Integration**: Real-time market data using Finnhub API
- **Sentiment Analysis**: Market sentiment analysis using TextBlob
- **Risk Assessment**: Portfolio risk analysis with concentration metrics
- **Personalized Recommendations**: Customized investment recommendations based on user preferences

## Setup

1. Clone the repository:
```bash
git clone https://github.com/singh2626ss/Google-Hackathon_Backend.git
cd Google-Hackathon_Backend
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file with your API keys:
```
GOOGLE_CLOUD_API_KEY=your_google_cloud_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here
FMP_API_KEY=your_financial_modeling_prep_api_key_here
```

4. Start the server:
```bash
poetry run python app.py
```

## API Endpoints

### POST /analyze-portfolio
Analyzes a portfolio and generates a comprehensive report.

Request body:
```json
{
    "portfolio": [
        {
            "symbol": "AAPL",
            "quantity": 10,
            "purchase_price": 150.0
        }
    ],
    "risk_tolerance": "moderate",
    "investment_goals": ["growth", "income"],
    "time_horizon": "5-10 years"
}
```

### GET /health
Health check endpoint.

## Testing

Run the test script:
```bash
poetry run python test_api.py
```

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
