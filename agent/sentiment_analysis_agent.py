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
        self.newsdata_api_key = os.getenv('NEWSDATA_API_KEY', 'pub_56a8c8c7c7cf45adb0cbb64ebc746c66')  # Load NewsData.io key

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
            self.logger.info(f"Fetching news for {symbol} using NewsAPI")
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
            articles = news_data.get('articles', [])
            
            self.logger.info(f"Fetched {len(articles)} articles for {symbol}")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching news for {symbol}: {str(e)}")
            return []

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
                    'content': content,  # Add content field for recent events extraction
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
            portfolio_recent_events = []
            
            for symbol in symbols:
                try:
                    sentiment_data = await self.get_symbol_sentiment(symbol)
                    symbol_sentiments[symbol] = sentiment_data
                    
                    sentiment = sentiment_data['sentiment']
                    total_polarity += sentiment['polarity']
                    total_subjectivity += sentiment['subjectivity']
                    sentiment_counts[sentiment['category']] += 1
                    
                    # Collect headlines for news summary and recent events
                    if 'headlines' in sentiment_data and sentiment_data['headlines']:
                        all_headlines.extend(sentiment_data['headlines'][:5])  # Top 5 headlines per symbol
                        
                        # Extract recent events for this symbol
                        recent_events = await self.extract_recent_events(sentiment_data['headlines'], symbol)
                        if recent_events['recent_events']:
                            portfolio_recent_events.append(recent_events)
                    
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
                
                # Generate portfolio-level recent events summary
                portfolio_events_summary = self._generate_portfolio_events_summary(portfolio_recent_events)
                
                return {
                    'overall_sentiment': overall_category,
                    'sentiment_strength': avg_polarity,
                    'subjectivity': avg_subjectivity,
                    'symbol_breakdown': symbol_sentiments,
                    'sentiment_distribution': sentiment_counts,
                    'news_summary': news_summary,
                    'recent_events': {
                        'portfolio_events': portfolio_recent_events,
                        'portfolio_summary': portfolio_events_summary,
                        'total_events': sum(len(events['recent_events']) for events in portfolio_recent_events),
                        'high_impact_count': sum(events['high_impact_events'] for events in portfolio_recent_events)
                    },
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
                    'recent_events': {
                        'portfolio_events': [],
                        'portfolio_summary': "No recent events detected for portfolio stocks.",
                        'total_events': 0,
                        'high_impact_count': 0
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error getting portfolio sentiment summary: {str(e)}")
            raise

    def _get_sentiment_description(self, headlines: List[Dict]) -> str:
        """
        Get a description of the overall sentiment from headlines.
        
        Args:
            headlines (List[Dict]): List of headlines with sentiment data
            
        Returns:
            str: Sentiment description
        """
        if not headlines:
            return "mixed"
        
        positive_count = sum(1 for h in headlines if h.get('sentiment', {}).get('category') == 'positive')
        negative_count = sum(1 for h in headlines if h.get('sentiment', {}).get('category') == 'negative')
        neutral_count = sum(1 for h in headlines if h.get('sentiment', {}).get('category') == 'neutral')
        
        total = len(headlines)
        if total == 0:
            return "mixed"
        
        positive_ratio = positive_count / total
        negative_ratio = negative_count / total
        
        if positive_ratio > 0.5:
            return "positive"
        elif negative_ratio > 0.5:
            return "negative"
        else:
            return "mixed"

    def _generate_portfolio_events_summary(self, portfolio_events: List[Dict]) -> str:
        """
        Generate a summary of recent events across the entire portfolio.
        
        Args:
            portfolio_events (List[Dict]): List of recent events for each symbol
            
        Returns:
            str: Portfolio-level events summary
        """
        if not portfolio_events:
            return "No significant recent events detected across portfolio stocks."
        
        total_events = sum(len(events['recent_events']) for events in portfolio_events)
        high_impact_total = sum(events['high_impact_events'] for events in portfolio_events)
        
        # Get symbols with events
        symbols_with_events = [events['symbol'] for events in portfolio_events if events['recent_events']]
        
        if high_impact_total > 0:
            return f"Portfolio has {total_events} recent developments across {len(symbols_with_events)} stocks, including {high_impact_total} high-impact events. These developments could significantly influence portfolio performance."
        elif total_events > 0:
            return f"Portfolio has {total_events} recent developments across {len(symbols_with_events)} stocks that may impact market sentiment and stock performance."
        else:
            return "No significant recent events detected across portfolio stocks."

    async def generate_news_summary(self, headlines: List[Dict]) -> str:
        """
        Generate a summary of news headlines.
        
        Args:
            headlines (List[Dict]): List of news headlines with sentiment data
            
        Returns:
            str: Summary of news
        """
        try:
            if not headlines:
                return "No recent news available."
            
            # Get top headlines by sentiment strength
            top_headlines = sorted(headlines, key=lambda x: abs(x.get('sentiment', {}).get('polarity', 0)), reverse=True)[:3]
            
            summary_parts = []
            for headline in top_headlines:
                title = headline.get('headline', '')
                if title:
                    summary_parts.append(f"'{title}'")
            
            if summary_parts:
                return f"Recent market news shows {self._get_sentiment_description(headlines)} sentiment. Top stories include: {', '.join(summary_parts)}"
            else:
                return "Recent market news shows mixed sentiment with no major headlines."
                
        except Exception as e:
            self.logger.error(f"Error generating news summary: {str(e)}")
            return "Unable to generate news summary at this time."

    async def extract_recent_events(self, headlines: List[Dict], symbol: str) -> Dict:
        """
        Extract and analyze recent company-specific events from news headlines.
        
        Args:
            headlines (List[Dict]): List of news headlines with sentiment data
            symbol (str): Stock symbol for context
            
        Returns:
            Dict: Recent events analysis with structured event data
        """
        try:
            self.logger.info(f"Extracting recent events for {symbol}")
            
            # Event keywords that indicate significant developments
            event_keywords = [
                'announces', 'launches', 'unveils', 'releases', 'introduces', 'debuts',
                'partners', 'acquires', 'merges', 'buys', 'sells', 'divests',
                'settles', 'sues', 'lawsuit', 'legal', 'investigation', 'probe',
                'ceo', 'executive', 'resigns', 'appoints', 'hires', 'fires',
                'earnings', 'revenue', 'profit', 'loss', 'quarterly', 'annual',
                'dividend', 'stock split', 'buyback', 'ipo', 'secondary',
                'regulatory', 'fda', 'sec', 'approval', 'rejection', 'warning',
                'recall', 'safety', 'security', 'breach', 'hack', 'cyber',
                'expansion', 'opens', 'closes', 'restructuring', 'layoffs',
                'innovation', 'patent', 'technology', 'ai', 'machine learning'
            ]
            
            recent_events = []
            current_date = datetime.now()
            
            for headline in headlines:
                title = headline.get('headline', '').lower()
                content = headline.get('content', '').lower()
                published_at = headline.get('published_at', '')
                
                # Check if headline contains event keywords
                event_found = False
                event_type = None
                
                for keyword in event_keywords:
                    if keyword in title or keyword in content:
                        event_found = True
                        event_type = keyword
                        break
                
                if event_found:
                    # Parse publication date
                    try:
                        if published_at:
                            # Handle different date formats from NewsData.io
                            if published_at.endswith('Z'):
                                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                            else:
                                # Try parsing without timezone info
                                pub_date = datetime.fromisoformat(published_at)
                            
                            # Make both dates timezone-aware for comparison
                            if pub_date.tzinfo is None:
                                pub_date = pub_date.replace(tzinfo=datetime.now().astimezone().tzinfo)
                            
                            # Make current_date timezone-aware if it isn't already
                            if current_date.tzinfo is None:
                                current_date = current_date.replace(tzinfo=datetime.now().astimezone().tzinfo)
                            
                            days_old = (current_date - pub_date).days
                            
                            # Only include events from last 10 days
                            if days_old <= 10:
                                event = {
                                    'headline': headline.get('headline', ''),
                                    'event_type': event_type,
                                    'days_old': days_old,
                                    'sentiment': headline.get('sentiment', {}),
                                    'source': headline.get('source', ''),
                                    'published_at': published_at,
                                    'impact_level': self._assess_event_impact(title, content, event_type)
                                }
                                recent_events.append(event)
                    except Exception as e:
                        self.logger.warning(f"Error parsing date for event: {str(e)}")
                        # Try a simpler approach - just include the event without date filtering
                        event = {
                            'headline': headline.get('headline', ''),
                            'event_type': event_type,
                            'days_old': 0,  # Unknown
                            'sentiment': headline.get('sentiment', {}),
                            'source': headline.get('source', ''),
                            'published_at': published_at,
                            'impact_level': self._assess_event_impact(title, content, event_type)
                        }
                        recent_events.append(event)
                        continue
            
            # Sort by impact level and recency
            recent_events.sort(key=lambda x: (x['impact_level'], -x.get('days_old', 0)))
            
            # Generate summary analysis
            event_summary = self._generate_event_summary(recent_events, symbol)
            
            return {
                'symbol': symbol,
                'recent_events': recent_events[:5],  # Top 5 most impactful events
                'event_summary': event_summary,
                'total_events': len(recent_events),
                'high_impact_events': len([e for e in recent_events if e['impact_level'] == 'high']),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting recent events for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'recent_events': [],
                'event_summary': f"Unable to extract recent events for {symbol} at this time.",
                'total_events': 0,
                'high_impact_events': 0,
                'timestamp': datetime.now().isoformat()
            }

    def _assess_event_impact(self, title: str, content: str, event_type: str) -> str:
        """
        Assess the potential impact level of an event.
        
        Args:
            title (str): News headline
            content (str): News content
            event_type (str): Type of event detected
            
        Returns:
            str: Impact level (high, medium, low)
        """
        # High impact keywords
        high_impact = [
            'ceo', 'executive', 'resigns', 'appoints', 'merges', 'acquires',
            'lawsuit', 'legal', 'investigation', 'sec', 'fda', 'recall',
            'earnings', 'revenue', 'profit', 'loss', 'dividend', 'stock split',
            'ipo', 'breach', 'hack', 'cyber', 'layoffs', 'restructuring'
        ]
        
        # Medium impact keywords
        medium_impact = [
            'announces', 'launches', 'unveils', 'releases', 'partners',
            'expansion', 'innovation', 'patent', 'technology', 'ai'
        ]
        
        if event_type in high_impact:
            return 'high'
        elif event_type in medium_impact:
            return 'medium'
        else:
            return 'low'

    def _generate_event_summary(self, events: List[Dict], symbol: str) -> str:
        """
        Generate a summary of recent events for a symbol.
        
        Args:
            events (List[Dict]): List of recent events
            symbol (str): Stock symbol
            
        Returns:
            str: Summary of recent events
        """
        if not events:
            return f"No significant recent events detected for {symbol}."
        
        high_impact = [e for e in events if e['impact_level'] == 'high']
        medium_impact = [e for e in events if e['impact_level'] == 'medium']
        
        summary_parts = []
        
        if high_impact:
            summary_parts.append(f"{len(high_impact)} high-impact development{'s' if len(high_impact) > 1 else ''}")
        
        if medium_impact:
            summary_parts.append(f"{len(medium_impact)} notable announcement{'s' if len(medium_impact) > 1 else ''}")
        
        if summary_parts:
            event_types = list(set([e['event_type'] for e in events[:3]]))
            event_description = ', '.join(event_types[:2])
            
            return f"{symbol} has {', '.join(summary_parts)} in the past 10 days, including {event_description}. These developments could influence short-term sentiment and stock performance."
        else:
            return f"{symbol} has {len(events)} recent developments that may impact market sentiment."

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

