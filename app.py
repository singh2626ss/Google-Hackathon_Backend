"""
Main FastAPI application for the portfolio management system.
"""

import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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

# Mount templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize agents
sentiment_agent = SentimentAnalysisAgent()
market_data_agent = MarketDataAgent()
risk_agent = RiskAssessmentAgent()
reporting_agent = ReportingAgent()
personalization_agent = PersonalizationAgent()

# Define request/response models
class PortfolioRequest(BaseModel):
    portfolio: List[dict]
    risk_tolerance: str
    investment_goals: List[str]
    time_horizon: str
    user_id: Optional[str] = None

class ExportRequest(BaseModel):
    report: Dict
    format: str = 'json'

class HistoricalComparisonRequest(BaseModel):
    report: Dict
    lookback_days: int = 30

class PortfolioResponse(BaseModel):
    timestamp: str
    portfolio_summary: Dict
    performance_analysis: Dict
    risk_analysis: Dict
    market_sentiment: Dict
    recommendations: List[dict]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze-portfolio")
async def analyze_portfolio(request: PortfolioRequest):
    """
    Analyze a portfolio and generate a comprehensive report.
    """
    try:
        logger.info(f"Received portfolio analysis request: {request}")
        
        # Get market data and sentiment for each position in parallel
        import asyncio
        portfolio = request.portfolio
        
        async def get_data(position):
            symbol = position['symbol']
            quantity = position['quantity']
            purchase_price = position['purchase_price']
            quote = await market_data_agent.get_stock_quote(symbol)
            sentiment = await sentiment_agent.get_market_sentiment(symbol)
            current_price = quote['current_price']
            position_value = quantity * current_price
            return {
                'symbol': symbol,
                'quantity': quantity,
                'purchase_price': purchase_price,
                'current_price': current_price,
                'position_value': position_value,
                'return_percentage': ((current_price - purchase_price) / purchase_price) * 100,
                'sentiment': sentiment['sentiment'] if 'sentiment' in sentiment else sentiment
            }, quote
        
        results = await asyncio.gather(*(get_data(pos) for pos in portfolio))
        portfolio_data = [r[0] for r in results]
        market_data = {pos['symbol']: quote for pos, (_, quote) in zip(portfolio, results)}
        
        # Calculate risk metrics
        risk_metrics = await risk_agent.calculate_portfolio_risk(portfolio, market_data)
        
        # Aggregate sentiment for the whole portfolio (optional: use first symbol's sentiment for now)
        sentiment_analysis = portfolio_data[0]['sentiment'] if portfolio_data else {}
        
        # Generate portfolio report
        report = await reporting_agent.generate_portfolio_report(
            portfolio=portfolio,
            market_data=market_data,
            risk_assessment=risk_metrics,
            sentiment_analysis=sentiment_analysis
        )
        
        return report
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        raise

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/export-report")
async def export_report(request: ExportRequest):
    """
    Export portfolio report in specified format (json, csv, or pdf).
    """
    try:
        logger.info(f"Exporting report in {request.format} format")
        
        # Validate format
        if request.format not in ['json', 'csv', 'pdf']:
            raise HTTPException(status_code=400, detail="Unsupported export format")
        
        # Export report
        export_data = await reporting_agent.export_report(request.report, request.format)
        
        # Set appropriate content type
        content_type = {
            'json': 'application/json',
            'csv': 'text/csv',
            'pdf': 'application/pdf'
        }[request.format]
        
        # Set filename
        filename = f"portfolio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{request.format}"
        
        return Response(
            content=export_data,
            media_type=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        logger.error(f"Error exporting report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/historical-comparison")
async def get_historical_comparison(request: HistoricalComparisonRequest):
    """
    Get historical comparison data for the current report.
    """
    try:
        logger.info(f"Generating historical comparison with {request.lookback_days} days lookback")
        
        comparison_data = await reporting_agent.get_historical_comparison(
            request.report,
            request.lookback_days
        )
        
        return comparison_data
        
    except Exception as e:
        logger.error(f"Error generating historical comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 