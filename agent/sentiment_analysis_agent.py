"""
Sentiment Analysis Agent for analyzing market sentiment using TextBlob.
"""

import logging
from typing import Dict, List, Optional
from textblob import TextBlob
import requests
from datetime import datetime, timedelta
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalysisAgent:
    def __init__(self):
        """Initialize the SentimentAnalysisAgent."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing SentimentAnalysisAgent")

    async def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of given text using TextBlob.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Sentiment analysis results including polarity and subjectivity
        """
        try:
            self.logger.info(f"Analyzing sentiment for text: {text[:100]}...")
            blob = TextBlob(text)
            
            # Get overall sentiment
            sentiment = {
                'polarity': blob.sentiment.polarity,  # Range: -1.0 to 1.0
                'subjectivity': blob.sentiment.subjectivity,  # Range: 0.0 to 1.0
                'confidence': abs(blob.sentiment.polarity),  # Confidence based on polarity strength
                'timestamp': datetime.now().isoformat()
            }
            
            # Add sentiment category
            if sentiment['polarity'] > 0.1:
                sentiment['category'] = 'positive'
            elif sentiment['polarity'] < -0.1:
                sentiment['category'] = 'negative'
            else:
                sentiment['category'] = 'neutral'
            
            self.logger.info(f"Sentiment analysis complete: {sentiment['category']}")
            return sentiment
            
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            raise

    async def analyze_news_sentiment(self, news_items: List[Dict]) -> Dict:
        """
        Analyze sentiment across multiple news items.
        
        Args:
            news_items (List[Dict]): List of news items with 'title' and 'content'
            
        Returns:
            Dict: Aggregated sentiment analysis results
        """
        try:
            self.logger.info(f"Analyzing sentiment for {len(news_items)} news items")
            
            sentiments = []
            for item in news_items:
                # Combine title and content for analysis
                text = f"{item.get('title', '')} {item.get('content', '')}"
                sentiment = await self.analyze_sentiment(text)
                sentiments.append(sentiment)
            
            # Calculate aggregate metrics
            aggregate = {
                'average_polarity': sum(s['polarity'] for s in sentiments) / len(sentiments),
                'average_subjectivity': sum(s['subjectivity'] for s in sentiments) / len(sentiments),
                'sentiment_distribution': {
                    'positive': len([s for s in sentiments if s['category'] == 'positive']),
                    'negative': len([s for s in sentiments if s['category'] == 'negative']),
                    'neutral': len([s for s in sentiments if s['category'] == 'neutral'])
                },
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Aggregate sentiment analysis complete: {aggregate}")
            return aggregate
            
        except Exception as e:
            self.logger.error(f"Error in news sentiment analysis: {str(e)}")
            raise

    async def get_market_sentiment(self, symbol: str) -> Dict:
        """
        Get market sentiment for a specific symbol.
        
        Args:
            symbol (str): Stock symbol to analyze
            
        Returns:
            Dict: Market sentiment analysis results
        """
        try:
            self.logger.info(f"Getting market sentiment for {symbol}")
            
            # TODO: Implement actual news fetching from a news API
            # For now, return a placeholder sentiment
            sentiment = await self.analyze_sentiment(
                f"Market analysis for {symbol}: Current market conditions show moderate volatility."
            )
            
            return {
                'symbol': symbol,
                'sentiment': sentiment,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting market sentiment for {symbol}: {str(e)}")
            raise

# Create the ADK tool
@FunctionTool
def analyze_sentiment_tool(text: str) -> Dict:
    """ADK tool for sentiment analysis."""
    logger.info("Sentiment analysis tool called")
    agent = SentimentAnalysisAgent()
    return agent.analyze_sentiment(text)

# Create the ADK agent
sentiment_agent = LlmAgent(
    name="sentiment_analysis_agent",
    description="Analyzes sentiment of financial news and social media content using TextBlob.",
    tools=[analyze_sentiment_tool],
)
