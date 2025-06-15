"""
Main FastAPI application for the portfolio management system.
"""

import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from agent.sentiment_analysis_agent import SentimentAnalysisAgent
from agent.market_data_agent import MarketDataAgent
from agent.risk_assessment_agent import RiskAssessmentAgent
from agent.reporting_agent import ReportingAgent
from agent.personalization_agent import PersonalizationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio Management API",
    description="API for portfolio management and analysis",
    version="1.0.0"
)

# Initialize agents
sentiment_agent = SentimentAnalysisAgent()
market_agent = MarketDataAgent()
risk_agent = RiskAssessmentAgent()
reporting_agent = ReportingAgent()
personalization_agent = PersonalizationAgent()

# Define request/response models
class PortfolioRequest(BaseModel):
    portfolio: List[Dict]
    risk_tolerance: str
    investment_goals: List[str]
    time_horizon: str
    user_id: Optional[str] = None

class PortfolioResponse(BaseModel):
    timestamp: str
    portfolio_summary: Dict
    performance_analysis: Dict
    risk_analysis: Dict
    market_sentiment: Dict
    recommendations: List[dict]

@app.post("/analyze-portfolio", response_model=PortfolioResponse)
async def analyze_portfolio(request: PortfolioRequest):
    """
    Analyze a portfolio and generate a comprehensive report.
    """
    try:
        logger.info(f"Received portfolio analysis request: {request}")
        
        # Get market data for all symbols
        market_data = {}
        for position in request.portfolio:
            symbol = position['symbol']
            market_data[symbol] = await market_agent.get_stock_quote(symbol)
        
        # Get sentiment analysis
        sentiment_analysis = await sentiment_agent.get_market_sentiment(
            request.portfolio[0]['symbol']  # Using first symbol for now
        )
        
        # Calculate risk assessment
        risk_assessment = await risk_agent.calculate_portfolio_risk(
            request.portfolio,
            market_data
        )
        
        # Generate report
        report = await reporting_agent.generate_portfolio_report(
            request.portfolio,
            market_data,
            risk_assessment,
            sentiment_analysis
        )
        
        # If user_id is provided, get personalized report
        if request.user_id:
            report = await personalization_agent.get_customized_report(
                request.user_id,
                report
            )
        
        return report
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Create the main portfolio agent
portfolio_agent = Agent(
    name="portfolio_agent",
    description="Analyzes portfolios and generates comprehensive reports.",
    tools=[
        FunctionTool(analyze_portfolio),
        FunctionTool(health_check)
    ],
)

# Register the agent with FastAPI
# app.include_router(portfolio_agent.router)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Portfolio Manager API server")
    uvicorn.run(app, host="0.0.0.0", port=8000) 