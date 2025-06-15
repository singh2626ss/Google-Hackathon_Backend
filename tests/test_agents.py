import pytest
from agent.market_data_agent import MarketDataAgent
from agent.risk_assessment_agent import RiskAssessmentAgent
from agent.reporting_agent import ReportingAgent
from agent.personalization_agent import PersonalizationAgent
from agent.sentiment_analysis_agent import SentimentAnalysisAgent

def test_market_data_agent():
    """Test market data agent initialization."""
    agent = MarketDataAgent()
    assert agent is not None

def test_risk_assessment_agent():
    """Test risk assessment agent initialization."""
    agent = RiskAssessmentAgent()
    assert agent is not None

def test_reporting_agent():
    """Test reporting agent initialization."""
    agent = ReportingAgent()
    assert agent is not None

def test_personalization_agent():
    """Test personalization agent initialization."""
    agent = PersonalizationAgent()
    assert agent is not None

def test_sentiment_analysis_agent():
    """Test sentiment analysis agent initialization."""
    agent = SentimentAnalysisAgent()
    assert agent is not None

async def test_portfolio_analysis():
    """Test complete portfolio analysis workflow."""
    # Initialize agents
    market_agent = MarketDataAgent()
    risk_agent = RiskAssessmentAgent()
    sentiment_agent = SentimentAnalysisAgent()
    reporting_agent = ReportingAgent()
    
    # Test portfolio data
    portfolio = [
        {'symbol': 'AAPL', 'quantity': 10, 'purchase_price': 150.0},
        {'symbol': 'GOOGL', 'quantity': 5, 'purchase_price': 2800.0},
        {'symbol': 'MSFT', 'quantity': 8, 'purchase_price': 300.0}
    ]
    
    # Get market data for each stock
    market_data = {}
    for stock in portfolio:
        quote = await market_agent.get_stock_quote(stock['symbol'])
        market_data[stock['symbol']] = quote
    print("\nMarket Data:", list(market_data.values()))
    
    # Get risk assessment (fixed method name)
    risk_analysis = await risk_agent.calculate_portfolio_risk(portfolio, market_data)
    print("\nRisk Analysis:", risk_analysis)
    
    # Get sentiment analysis
    sentiment_analysis = await sentiment_agent.analyze_sentiment("Portfolio analysis for AAPL, GOOGL, MSFT.")
    print("\nSentiment Analysis:", sentiment_analysis)
    
    # Generate report
    report = await reporting_agent.generate_portfolio_report(
        portfolio=portfolio,
        market_data=market_data,
        risk_assessment=risk_analysis,
        sentiment_analysis=sentiment_analysis
    )
    print("\nPortfolio Report:", report)
    
    assert market_data is not None
    assert risk_analysis is not None
    assert sentiment_analysis is not None
    assert report is not None

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_portfolio_analysis())
