"""
Reporting Agent for generating portfolio analysis reports.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
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
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

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

            # Generate visualization data
            visualization_data = await self._generate_visualization_data(
                portfolio, market_data, performance, sentiment
            )
            
            # Combine all sections
            report = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_summary': portfolio_summary,
                'performance_analysis': performance_analysis,
                'risk_analysis': risk_analysis,
                'market_sentiment': sentiment,
                'recommendations': recommendations,
                'visualization_data': visualization_data
            }

            # Save report for historical comparison
            self._save_report(report)
            
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
            
            # Handle new portfolio sentiment structure
            if 'portfolio_sentiment' in sentiment_analysis:
                portfolio_sentiment = sentiment_analysis['portfolio_sentiment']
                formatted = {
                    'overall_sentiment': portfolio_sentiment.get('category', 'neutral'),
                    'sentiment_strength': abs(portfolio_sentiment.get('polarity', 0.0)),
                    'subjectivity': portfolio_sentiment.get('subjectivity', 0.0),
                    'symbol_breakdown': sentiment_analysis.get('symbol_breakdown', {}),
                    'sentiment_distribution': sentiment_analysis.get('sentiment_distribution', {}),
                    'trend_analysis': self._analyze_sentiment_trends(sentiment_analysis.get('symbol_breakdown', {}))
                }
            else:
                # Handle new sentiment structure with news_summary and recent_events
                formatted = {
                    'overall_sentiment': sentiment_analysis.get('overall_sentiment', 'neutral'),
                    'sentiment_strength': abs(sentiment_analysis.get('sentiment_strength', 0.0)),
                    'subjectivity': sentiment_analysis.get('subjectivity', 0.0),
                    'symbol_breakdown': sentiment_analysis.get('symbol_breakdown', {}),
                    'sentiment_distribution': sentiment_analysis.get('sentiment_distribution', {}),
                    'news_summary': sentiment_analysis.get('news_summary', 'No recent news available for portfolio analysis.'),
                    'trend_analysis': self._analyze_sentiment_trends(sentiment_analysis.get('symbol_breakdown', {})),
                    'recent_events': sentiment_analysis.get('recent_events', {})
                }
            
            self.logger.debug(f"Formatted sentiment analysis: {formatted}")
            return formatted
        except Exception as e:
            self.logger.error(f"Error formatting sentiment analysis: {str(e)}", exc_info=True)
            raise

    def _analyze_sentiment_trends(self, symbol_breakdown: Dict) -> Dict:
        """
        Analyze sentiment trends across symbols.
        
        Args:
            symbol_breakdown (Dict): Symbol-specific sentiment data
            
        Returns:
            Dict: Trend analysis results
        """
        try:
            trends = {
                'improving': [],
                'declining': [],
                'stable': []
            }
            
            for symbol, data in symbol_breakdown.items():
                if 'trend' in data:
                    trend = data['trend']
                    if trend in trends:
                        trends[trend].append(symbol)
            
            return {
                'trends': trends,
                'summary': {
                    'improving_count': len(trends['improving']),
                    'declining_count': len(trends['declining']),
                    'stable_count': len(trends['stable'])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment trends: {str(e)}")
            return {'trends': {}, 'summary': {}}

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

    async def _generate_visualization_data(self, portfolio: List[Dict], market_data: Dict, performance: Dict, sentiment: Dict) -> Dict:
        """
        Generate data structures for frontend visualizations.
        
        Args:
            portfolio (List[Dict]): Portfolio positions
            market_data (Dict): Market data
            performance (Dict): Performance metrics
            sentiment (Dict): Sentiment analysis
            
        Returns:
            Dict: Visualization data structures
        """
        try:
            # Portfolio composition pie chart
            composition_data = {
                'type': 'pie',
                'labels': [pos['symbol'] for pos in portfolio],
                'values': [pos['quantity'] * market_data[pos['symbol']]['current_price'] for pos in portfolio],
                'title': 'Portfolio Composition'
            }

            # Enhanced performance trend with historical data
            from .market_data_agent import MarketDataAgent
            market_agent = MarketDataAgent()
            
            # Get historical data for performance trend
            performance_trend_data = []
            for pos in portfolio:
                try:
                    historical_data = await market_agent.get_historical_data(pos['symbol'], days=30)
                    if historical_data.get('timestamps') and historical_data.get('close_prices'):
                        # Calculate position value over time
                        for i, (timestamp, price) in enumerate(zip(historical_data['timestamps'], historical_data['close_prices'])):
                            position_value = pos['quantity'] * price
                            performance_trend_data.append({
                                'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                                'value': position_value,
                                'symbol': pos['symbol']
                            })
                except Exception as e:
                    self.logger.warning(f"Could not get historical data for {pos['symbol']}: {str(e)}")
            
            # Aggregate daily portfolio values
            if performance_trend_data:
                from collections import defaultdict
                daily_values = defaultdict(float)
                for data_point in performance_trend_data:
                    daily_values[data_point['date']] += data_point['value']
                
                performance_data = {
                    'type': 'line',
                    'x': list(daily_values.keys()),
                    'y': list(daily_values.values()),
                    'title': 'Portfolio Performance Trend (30 Days)'
                }
            else:
                # Fallback to single point
                performance_data = {
                    'type': 'line',
                    'x': [datetime.now().strftime('%Y-%m-%d')],
                    'y': [performance['current_value']],
                    'title': 'Portfolio Performance Trend'
                }

            # Enhanced sentiment gauge chart
            sentiment_data = {
                'type': 'gauge',
                'value': sentiment['sentiment_strength'],
                'title': 'Market Sentiment',
                'min': 0,
                'max': 1,
                'thresholds': {
                    'low': 0.3,
                    'medium': 0.6,
                    'high': 1.0
                }
            }

            # Enhanced risk metrics bar chart with real data
            risk_metrics = []
            risk_labels = []
            
            # Get volatility data for each position
            for pos in portfolio:
                symbol = pos['symbol']
                try:
                    vol_data = await market_agent.calculate_volatility(symbol, days=30)
                    if vol_data.get('annualized_volatility', 0) > 0:
                        risk_metrics.append(vol_data['annualized_volatility'])
                        risk_labels.append(f"{symbol} Vol")
                except Exception as e:
                    self.logger.warning(f"Could not calculate volatility for {symbol}: {str(e)}")
            
            # Add portfolio-level metrics
            if 'portfolio_volatility' in market_data:
                risk_metrics.append(market_data['portfolio_volatility'])
                risk_labels.append('Portfolio Vol')
            
            if not risk_metrics:
                risk_metrics = [0, 0, 0]
                risk_labels = ['HHI', 'Top 3 Concentration', 'Volatility']
            
            risk_data = {
                'type': 'bar',
                'labels': risk_labels,
                'values': risk_metrics,
                'title': 'Risk Metrics'
            }

            # Add goal-based forecasting data
            forecasting_data = self._generate_forecasting_data(performance, portfolio)

            return {
                'composition': composition_data,
                'performance': performance_data,
                'sentiment': sentiment_data,
                'risk': risk_data,
                'forecasting': forecasting_data
            }

        except Exception as e:
            self.logger.error(f"Error generating visualization data: {str(e)}")
            raise

    def _generate_forecasting_data(self, performance: Dict, portfolio: List[Dict]) -> Dict:
        """
        Generate goal-based forecasting data.
        
        Args:
            performance (Dict): Current performance metrics
            portfolio (List[Dict]): Portfolio positions
            
        Returns:
            Dict: Forecasting data
        """
        try:
            current_value = performance['current_value']
            total_cost = performance['total_cost']
            
            # Simple compound growth projections
            projections = {
                'conservative': 0.05,  # 5% annual return
                'moderate': 0.08,      # 8% annual return
                'aggressive': 0.12     # 12% annual return
            }
            
            forecast_data = {}
            for risk_level, annual_return in projections.items():
                # Project 1, 3, 5, 10 years
                years = [1, 3, 5, 10]
                projected_values = []
                
                for year in years:
                    projected_value = current_value * ((1 + annual_return) ** year)
                    projected_values.append({
                        'year': year,
                        'value': projected_value,
                        'growth': ((projected_value - current_value) / current_value) * 100
                    })
                
                forecast_data[risk_level] = {
                    'annual_return': annual_return * 100,
                    'projections': projected_values
                }
            
            return {
                'type': 'forecast',
                'current_value': current_value,
                'scenarios': forecast_data,
                'title': 'Portfolio Growth Projections'
            }
            
        except Exception as e:
            self.logger.error(f"Error generating forecasting data: {str(e)}")
            return {
                'type': 'forecast',
                'error': str(e)
            }

    def _save_report(self, report: Dict) -> None:
        """
        Save report for historical comparison.
        
        Args:
            report (Dict): Generated report
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.reports_dir / f"report_{timestamp}.json"
            
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"Saved report to {report_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
            raise

    async def export_report(self, report: Dict, format: str = 'json') -> bytes:
        """
        Export report in specified format.
        
        Args:
            report (Dict): Report to export
            format (str): Export format ('json', 'csv', 'pdf')
            
        Returns:
            bytes: Exported report data
        """
        try:
            if format == 'json':
                return json.dumps(report, indent=2).encode()
            
            elif format == 'csv':
                # Convert relevant sections to DataFrame
                df = pd.DataFrame(report['portfolio_summary']['positions'])
                return df.to_csv(index=False).encode()
            
            elif format == 'pdf':
                # Generate PDF using plotly
                fig = go.Figure()
                
                # Add portfolio composition pie chart
                fig.add_trace(go.Pie(
                    labels=report['visualization_data']['composition']['labels'],
                    values=report['visualization_data']['composition']['values'],
                    name="Portfolio Composition"
                ))
                
                # Add performance line chart
                fig.add_trace(go.Scatter(
                    x=report['visualization_data']['performance']['x'],
                    y=report['visualization_data']['performance']['y'],
                    name="Performance"
                ))
                
                # Save as PDF
                pdf_path = self.reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                fig.write_image(str(pdf_path))
                
                with open(pdf_path, 'rb') as f:
                    return f.read()
            
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
        except Exception as e:
            self.logger.error(f"Error exporting report: {str(e)}")
            raise

    async def get_historical_comparison(self, current_report: Dict, lookback_days: int = 30) -> Dict:
        """
        Compare current report with historical reports.
        
        Args:
            current_report (Dict): Current report
            lookback_days (int): Number of days to look back
            
        Returns:
            Dict: Comparison data
        """
        try:
            # Get historical reports
            historical_reports = []
            cutoff_date = datetime.now() - timedelta(days=lookback_days)
            
            for report_file in self.reports_dir.glob("report_*.json"):
                try:
                    with open(report_file, 'r') as f:
                        report = json.load(f)
                        report_date = datetime.fromisoformat(report['timestamp'])
                        if report_date >= cutoff_date:
                            historical_reports.append(report)
                except Exception as e:
                    self.logger.warning(f"Error reading report {report_file}: {str(e)}")
            
            # Generate comparison metrics
            comparison = {
                'performance_trend': {
                    'dates': [r['timestamp'] for r in historical_reports],
                    'values': [r['performance_analysis']['return_percentage'] for r in historical_reports]
                },
                'risk_trend': {
                    'dates': [r['timestamp'] for r in historical_reports],
                    'values': [r['risk_analysis']['portfolio_volatility'] for r in historical_reports]
                },
                'sentiment_trend': {
                    'dates': [r['timestamp'] for r in historical_reports],
                    'values': [r['market_sentiment']['sentiment_strength'] for r in historical_reports]
                }
            }
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error generating historical comparison: {str(e)}")
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

