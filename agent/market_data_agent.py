"""
Market Data Agent for retrieving and analyzing market data using Alpha Vantage API.
"""

import logging
import os
from typing import Dict, List, Optional
import requests
from datetime import datetime, timedelta
import numpy as np
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MarketDataAgent:
    def __init__(self):
        """Initialize the MarketDataAgent with multiple API configurations."""
        self.logger = logging.getLogger(__name__)
        self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.iex_api_key = os.getenv('IEX_API_KEY')  # Free tier: 50,000 calls/month
        self.base_url_alpha = 'https://www.alphavantage.co/query'
        self.base_url_yahoo = 'https://query1.finance.yahoo.com/v8/finance/chart'
        self.base_url_iex = 'https://cloud.iexapis.com/stable'
        self.logger.info("Initializing MarketDataAgent with multiple data sources")
        
        # Add caching for rate limit optimization
        self._quote_cache = {}
        self._cache_duration = timedelta(minutes=5)  # Cache for 5 minutes

    async def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get current stock quote for a symbol using multiple APIs with fallback.
        
        Args:
            symbol (str): Stock symbol to get quote for
            
        Returns:
            Dict: Current stock quote data
        """
        # Check cache first
        cache_key = f"quote_{symbol}"
        if cache_key in self._quote_cache:
            cached_data, cache_time = self._quote_cache[cache_key]
            if datetime.now() - cache_time < self._cache_duration:
                self.logger.info(f"Returning cached quote for {symbol}")
                return cached_data
        
        # Try Alpha Vantage first
        try:
            self.logger.info(f"Getting stock quote for {symbol} from Alpha Vantage")
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.alpha_vantage_api_key
            }
            response = requests.get(self.base_url_alpha, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check for rate limit or API errors
            if 'Information' in data and 'rate limit' in data['Information'].lower():
                raise Exception("Alpha Vantage rate limit reached")
            
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                result = {
                    'symbol': symbol,
                    'current_price': float(quote.get('05. price', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent', '0%'),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0)),
                    'open': float(quote.get('02. open', 0)),
                    'previous_close': float(quote.get('08. previous close', 0)),
                    'volume': int(quote.get('06. volume', 0)),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'alpha_vantage'
                }
                # Cache the result
                self._quote_cache[cache_key] = (result, datetime.now())
                return result
        except Exception as e:
            self.logger.warning(f"Alpha Vantage failed for {symbol}: {str(e)}")
        
        # Try Yahoo Finance as fallback
        try:
            self.logger.info(f"Getting stock quote for {symbol} from Yahoo Finance")
            params = {
                'symbols': symbol,
                'range': '1d',
                'interval': '1m'
            }
            response = requests.get(self.base_url_yahoo, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result_data = data['chart']['result'][0]
                meta = result_data.get('meta', {})
                indicators = result_data.get('indicators', {})
                
                current_price = meta.get('regularMarketPrice', 0)
                previous_close = meta.get('previousClose', current_price)
                change = current_price - previous_close
                change_percent = f"{(change / previous_close * 100):.2f}%" if previous_close > 0 else "0%"
                
                result = {
                    'symbol': symbol,
                    'current_price': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'high': meta.get('regularMarketDayHigh', current_price),
                    'low': meta.get('regularMarketDayLow', current_price),
                    'open': meta.get('regularMarketOpen', current_price),
                    'previous_close': previous_close,
                    'volume': meta.get('regularMarketVolume', 0),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'yahoo_finance'
                }
                # Cache the result
                self._quote_cache[cache_key] = (result, datetime.now())
                return result
        except Exception as e:
            self.logger.warning(f"Yahoo Finance failed for {symbol}: {str(e)}")
        
        # Try IEX Cloud as final fallback
        if self.iex_api_key:
            try:
                self.logger.info(f"Getting stock quote for {symbol} from IEX Cloud")
                url = f"{self.base_url_iex}/stock/{symbol}/quote"
                params = {'token': self.iex_api_key}
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                result = {
                    'symbol': symbol,
                    'current_price': data.get('latestPrice', 0),
                    'change': data.get('change', 0),
                    'change_percent': f"{data.get('changePercent', 0):.2f}%",
                    'high': data.get('high', 0),
                    'low': data.get('low', 0),
                    'open': data.get('open', 0),
                    'previous_close': data.get('previousClose', 0),
                    'volume': data.get('latestVolume', 0),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'iex_cloud'
                }
                # Cache the result
                self._quote_cache[cache_key] = (result, datetime.now())
                return result
            except Exception as e:
                self.logger.warning(f"IEX Cloud failed for {symbol}: {str(e)}")
        
        # If all APIs fail, raise an exception
        raise Exception(f"All market data APIs failed for {symbol}. Please check your API keys and try again.")

    async def get_historical_data(self, symbol: str, days: int = 30) -> Dict:
        """
        Get historical price data for a symbol using Alpha Vantage API.
        
        Args:
            symbol (str): Stock symbol to get historical data for
            days (int): Number of days of historical data to fetch
            
        Returns:
            Dict: Historical price data with timestamps and prices
        """
        try:
            self.logger.info(f"Getting historical data for {symbol} for {days} days from Alpha Vantage")
            
            # Determine the appropriate function based on days
            if days <= 5:
                function = 'TIME_SERIES_INTRADAY'
                interval = '60min'
            elif days <= 30:
                function = 'TIME_SERIES_DAILY'
                interval = None
            else:
                function = 'TIME_SERIES_DAILY'
                interval = None
            
            params = {
                'function': function,
                'symbol': symbol,
                'apikey': self.alpha_vantage_api_key
            }
            
            if interval:
                params['interval'] = interval
            
            response = requests.get(self.base_url_alpha, params=params)
            
            # Check for API limits
            if response.status_code == 429:
                self.logger.warning(f"429 Rate Limited: Alpha Vantage API limit reached for {symbol}")
                return {
                    'symbol': symbol,
                    'timestamps': [],
                    'close_prices': [],
                    'days': days,
                    'error': 'API rate limit reached. Please wait before making more requests.',
                    'data_source': 'alpha_vantage',
                    'rate_limited': True
                }
            
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                raise Exception(data['Error Message'])
            if 'Note' in data:
                self.logger.warning(f"API Note for {symbol}: {data['Note']}")
                return {
                    'symbol': symbol,
                    'timestamps': [],
                    'close_prices': [],
                    'days': days,
                    'error': 'API limit reached. Please wait before making more requests.',
                    'data_source': 'alpha_vantage',
                    'rate_limited': True
                }
            
            # Extract time series data - handle different response formats
            time_series_key = None
            for key in data.keys():
                if 'Time Series' in key:
                    time_series_key = key
                    break
            
            if not time_series_key:
                # Try alternative response format
                if 'Time Series (Daily)' in data:
                    time_series_key = 'Time Series (Daily)'
                elif 'Time Series (60min)' in data:
                    time_series_key = 'Time Series (60min)'
                else:
                    self.logger.warning(f"Available keys in response: {list(data.keys())}")
                    raise Exception(f"No time series data found for {symbol}")
            
            time_series = data[time_series_key]
            
            if not time_series:
                raise Exception(f"Empty time series data for {symbol}")
            
            # Convert to sorted list of dates
            dates = sorted(time_series.keys(), reverse=True)[:days]
            
            if not dates:
                raise Exception(f"No valid dates found in time series for {symbol}")
            
            timestamps = []
            close_prices = []
            open_prices = []
            high_prices = []
            low_prices = []
            volumes = []
            
            for date in dates:
                daily_data = time_series[date]
                timestamps.append(datetime.strptime(date, '%Y-%m-%d').timestamp())
                close_prices.append(float(daily_data.get('4. close', 0)))
                open_prices.append(float(daily_data.get('1. open', 0)))
                high_prices.append(float(daily_data.get('2. high', 0)))
                low_prices.append(float(daily_data.get('3. low', 0)))
                volumes.append(int(daily_data.get('5. volume', 0)))
            
            historical_data = {
                'symbol': symbol,
                'timestamps': timestamps,
                'open_prices': open_prices,
                'high_prices': high_prices,
                'low_prices': low_prices,
                'close_prices': close_prices,
                'volumes': volumes,
                'days': len(dates),
                'data_source': 'alpha_vantage'
            }
            
            if len(close_prices) > 0:
                historical_data['statistics'] = {
                    'current_price': close_prices[0],  # Most recent
                    'price_change': close_prices[0] - close_prices[-1] if len(close_prices) > 1 else 0,
                    'price_change_percent': ((close_prices[0] - close_prices[-1]) / close_prices[-1] * 100) if len(close_prices) > 1 and close_prices[-1] > 0 else 0,
                    'min_price': min(close_prices),
                    'max_price': max(close_prices),
                    'avg_price': sum(close_prices) / len(close_prices)
                }
            
            self.logger.info(f"Successfully fetched {len(close_prices)} data points for {symbol} from Alpha Vantage")
            return historical_data
            
        except Exception as e:
            self.logger.error(f"Error getting historical data from Alpha Vantage for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'timestamps': [],
                'close_prices': [],
                'days': days,
                'error': str(e),
                'data_source': 'alpha_vantage'
            }

    async def calculate_volatility(self, symbol: str, days: int = 30) -> Dict:
        """
        Calculate volatility metrics for a symbol using historical data from Alpha Vantage.
        
        Args:
            symbol (str): Stock symbol
            days (int): Number of days for volatility calculation
            
        Returns:
            Dict: Volatility metrics including standard deviation and beta
        """
        try:
            self.logger.info(f"Calculating volatility for {symbol} using Alpha Vantage data")
            historical_data = await self.get_historical_data(symbol, days)
            
            # Check for specific error conditions
            if 'rate_limited' in historical_data:
                return {
                    'symbol': symbol,
                    'volatility': 0,
                    'annualized_volatility': 0,
                    'daily_returns': [],
                    'error': 'API rate limit reached. Volatility calculation unavailable.',
                    'data_source': 'alpha_vantage',
                    'rate_limited': True
                }
            elif 'error' in historical_data or len(historical_data['close_prices']) < 2:
                return {
                    'symbol': symbol,
                    'volatility': 0,
                    'annualized_volatility': 0,
                    'daily_returns': [],
                    'error': historical_data.get('error', 'Insufficient data for volatility calculation'),
                    'data_source': 'alpha_vantage'
                }
            
            prices = historical_data['close_prices']
            daily_returns = []
            for i in range(1, len(prices)):
                if prices[i-1] > 0:
                    daily_return = (prices[i] - prices[i-1]) / prices[i-1]
                    daily_returns.append(daily_return)
            
            if len(daily_returns) == 0:
                return {
                    'symbol': symbol,
                    'volatility': 0,
                    'annualized_volatility': 0,
                    'daily_returns': [],
                    'error': 'No valid returns calculated',
                    'data_source': 'alpha_vantage'
                }
            
            volatility = np.std(daily_returns)
            annualized_volatility = volatility * np.sqrt(252)
            
            return {
                'symbol': symbol,
                'volatility': float(volatility),
                'annualized_volatility': float(annualized_volatility),
                'daily_returns': daily_returns,
                'days_analyzed': len(daily_returns),
                'data_source': 'alpha_vantage'
            }
        except Exception as e:
            self.logger.error(f"Error calculating volatility for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'volatility': 0,
                'annualized_volatility': 0,
                'daily_returns': [],
                'error': str(e),
                'data_source': 'alpha_vantage'
            }

# Create the ADK tool
@FunctionTool
def get_market_data_tool(symbol: str) -> Dict:
    """ADK tool for getting market data."""
    logger.info("Market data tool called")
    agent = MarketDataAgent()
    return agent.get_stock_quote(symbol)

# Create the ADK agent
market_agent = LlmAgent(
    name="market_data_agent",
    description="Fetches and analyzes market data using Alpha Vantage API.",
    tools=[get_market_data_tool],
)

