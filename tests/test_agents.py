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
