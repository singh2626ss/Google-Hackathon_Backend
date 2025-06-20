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
            
            # Calculate volatility metrics for each position
            from .market_data_agent import MarketDataAgent
            market_agent = MarketDataAgent()
            
            volatility_data = {}
            portfolio_volatility = 0
            
            for pos in portfolio:
                symbol = pos['symbol']
                try:
                    vol_data = await market_agent.calculate_volatility(symbol, days=30)
                    volatility_data[symbol] = vol_data
                    
                    # Calculate weighted portfolio volatility
                    if vol_data.get('annualized_volatility', 0) > 0:
                        portfolio_volatility += weights[symbol] * vol_data['annualized_volatility']
                        
                except Exception as e:
                    self.logger.warning(f"Could not calculate volatility for {symbol}: {str(e)}")
                    volatility_data[symbol] = {'annualized_volatility': 0, 'error': str(e)}
            
            risk_metrics['volatility_data'] = volatility_data
            risk_metrics['portfolio_volatility'] = portfolio_volatility
            
            # Calculate diversification score
            risk_metrics['diversification_score'] = self._calculate_diversification_score(weights, len(portfolio))
            
            # Add risk level based on multiple factors
            risk_metrics['overall_risk_level'] = self._calculate_overall_risk_level(
                risk_metrics['concentration_risk']['hhi'],
                portfolio_volatility,
                len(portfolio)
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

    def _calculate_diversification_score(self, weights: Dict[str, float], num_positions: int) -> float:
        """
        Calculate diversification score (0-100, higher is better).
        
        Args:
            weights (Dict[str, float]): Position weights
            num_positions (int): Number of positions
            
        Returns:
            float: Diversification score
        """
        try:
            # Base score from number of positions
            position_score = min(num_positions * 10, 50)  # Max 50 points for positions
            
            # Weight distribution score
            if len(weights) > 1:
                # Calculate how evenly distributed the weights are
                max_weight = max(weights.values())
                weight_score = (1 - max_weight) * 50  # Max 50 points for even distribution
            else:
                weight_score = 0
            
            total_score = position_score + weight_score
            return min(total_score, 100)
            
        except Exception as e:
            self.logger.error(f"Error calculating diversification score: {str(e)}")
            return 0

    def _calculate_overall_risk_level(self, hhi: float, portfolio_volatility: float, num_positions: int) -> str:
        """
        Calculate overall risk level based on multiple factors.
        
        Args:
            hhi (float): Herfindahl-Hirschman Index
            portfolio_volatility (float): Portfolio volatility
            num_positions (int): Number of positions
            
        Returns:
            str: Risk level description
        """
        try:
            risk_score = 0
            
            # Concentration risk (0-40 points)
            if hhi > 0.25:
                risk_score += 40
            elif hhi > 0.15:
                risk_score += 25
            elif hhi > 0.10:
                risk_score += 15
            else:
                risk_score += 5
            
            # Volatility risk (0-30 points)
            if portfolio_volatility > 0.30:
                risk_score += 30
            elif portfolio_volatility > 0.20:
                risk_score += 20
            elif portfolio_volatility > 0.15:
                risk_score += 15
            else:
                risk_score += 5
            
            # Diversification risk (0-30 points)
            if num_positions < 3:
                risk_score += 30
            elif num_positions < 5:
                risk_score += 20
            elif num_positions < 10:
                risk_score += 10
            else:
                risk_score += 5
            
            # Determine risk level
            if risk_score >= 70:
                return 'very_high'
            elif risk_score >= 50:
                return 'high'
            elif risk_score >= 30:
                return 'moderate'
            else:
                return 'low'
                
        except Exception as e:
            self.logger.error(f"Error calculating overall risk level: {str(e)}")
            return 'moderate'

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

