"""
AI Insights Agent for natural language portfolio and market analysis.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import os
import requests
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIInsightsAgent:
    def __init__(self):
        """Initialize the AIInsightsAgent."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing AIInsightsAgent")
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

    async def generate_nlp_insight(self, user_question: str, portfolio_data: Dict = None, market_context: Dict = None) -> str:
        """
        Generate natural language insights based on user question and portfolio/market context.
        
        Args:
            user_question (str): User's natural language question
            portfolio_data (Dict): Current portfolio data
            market_context (Dict): Market context and sentiment data
            
        Returns:
            str: AI-generated insight response
        """
        try:
            self.logger.info(f"Generating NLP insight for question: {user_question[:100]}...")
            
            # Analyze the question type
            question_type = self._analyze_question_type(user_question.lower())
            
            # Generate response based on question type
            if question_type == "investment_recommendation":
                return await self._generate_investment_recommendation(user_question, portfolio_data, market_context)
            elif question_type == "stock_analysis":
                return await self._generate_stock_analysis(user_question, portfolio_data, market_context)
            elif question_type == "market_overview":
                return await self._generate_market_overview(user_question, market_context)
            elif question_type == "portfolio_optimization":
                return await self._generate_portfolio_optimization(user_question, portfolio_data, market_context)
            else:
                return await self._generate_general_insight(user_question, portfolio_data, market_context)
                
        except Exception as e:
            self.logger.error(f"Error generating NLP insight: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question. Please try rephrasing or ask a different question. Error: {str(e)}"

    def _analyze_question_type(self, question: str) -> str:
        """Analyze the type of question being asked."""
        if any(word in question for word in ['invest', 'buy', 'sell', 'recommend', 'should i']):
            return "investment_recommendation"
        elif any(word in question for word in ['tesla', 'apple', 'microsoft', 'stock', 'company']):
            return "stock_analysis"
        elif any(word in question for word in ['market', 'trend', 'outlook', 'forecast']):
            return "market_overview"
        elif any(word in question for word in ['portfolio', 'diversify', 'optimize', 'balance']):
            return "portfolio_optimization"
        else:
            return "general"

    async def _generate_investment_recommendation(self, question: str, portfolio_data: Dict, market_context: Dict) -> str:
        """Generate investment recommendations based on portfolio and market data."""
        try:
            if not portfolio_data:
                return "I'd be happy to provide investment recommendations! Please first analyze your portfolio so I can give you personalized advice based on your current holdings and risk profile."
            
            # Extract portfolio insights
            portfolio_summary = portfolio_data.get('portfolio_summary', {})
            risk_analysis = portfolio_data.get('risk_analysis', {})
            performance = portfolio_data.get('performance_analysis', {})
            
            # Generate recommendation based on portfolio characteristics
            risk_level = risk_analysis.get('risk_level', 'moderate')
            total_return = performance.get('return_percentage', 0)
            positions = portfolio_summary.get('positions', [])
            
            if risk_level == 'high' and total_return < 0:
                recommendation = "Given your high-risk portfolio and current negative returns, I recommend considering defensive positions or rebalancing to reduce concentration risk. Focus on quality companies with strong fundamentals."
            elif risk_level == 'conservative' and total_return > 10:
                recommendation = "Your conservative portfolio is performing well! Consider gradually adding growth-oriented positions while maintaining your risk-averse approach."
            elif len(positions) < 3:
                recommendation = "Your portfolio shows low diversification. Consider adding positions in different sectors to reduce risk and improve potential returns."
            else:
                recommendation = "Your portfolio appears well-balanced. Consider reviewing sector allocation and ensuring alignment with your investment goals."
            
            return f"Based on your portfolio analysis: {recommendation} Your current risk level is {risk_level} with a {total_return:.1f}% return. Always consult with a financial advisor for personalized investment advice."
            
        except Exception as e:
            self.logger.error(f"Error generating investment recommendation: {str(e)}")
            return "I'm unable to generate specific investment recommendations at this time. Please ensure your portfolio data is complete and try again."

    async def _generate_stock_analysis(self, question: str, portfolio_data: Dict, market_context: Dict) -> str:
        """Generate stock-specific analysis."""
        try:
            # Extract stock mentions from question
            stocks = self._extract_stock_mentions(question)
            
            if not stocks:
                return "I'd be happy to analyze specific stocks! Please mention the stock symbols you'd like me to analyze (e.g., 'Tell me about AAPL' or 'What's happening with Tesla?')."
            
            # Get market context for mentioned stocks
            stock_analysis = []
            for stock in stocks[:3]:  # Limit to 3 stocks
                if market_context and 'symbol_breakdown' in market_context:
                    stock_data = market_context['symbol_breakdown'].get(stock, {})
                    if stock_data:
                        sentiment = stock_data.get('sentiment', {})
                        trend = stock_data.get('trend', 'stable')
                        headlines = stock_data.get('headlines', [])
                        
                        analysis = f"{stock}: Current sentiment is {sentiment.get('category', 'neutral')} with a {trend} trend. "
                        if headlines:
                            analysis += f"Recent news: {headlines[0].get('headline', '')[:80]}..."
                        stock_analysis.append(analysis)
                    else:
                        stock_analysis.append(f"{stock}: Limited data available for analysis.")
                else:
                    stock_analysis.append(f"{stock}: Please analyze your portfolio first to get detailed stock insights.")
            
            return " ".join(stock_analysis)
            
        except Exception as e:
            self.logger.error(f"Error generating stock analysis: {str(e)}")
            return "I'm unable to provide stock analysis at this time. Please try again or ensure your portfolio data is available."

    async def _generate_market_overview(self, question: str, market_context: Dict) -> str:
        """Generate market overview and trends."""
        try:
            if not market_context:
                return "I'd be happy to provide market insights! Please first analyze your portfolio to get current market sentiment and trends."
            
            overall_sentiment = market_context.get('overall_sentiment', 'neutral')
            sentiment_strength = market_context.get('sentiment_strength', 0)
            news_summary = market_context.get('news_summary', '')
            
            sentiment_description = "positive" if overall_sentiment == 'positive' else "negative" if overall_sentiment == 'negative' else "neutral"
            
            overview = f"Current market sentiment is {sentiment_description} with a strength of {abs(sentiment_strength)*100:.1f}%. "
            
            if news_summary:
                overview += f"Market news: {news_summary}"
            else:
                overview += "Market conditions appear stable with mixed sentiment across different sectors."
            
            return overview
            
        except Exception as e:
            self.logger.error(f"Error generating market overview: {str(e)}")
            return "I'm unable to provide market overview at this time. Please try again."

    async def _generate_portfolio_optimization(self, question: str, portfolio_data: Dict, market_context: Dict) -> str:
        """Generate portfolio optimization advice."""
        try:
            if not portfolio_data:
                return "I'd be happy to help optimize your portfolio! Please first analyze your portfolio so I can provide specific recommendations based on your current holdings."
            
            risk_analysis = portfolio_data.get('risk_analysis', {})
            performance = portfolio_data.get('performance_analysis', {})
            portfolio_summary = portfolio_data.get('portfolio_summary', {})
            
            risk_level = risk_analysis.get('risk_level', 'moderate')
            concentration = risk_analysis.get('concentration_metrics', {})
            hhi = concentration.get('hhi', 0)
            positions = portfolio_summary.get('positions', [])
            
            optimization_advice = []
            
            if hhi > 0.5:
                optimization_advice.append("Your portfolio shows high concentration risk. Consider diversifying across more positions and sectors.")
            
            if len(positions) < 5:
                optimization_advice.append("Adding more positions could improve diversification and reduce risk.")
            
            if risk_level == 'high' and performance.get('return_percentage', 0) < 0:
                optimization_advice.append("Consider rebalancing to reduce risk given current negative performance.")
            
            if not optimization_advice:
                optimization_advice.append("Your portfolio appears well-optimized for your current risk profile.")
            
            return "Portfolio optimization insights: " + " ".join(optimization_advice)
            
        except Exception as e:
            self.logger.error(f"Error generating portfolio optimization: {str(e)}")
            return "I'm unable to provide portfolio optimization advice at this time. Please try again."

    async def _generate_general_insight(self, question: str, portfolio_data: Dict, market_context: Dict) -> str:
        """Generate general insights for other types of questions."""
        try:
            # Provide a general response based on available context
            if portfolio_data:
                return "I can help you with investment decisions, portfolio analysis, and market insights. Try asking specific questions about your portfolio performance, stock recommendations, or market trends."
            else:
                return "Welcome! I'm here to help with your investment questions. Please first analyze your portfolio, then ask me about specific stocks, market trends, or investment recommendations."
                
        except Exception as e:
            self.logger.error(f"Error generating general insight: {str(e)}")
            return "I'm here to help with your investment questions. Please try asking a specific question about your portfolio or the market."

    def _extract_stock_mentions(self, question: str) -> List[str]:
        """Extract stock symbols mentioned in the question."""
        # Common stock symbols and company names
        stock_mappings = {
            'tesla': 'TSLA',
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'amazon': 'AMZN',
            'nvidia': 'NVDA',
            'meta': 'META',
            'netflix': 'NFLX',
            'disney': 'DIS',
            'coca-cola': 'KO',
            'mcdonalds': 'MCD',
            'walmart': 'WMT',
            'johnson & johnson': 'JNJ',
            'procter & gamble': 'PG'
        }
        
        mentioned_stocks = []
        question_lower = question.lower()
        
        # Check for exact stock symbols (uppercase)
        import re
        symbols = re.findall(r'\b[A-Z]{2,5}\b', question)
        mentioned_stocks.extend(symbols)
        
        # Check for company names
        for company, symbol in stock_mappings.items():
            if company in question_lower:
                mentioned_stocks.append(symbol)
        
        return list(set(mentioned_stocks))  # Remove duplicates 