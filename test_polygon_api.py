#!/usr/bin/env python3
"""
Test script for Polygon.io API connectivity.
"""

import requests
import os
from datetime import datetime, timedelta

def test_polygon_api():
    """Test Polygon.io API connectivity."""
    
    print("🔍 Testing Polygon.io API Connectivity")
    print("=" * 40)
    
    # API key
    api_key = '0XY6ahcoYcmIt8dJW9YABjhhCmu1LT4p'
    base_url = 'https://api.polygon.io'
    
    # Test symbols
    test_symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    print(f"Testing date range: {start_str} to {end_str}")
    print()
    
    for symbol in test_symbols:
        print(f"Testing {symbol}...")
        
        # Try different symbol formats
        symbol_formats = [
            symbol,
            f"{symbol}.O",
            f"{symbol}.N", 
            f"{symbol}.A"
        ]
        
        for symbol_format in symbol_formats:
            try:
                url = f"{base_url}/v2/aggs/ticker/{symbol_format}/range/1/day/{start_str}/{end_str}"
                params = {
                    'apiKey': api_key,
                    'adjusted': 'true',
                    'sort': 'asc'
                }
                
                print(f"  Trying format: {symbol_format}")
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"    ✅ Success! Status: {data.get('status')}")
                    print(f"    📊 Results count: {data.get('resultsCount', 0)}")
                    
                    if data.get('resultsCount', 0) > 0:
                        results = data['results']
                        latest = results[-1]
                        print(f"    💰 Latest close: ${latest['c']}")
                        print(f"    📈 Price change: ${latest['c'] - results[0]['c']:.2f}")
                        break
                else:
                    print(f"    ❌ HTTP {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"    ❌ Error: {str(e)}")
        
        print()
    
    # Test current price endpoint
    print("Testing current price endpoint...")
    try:
        url = f"{base_url}/v2/snapshot/locale/us/markets/stocks/tickers"
        params = {
            'apiKey': api_key,
            'tickers': 'AAPL,MSFT'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current price endpoint works!")
            print(f"📊 Response keys: {list(data.keys())}")
        else:
            print(f"❌ Current price endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Current price endpoint error: {str(e)}")

if __name__ == "__main__":
    test_polygon_api() 