"""
Risk Assessment Agent for analyzing portfolio risk and volatility.
"""

import logging
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskAssessmentAgent:
    def __init__(self):
        """Initialize the RiskAssessmentAgent."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing RiskAssessmentAgent")

    async def calculate_portfolio_risk(self, portfolio: List[Dict], market_data: Dict) -> Dict:
        """
        Calculate risk metrics for a portfolio.
        
        Args:
            portfolio (List[Dict]): List of portfolio positions
            market_data (Dict): Market data for portfolio symbols
            
        Returns:
            Dict: Risk assessment results
        """
        try:
            self.logger.info("Calculating portfolio risk metrics")
            
            # Calculate position weights
            total_value = sum(pos['quantity'] * market_data[pos['symbol']]['current_price'] 
                            for pos in portfolio)
            
            weights = {
                pos['symbol']: (pos['quantity'] * market_data[pos['symbol']]['current_price']) / total_value
                for pos in portfolio
            }
            
            # Calculate basic risk metrics
            risk_metrics = {
                'total_value': total_value,
                'position_weights': weights,
                'number_of_positions': len(portfolio),
                'concentration_risk': self._calculate_concentration_risk(weights),
                'timestamp': datetime.now().isoformat()
            }
            
            # Add volatility metrics if available
            if all('volatility' in market_data[symbol] for symbol in weights.keys()):
                risk_metrics['portfolio_volatility'] = self._calculate_portfolio_volatility(
                    weights, market_data
                )
            
            self.logger.info(f"Risk assessment complete: {risk_metrics}")
            return risk_metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating portfolio risk: {str(e)}")
            raise

    def _calculate_concentration_risk(self, weights: Dict[str, float]) -> Dict:
        """
        Calculate concentration risk metrics.
        
        Args:
            weights (Dict[str, float]): Position weights
            
        Returns:
            Dict: Concentration risk metrics
        """
        try:
            # Calculate Herfindahl-Hirschman Index (HHI)
            hhi = sum(weight ** 2 for weight in weights.values())
            
            # Calculate top holdings concentration
            sorted_weights = sorted(weights.values(), reverse=True)
            top_3_concentration = sum(sorted_weights[:3])
            
            return {
                'hhi': hhi,
                'top_3_concentration': top_3_concentration,
                'risk_level': self._get_concentration_risk_level(hhi)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating concentration risk: {str(e)}")
            raise

    def _calculate_portfolio_volatility(self, weights: Dict[str, float], market_data: Dict) -> float:
        """
        Calculate portfolio volatility using position weights and individual volatilities.
        
        Args:
            weights (Dict[str, float]): Position weights
            market_data (Dict): Market data with volatility information
            
        Returns:
            float: Portfolio volatility
        """
        try:
            # Calculate weighted average volatility
            weighted_vol = sum(
                weights[symbol] * market_data[symbol]['volatility']
                for symbol in weights.keys()
            )
            
            return weighted_vol
            
        except Exception as e:
            self.logger.error(f"Error calculating portfolio volatility: {str(e)}")
            raise

    def _get_concentration_risk_level(self, hhi: float) -> str:
        """
        Determine concentration risk level based on HHI.
        
        Args:
            hhi (float): Herfindahl-Hirschman Index
            
        Returns:
            str: Risk level description
        """
        if hhi > 0.25:
            return 'high'
        elif hhi > 0.15:
            return 'moderate'
        else:
            return 'low'

# Create the ADK tool
@FunctionTool
def assess_portfolio_risk_tool(portfolio: List[Dict], market_data: Dict) -> Dict:
    """ADK tool for portfolio risk assessment."""
    logger.info("Portfolio risk assessment tool called")
    agent = RiskAssessmentAgent()
    return agent.calculate_portfolio_risk(portfolio, market_data)

# Create the ADK agent
risk_agent = LlmAgent(
    name="risk_assessment_agent",
    description="Assesses portfolio risk and provides recommendations.",
    tools=[assess_portfolio_risk_tool],
)
