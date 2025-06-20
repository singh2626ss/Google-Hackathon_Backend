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
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalysisAgent:
    def __init__(self):
        """Initialize the SentimentAnalysisAgent."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing SentimentAnalysisAgent")
        self.sentiment_history = {}  # Store sentiment history for trend analysis
        self.news_api_key = os.getenv('NEWS_API_KEY')  # Load NewsAPI key from environment variables

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
            # Add overall sentiment category based on average polarity
            if aggregate['average_polarity'] > 0.1:
                aggregate['category'] = 'positive'
            elif aggregate['average_polarity'] < -0.1:
                aggregate['category'] = 'negative'
            else:
                aggregate['category'] = 'neutral'
            # Add keys for compatibility with reporting agent
            aggregate['polarity'] = aggregate['average_polarity']
            aggregate['subjectivity'] = aggregate['average_subjectivity']
            
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
            
            # Fetch real-time news for the symbol
            news_items = await self.fetch_news(symbol)
            sentiment = await self.analyze_news_sentiment(news_items)
            
            # Store sentiment in history for trend analysis
            if symbol not in self.sentiment_history:
                self.sentiment_history[symbol] = []
            self.sentiment_history[symbol].append(sentiment)
            
            return {
                'symbol': symbol,
                'sentiment': sentiment,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting market sentiment for {symbol}: {str(e)}")
            raise

    async def fetch_news(self, symbol: str) -> List[Dict]:
        """
        Fetch real-time news for a specific symbol using NewsAPI.
        
        Args:
            symbol (str): Stock symbol to fetch news for
            
        Returns:
            List[Dict]: List of news items
        """
        try:
            self.logger.info(f"Fetching news for {symbol}")
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': symbol,
                'apiKey': self.news_api_key,
                'language': 'en',
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            news_data = response.json()
            return news_data.get('articles', [])
            
        except Exception as e:
            self.logger.error(f"Error fetching news for {symbol}: {str(e)}")
            raise

    async def get_sentiment_trend(self, symbol: str) -> Dict:
        """
        Get sentiment trend over time for a specific symbol.
        
        Args:
            symbol (str): Stock symbol to analyze
            
        Returns:
            Dict: Sentiment trend analysis results
        """
        try:
            self.logger.info(f"Getting sentiment trend for {symbol}")
            
            if symbol not in self.sentiment_history:
                return {'error': 'No sentiment history available for this symbol'}
            
            sentiments = self.sentiment_history[symbol]
            trend = {
                'symbol': symbol,
                'trend': sentiments,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Sentiment trend analysis complete: {trend}")
            return trend
            
        except Exception as e:
            self.logger.error(f"Error getting sentiment trend for {symbol}: {str(e)}")
            raise

    async def get_symbol_sentiment(self, symbol: str) -> Dict:
        """
        Get detailed sentiment analysis for a specific symbol with headlines.
        
        Args:
            symbol (str): Stock symbol to analyze
            
        Returns:
            Dict: Detailed sentiment analysis with headlines
        """
        try:
            self.logger.info(f"Getting detailed sentiment for {symbol}")
            
            # Fetch news for the symbol
            news_items = await self.fetch_news(symbol)
            
            if not news_items:
                return {
                    'symbol': symbol,
                    'sentiment': {
                        'category': 'neutral',
                        'polarity': 0.0,
                        'subjectivity': 0.0,
                        'confidence': 0.0
                    },
                    'headlines': [],
                    'trend': 'stable',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Analyze sentiment for each headline
            headline_sentiments = []
            for item in news_items[:10]:  # Limit to 10 most recent articles
                headline = item.get('title', '')
                content = item.get('description', '')
                text = f"{headline} {content}"
                
                sentiment = await self.analyze_sentiment(text)
                headline_sentiments.append({
                    'headline': headline,
                    'sentiment': sentiment,
                    'published_at': item.get('publishedAt', ''),
                    'source': item.get('source', {}).get('name', '')
                })
            
            # Calculate aggregate sentiment
            if headline_sentiments:
                polarities = [h['sentiment']['polarity'] for h in headline_sentiments]
                subjectivities = [h['sentiment']['subjectivity'] for h in headline_sentiments]
                
                aggregate_sentiment = {
                    'category': 'neutral',
                    'polarity': sum(polarities) / len(polarities),
                    'subjectivity': sum(subjectivities) / len(subjectivities),
                    'confidence': abs(sum(polarities) / len(polarities)),
                    'article_count': len(headline_sentiments)
                }
                
                # Determine category
                if aggregate_sentiment['polarity'] > 0.1:
                    aggregate_sentiment['category'] = 'positive'
                elif aggregate_sentiment['polarity'] < -0.1:
                    aggregate_sentiment['category'] = 'negative'
                
                # Determine trend based on recent vs older articles
                if len(headline_sentiments) >= 2:
                    recent_polarities = [h['sentiment']['polarity'] for h in headline_sentiments[:5]]
                    older_polarities = [h['sentiment']['polarity'] for h in headline_sentiments[5:]]
                    
                    if recent_polarities and older_polarities:
                        recent_avg = sum(recent_polarities) / len(recent_polarities)
                        older_avg = sum(older_polarities) / len(older_polarities)
                        
                        if recent_avg > older_avg + 0.1:
                            trend = 'improving'
                        elif recent_avg < older_avg - 0.1:
                            trend = 'declining'
                        else:
                            trend = 'stable'
                    else:
                        trend = 'stable'
                else:
                    trend = 'stable'
                
                return {
                    'symbol': symbol,
                    'sentiment': aggregate_sentiment,
                    'headlines': headline_sentiments,
                    'trend': trend,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'symbol': symbol,
                    'sentiment': {
                        'category': 'neutral',
                        'polarity': 0.0,
                        'subjectivity': 0.0,
                        'confidence': 0.0
                    },
                    'headlines': [],
                    'trend': 'stable',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error getting symbol sentiment for {symbol}: {str(e)}")
            raise

    async def get_portfolio_sentiment_summary(self, symbols: List[str]) -> Dict:
        """
        Get sentiment summary for multiple symbols in a portfolio.
        
        Args:
            symbols (List[str]): List of stock symbols
            
        Returns:
            Dict: Portfolio sentiment summary
        """
        try:
            self.logger.info(f"Getting portfolio sentiment summary for {len(symbols)} symbols")
            
            symbol_sentiments = {}
            total_polarity = 0
            total_subjectivity = 0
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            all_headlines = []
            
            for symbol in symbols:
                try:
                    sentiment_data = await self.get_symbol_sentiment(symbol)
                    symbol_sentiments[symbol] = sentiment_data
                    
                    sentiment = sentiment_data['sentiment']
                    total_polarity += sentiment['polarity']
                    total_subjectivity += sentiment['subjectivity']
                    sentiment_counts[sentiment['category']] += 1
                    
                    # Collect headlines for news summary
                    if 'headlines' in sentiment_data and sentiment_data['headlines']:
                        all_headlines.extend(sentiment_data['headlines'][:5])  # Top 5 headlines per symbol
                    
                except Exception as e:
                    self.logger.warning(f"Could not get sentiment for {symbol}: {str(e)}")
                    symbol_sentiments[symbol] = {
                        'symbol': symbol,
                        'sentiment': {'category': 'neutral', 'polarity': 0, 'subjectivity': 0},
                        'error': str(e)
                    }
            
            # Calculate portfolio-level sentiment
            if symbol_sentiments:
                avg_polarity = total_polarity / len(symbol_sentiments)
                avg_subjectivity = total_subjectivity / len(symbol_sentiments)
                
                # Determine overall portfolio sentiment
                if avg_polarity > 0.1:
                    overall_category = 'positive'
                elif avg_polarity < -0.1:
                    overall_category = 'negative'
                else:
                    overall_category = 'neutral'
                
                # Generate news summary from top headlines
                news_summary = await self.generate_news_summary(all_headlines)
                
                return {
                    'overall_sentiment': overall_category,
                    'sentiment_strength': avg_polarity,
                    'subjectivity': avg_subjectivity,
                    'symbol_breakdown': symbol_sentiments,
                    'sentiment_distribution': sentiment_counts,
                    'news_summary': news_summary,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'overall_sentiment': 'neutral',
                    'sentiment_strength': 0.0,
                    'subjectivity': 0.0,
                    'symbol_breakdown': {},
                    'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                    'news_summary': "No recent news available for portfolio analysis.",
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error getting portfolio sentiment summary: {str(e)}")
            raise

    async def generate_news_summary(self, headlines: List[Dict]) -> str:
        """
        Generate a concise news summary from the top headlines.
        
        Args:
            headlines (List[Dict]): List of headline dictionaries
            
        Returns:
            str: Concise news summary
        """
        try:
            if not headlines:
                return "No recent news available for portfolio analysis."
            
            # Take top 5 headlines and extract titles
            top_headlines = headlines[:5]
            headline_titles = [h.get('headline', '') for h in top_headlines if h.get('headline')]
            
            if not headline_titles:
                return "No recent news available for portfolio analysis."
            
            # Create a simple summary based on sentiment and key themes
            positive_count = sum(1 for h in top_headlines if h.get('sentiment', {}).get('category') == 'positive')
            negative_count = sum(1 for h in top_headlines if h.get('sentiment', {}).get('category') == 'negative')
            
            # Extract common themes (simplified approach)
            themes = []
            for title in headline_titles:
                title_lower = title.lower()
                if 'earnings' in title_lower or 'quarterly' in title_lower:
                    themes.append('earnings')
                elif 'ai' in title_lower or 'artificial intelligence' in title_lower:
                    themes.append('AI')
                elif 'dividend' in title_lower:
                    themes.append('dividends')
                elif 'layoff' in title_lower or 'job' in title_lower:
                    themes.append('employment')
                elif 'merger' in title_lower or 'acquisition' in title_lower:
                    themes.append('M&A')
            
            # Generate summary
            if positive_count > negative_count:
                sentiment_tone = "positive"
            elif negative_count > positive_count:
                sentiment_tone = "negative"
            else:
                sentiment_tone = "mixed"
            
            theme_summary = ""
            if themes:
                unique_themes = list(set(themes))
                if len(unique_themes) == 1:
                    theme_summary = f" focusing on {unique_themes[0]} developments"
                elif len(unique_themes) > 1:
                    theme_summary = f" covering {', '.join(unique_themes[:-1])} and {unique_themes[-1]}"
            
            # Create a more comprehensive summary
            if len(headline_titles) >= 2:
                summary = f"Recent market news shows {sentiment_tone} sentiment{theme_summary}. Top stories include: '{headline_titles[0][:60]}...' and '{headline_titles[1][:60]}...'"
            else:
                summary = f"Recent market news shows {sentiment_tone} sentiment{theme_summary}. Key headline: '{headline_titles[0][:80]}...'"
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating news summary: {str(e)}")
            return "Unable to generate news summary at this time."

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

