"""
Reporting Agent for generating portfolio analysis reports.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportingAgent:
    def __init__(self):
        """Initialize the ReportingAgent."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing ReportingAgent")

    async def generate_portfolio_report(
        self,
        portfolio: List[Dict],
        market_data: Dict,
        risk_assessment: Dict,
        sentiment_analysis: Dict
    ) -> Dict:
        """
        Generate a comprehensive portfolio report.
        
        Args:
            portfolio (List[Dict]): Portfolio positions
            market_data (Dict): Market data for portfolio symbols
            risk_assessment (Dict): Risk assessment results
            sentiment_analysis (Dict): Sentiment analysis results
            
        Returns:
            Dict: Comprehensive portfolio report
        """
        try:
            self.logger.info("Starting portfolio report generation")
            self.logger.debug(f"Input data - Portfolio: {portfolio}, Market: {market_data}, Risk: {risk_assessment}, Sentiment: {sentiment_analysis}")
            
            # Calculate portfolio performance
            performance = self._calculate_performance(portfolio, market_data)
            
            # Generate report sections
            self.logger.info("Formatting portfolio summary")
            portfolio_summary = self._generate_portfolio_summary(portfolio, market_data)
            
            self.logger.info("Formatting performance analysis")
            performance_analysis = performance
            
            self.logger.info("Formatting risk analysis")
            risk_analysis = self._format_risk_analysis(risk_assessment)
            
            self.logger.info("Formatting sentiment analysis")
            sentiment = self._format_sentiment_analysis(sentiment_analysis)
            
            self.logger.info("Generating recommendations")
            recommendations = self._generate_recommendations(
                portfolio_summary, risk_analysis, sentiment
            )
            
            # Combine all sections
            report = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_summary': portfolio_summary,
                'performance_analysis': performance_analysis,
                'risk_analysis': risk_analysis,
                'market_sentiment': sentiment,
                'recommendations': recommendations
            }
            
            self.logger.info("Portfolio report generation complete")
            self.logger.debug(f"Generated report: {report}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating portfolio report: {str(e)}", exc_info=True)
            raise

    def _calculate_performance(self, portfolio: List[Dict], market_data: Dict) -> Dict:
        """
        Calculate portfolio performance metrics.
        
        Args:
            portfolio (List[Dict]): Portfolio positions
            market_data (Dict): Market data for portfolio symbols
            
        Returns:
            Dict: Performance metrics
        """
        try:
            total_cost = sum(pos['quantity'] * pos['purchase_price'] for pos in portfolio)
            current_value = sum(
                pos['quantity'] * market_data[pos['symbol']]['current_price']
                for pos in portfolio
            )
            
            return {
                'total_cost': total_cost,
                'current_value': current_value,
                'total_return': current_value - total_cost,
                'return_percentage': ((current_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating performance: {str(e)}")
            raise

    def _generate_portfolio_summary(self, portfolio: List[Dict], market_data: Dict) -> Dict:
        """
        Generate portfolio summary.
        
        Args:
            portfolio (List[Dict]): Portfolio positions
            market_data (Dict): Market data for portfolio symbols
            
        Returns:
            Dict: Portfolio summary
        """
        try:
            positions = []
            for pos in portfolio:
                symbol = pos['symbol']
                current_price = market_data[symbol]['current_price']
                position_value = pos['quantity'] * current_price
                position_return = ((current_price - pos['purchase_price']) / pos['purchase_price']) * 100
                
                positions.append({
                    'symbol': symbol,
                    'quantity': pos['quantity'],
                    'purchase_price': pos['purchase_price'],
                    'current_price': current_price,
                    'position_value': position_value,
                    'return_percentage': position_return
                })
            
            return {
                'number_of_positions': len(portfolio),
                'positions': positions
            }
            
        except Exception as e:
            self.logger.error(f"Error generating portfolio summary: {str(e)}")
            raise

    def _format_risk_analysis(self, risk_assessment: Dict) -> Dict:
        """
        Format risk analysis results.
        
        Args:
            risk_assessment (Dict): Risk assessment results
            
        Returns:
            Dict: Formatted risk analysis
        """
        try:
            return {
                'risk_level': risk_assessment['concentration_risk']['risk_level'],
                'concentration_metrics': {
                    'hhi': risk_assessment['concentration_risk']['hhi'],
                    'top_3_concentration': risk_assessment['concentration_risk']['top_3_concentration']
                },
                'portfolio_volatility': risk_assessment.get('portfolio_volatility', 'N/A')
            }
            
        except Exception as e:
            self.logger.error(f"Error formatting risk analysis: {str(e)}")
            raise

    def _format_sentiment_analysis(self, sentiment_analysis: Dict) -> Dict:
        """
        Format sentiment analysis results.
        
        Args:
            sentiment_analysis (Dict): Sentiment analysis results
            
        Returns:
            Dict: Formatted sentiment analysis
        """
        try:
            self.logger.debug(f"Formatting sentiment analysis for data: {sentiment_analysis}")
            sentiment = sentiment_analysis.get('sentiment', sentiment_analysis)
            self.logger.debug(f"Extracted sentiment data: {sentiment}")
            
            formatted = {
                'overall_sentiment': sentiment['category'],
                'sentiment_strength': abs(sentiment['polarity']),
                'subjectivity': sentiment['subjectivity']
            }
            self.logger.debug(f"Formatted sentiment analysis: {formatted}")
            return formatted
            
        except Exception as e:
            self.logger.error(f"Error formatting sentiment analysis: {str(e)}", exc_info=True)
            raise

    def _generate_recommendations(
        self,
        portfolio_summary: Dict,
        risk_analysis: Dict,
        sentiment: Dict
    ) -> List[Dict]:
        """
        Generate investment recommendations.
        
        Args:
            portfolio_summary (Dict): Portfolio summary
            risk_analysis (Dict): Risk analysis
            sentiment (Dict): Market sentiment
            
        Returns:
            List[Dict]: List of recommendations
        """
        try:
            self.logger.info("Starting recommendation generation")
            self.logger.debug(f"Input data - Summary: {portfolio_summary}, Risk: {risk_analysis}, Sentiment: {sentiment}")
            
            recommendations = []
            
            # Add risk-based recommendations
            if risk_analysis['risk_level'] == 'high':
                self.logger.info("Adding risk-based recommendations for high concentration")
                recommendations.append({
                    'type': 'risk_management',
                    'priority': 'high',
                    'action': 'Consider diversifying portfolio to reduce concentration risk',
                    'details': 'Current portfolio shows high concentration in certain positions'
                })
            
            # Add sentiment-based recommendations
            if sentiment['overall_sentiment'] == 'negative':
                self.logger.info("Adding sentiment-based recommendations for negative sentiment")
                recommendations.append({
                    'type': 'market_timing',
                    'priority': 'medium',
                    'action': 'Consider defensive positions or hedging strategies',
                    'details': 'Market sentiment indicates cautious outlook'
                })
            
            self.logger.info(f"Generated {len(recommendations)} recommendations")
            self.logger.debug(f"Recommendations: {recommendations}")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
            raise

# Create the ADK tool
@FunctionTool
def generate_portfolio_report_tool(
    portfolio: List[Dict],
    market_data: Dict,
    risk_assessment: Dict,
    sentiment_analysis: Dict
) -> Dict:
    """ADK tool for generating portfolio reports."""
    logger.info("Portfolio report generation tool called")
    agent = ReportingAgent()
    return agent.generate_portfolio_report(
        portfolio, market_data, risk_assessment, sentiment_analysis
    )

# Create the ADK agent
reporting_agent = LlmAgent(
    name="reporting_agent",
    description="Generates comprehensive portfolio reports.",
    tools=[generate_portfolio_report_tool],
)
