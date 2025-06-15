import logging
from typing import Dict, Any
from google.adk.agents import LLmAgent
from google.adk.tools import FunctionTool
from .sentiment_analysis_agent import analyze_sentiment_tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@FunctionTool
def process_portfolio_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process portfolio analysis request.
    
    Args:
        input_data: Dictionary containing portfolio information and analysis parameters
        
    Returns:
        Dictionary containing analysis results
    """
    logger.info("Received portfolio request")
    logger.info(f"Input data: {input_data}")
    
    try:
        # Extract portfolio information
        portfolio = input_data.get('portfolio', [])
        risk_tolerance = input_data.get('risk_tolerance', 'moderate')
        investment_goals = input_data.get('investment_goals', [])
        time_horizon = input_data.get('time_horizon', '5-10 years')
        
        logger.info(f"Processing portfolio with {len(portfolio)} assets")
        logger.info(f"Risk tolerance: {risk_tolerance}")
        logger.info(f"Investment goals: {investment_goals}")
        logger.info(f"Time horizon: {time_horizon}")
        
        # Process each asset
        results = []
        for asset in portfolio:
            logger.info(f"Processing asset: {asset}")
            symbol = asset.get('symbol')
            quantity = asset.get('quantity')
            purchase_price = asset.get('purchase_price')
            
            # Calculate current value (placeholder - would use real market data)
            current_value = quantity * purchase_price
            logger.info(f"Calculated current value for {symbol}: ${current_value}")
            
            results.append({
                'symbol': symbol,
                'quantity': quantity,
                'purchase_price': purchase_price,
                'current_value': current_value
            })
        
        # Prepare response
        response = {
            'portfolio_analysis': {
                'assets': results,
                'total_value': sum(r['current_value'] for r in results),
                'risk_tolerance': risk_tolerance,
                'investment_goals': investment_goals,
                'time_horizon': time_horizon
            }
        }
        
        logger.info(f"Portfolio analysis complete. Response: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing portfolio request: {str(e)}")
        raise

# Create the main ADK agent
portfolio_agent = LLmAgent(
    name="portfolio_agent",
    description="Analyzes investment portfolios and provides insights.",
    tools=[process_portfolio_request, analyze_sentiment_tool],
    system_prompt="""You are a portfolio analysis agent that helps analyze investment portfolios.
    When given portfolio data, analyze it using the process_portfolio_request tool.
    The tool expects:
    - portfolio: List of assets with symbol, quantity, and purchase_price
    - risk_tolerance: Investment risk tolerance level
    - investment_goals: List of investment goals
    - time_horizon: Investment time horizon
    
    Provide clear insights based on the portfolio analysis results."""
) 