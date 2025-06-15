"""
Market Data Agent for retrieving and analyzing market data using Finnhub API.
"""

import logging
import os
from typing import Dict, List, Optional
import requests
from datetime import datetime, timedelta
import pandas as pd
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
        """Initialize the MarketDataAgent with API configuration."""
        self.logger = logging.getLogger(__name__)
        self.finnhub_api_key = os.getenv('FINNHUB_API_KEY')
        self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url_finnhub = 'https://finnhub.io/api/v1'
        self.base_url_alpha_vantage = 'https://www.alphavantage.co/query'
        self.logger.info("Initializing MarketDataAgent")

    async def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get current stock quote for a symbol using Finnhub API with retry logic.
        
        Args:
            symbol (str): Stock symbol to get quote for
            
        Returns:
            Dict: Current stock quote data
        """
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.logger.info(f"Getting stock quote for {symbol}")
                url = f"{self.base_url_finnhub}/quote"
                params = {
                    'symbol': symbol,
                    'token': self.finnhub_api_key
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                quote_data = response.json()
                return {
                    'symbol': symbol,
                    'current_price': quote_data.get('c'),
                    'change': quote_data.get('dp'),
                    'high': quote_data.get('h'),
                    'low': quote_data.get('l'),
                    'open': quote_data.get('o'),
                    'previous_close': quote_data.get('pc'),
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                retry_count += 1
                self.logger.error(f"Error getting stock quote for {symbol}: {str(e)}")
                if retry_count == max_retries:
                    raise
                self.logger.info(f"Retrying... Attempt {retry_count} of {max_retries}")

    async def get_alpha_vantage_quote(self, symbol: str) -> Dict:
        """
        Get current stock quote for a symbol using Alpha Vantage API with retry logic.
        
        Args:
            symbol (str): Stock symbol to get quote for
            
        Returns:
            Dict: Current stock quote data
        """
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.logger.info(f"Getting Alpha Vantage stock quote for {symbol}")
                url = self.base_url_alpha_vantage
                params = {
                    'function': 'GLOBAL_QUOTE',
                    'symbol': symbol,
                    'apikey': self.alpha_vantage_api_key
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                quote_data = response.json()
                return {
                    'symbol': symbol,
                    'current_price': quote_data.get('05. price'),
                    'change': quote_data.get('09. change'),
                    'high': quote_data.get('03. high'),
                    'low': quote_data.get('04. low'),
                    'open': quote_data.get('02. open'),
                    'previous_close': quote_data.get('08. previous close'),
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                retry_count += 1
                self.logger.error(f"Error getting Alpha Vantage stock quote for {symbol}: {str(e)}")
                if retry_count == max_retries:
                    raise
                self.logger.info(f"Retrying... Attempt {retry_count} of {max_retries}")

    async def get_company_profile(self, symbol: str) -> Dict:
        """
        Get company profile information.
        
        Args:
            symbol (str): Stock symbol to get profile for
            
        Returns:
            Dict: Company profile data
        """
        try:
            self.logger.info(f"Getting company profile for {symbol}")
            url = f"{self.base_url_finnhub}/stock/profile2"
            params = {
                'symbol': symbol,
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error getting company profile for {symbol}: {str(e)}")
            raise

    async def get_market_news(self, category: str = 'general') -> List[Dict]:
        """
        Get market news for a specific category.
        
        Args:
            category (str): News category (general, forex, crypto, merger)
            
        Returns:
            List[Dict]: List of news articles
        """
        try:
            self.logger.info(f"Getting market news for category: {category}")
            url = f"{self.base_url_finnhub}/news"
            params = {
                'category': category,
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error getting market news: {str(e)}")
            raise

    async def get_technical_indicators(self, symbol: str, resolution: str = 'D') -> Dict:
        """
        Get technical indicators for a symbol.
        
        Args:
            symbol (str): Stock symbol
            resolution (str): Data resolution (D for daily, W for weekly, M for monthly)
            
        Returns:
            Dict: Technical indicators data
        """
        try:
            self.logger.info(f"Getting technical indicators for {symbol}")
            url = f"{self.base_url_finnhub}/indicator"
            params = {
                'symbol': symbol,
                'resolution': resolution,
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error getting technical indicators for {symbol}: {str(e)}")
            raise
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
    description="Fetches and analyzes market data using Finnhub API.",
    tools=[get_market_data_tool],
)

