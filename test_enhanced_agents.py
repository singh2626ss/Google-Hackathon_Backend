#!/usr/bin/env python3
"""
Test script for enhanced portfolio management agents.
"""

import asyncio
import json
from agent.market_data_agent import MarketDataAgent
from agent.risk_assessment_agent import RiskAssessmentAgent
from agent.sentiment_analysis_agent import SentimentAnalysisAgent
from agent.reporting_agent import ReportingAgent

async def test_enhanced_agents():
    """Test the enhanced agents with sample data."""
    
    print("🧪 Testing Enhanced Portfolio Management Agents")
    print("=" * 50)
    
    # Sample portfolio data
    portfolio = [
        {'symbol': 'AAPL', 'quantity': 10, 'purchase_price': 150.0},
        {'symbol': 'MSFT', 'quantity': 5, 'purchase_price': 300.0}
    ]
    
    try:
        # Initialize agents
        print("📊 Initializing agents...")
        market_agent = MarketDataAgent()
        risk_agent = RiskAssessmentAgent()
        sentiment_agent = SentimentAnalysisAgent()
        reporting_agent = ReportingAgent()
        
        # Test 1: Enhanced Market Data
        print("\n📈 Testing Enhanced Market Data Agent...")
        for pos in portfolio:
            symbol = pos['symbol']
            print(f"  Testing {symbol}...")
            
            # Get current quote
            quote = await market_agent.get_stock_quote(symbol)
            print(f"    Current price: ${quote['current_price']}")
            
            # Get historical data
            historical = await market_agent.get_historical_data(symbol, days=7)
            if 'error' not in historical:
                print(f"    Historical data points: {len(historical['close_prices'])}")
            else:
                print(f"    Historical data error: {historical['error']}")
            
            # Get volatility
            volatility = await market_agent.calculate_volatility(symbol, days=30)
            if 'error' not in volatility:
                print(f"    Annualized volatility: {volatility['annualized_volatility']:.4f}")
            else:
                print(f"    Volatility error: {volatility['error']}")
        
        # Test 2: Enhanced Risk Assessment
        print("\n⚠️  Testing Enhanced Risk Assessment Agent...")
        
        # Get market data for risk calculation
        market_data = {}
        for pos in portfolio:
            quote = await market_agent.get_stock_quote(pos['symbol'])
            market_data[pos['symbol']] = quote
        
        risk_analysis = await risk_agent.calculate_portfolio_risk(portfolio, market_data)
        print(f"  Overall risk level: {risk_analysis['overall_risk_level']}")
        print(f"  Portfolio volatility: {risk_analysis['portfolio_volatility']:.4f}")
        print(f"  Diversification score: {risk_analysis['diversification_score']:.1f}")
        
        # Test 3: Enhanced Sentiment Analysis
        print("\n🧠 Testing Enhanced Sentiment Analysis Agent...")
        symbols = [pos['symbol'] for pos in portfolio]
        sentiment_summary = await sentiment_agent.get_portfolio_sentiment_summary(symbols)
        
        portfolio_sentiment = sentiment_summary['portfolio_sentiment']
        print(f"  Portfolio sentiment: {portfolio_sentiment['category']}")
        print(f"  Sentiment strength: {portfolio_sentiment['polarity']:.4f}")
        print(f"  Symbol breakdown: {len(sentiment_summary['symbol_breakdown'])} symbols")
        
        # Test 4: Enhanced Reporting
        print("\n📋 Testing Enhanced Reporting Agent...")
        report = await reporting_agent.generate_portfolio_report(
            portfolio=portfolio,
            market_data=market_data,
            risk_assessment=risk_analysis,
            sentiment_analysis=sentiment_summary
        )
        
        print(f"  Report generated successfully")
        print(f"  Performance return: {report['performance_analysis']['return_percentage']:.2f}%")
        print(f"  Risk level: {report['risk_analysis']['risk_level']}")
        print(f"  Sentiment: {report['market_sentiment']['overall_sentiment']}")
        print(f"  Recommendations: {len(report['recommendations'])}")
        
        # Check visualization data
        viz_data = report['visualization_data']
        print(f"  Visualization components: {list(viz_data.keys())}")
        
        if 'forecasting' in viz_data:
            print(f"  Forecasting scenarios: {list(viz_data['forecasting']['scenarios'].keys())}")
        
        print("\n✅ All enhanced agents tested successfully!")
        
        # Save sample report
        with open('test_enhanced_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("💾 Sample report saved to 'test_enhanced_report.json'")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_enhanced_agents()) 