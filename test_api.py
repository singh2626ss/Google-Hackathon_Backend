import requests
import json
from pprint import pprint

def test_portfolio_analysis():
    url = "http://localhost:8000/analyze-portfolio"
    
    # Sample portfolio data
    data = {
        "portfolio": [
            {"symbol": "AAPL", "quantity": 10, "purchase_price": 150.0},
            {"symbol": "GOOGL", "quantity": 5, "purchase_price": 2800.0},
            {"symbol": "MSFT", "quantity": 8, "purchase_price": 300.0}
        ],
        "risk_tolerance": "moderate",
        "investment_goals": ["growth", "income"],
        "time_horizon": "5-10 years"
    }
    
    # Make the request
    response = requests.post(url, json=data)
    
    # Check if request was successful
    if response.status_code == 200:
        print("\n=== Portfolio Analysis Results ===\n")
        
        # Get the response data
        result = response.json()
        
        # Print portfolio summary
        print("Portfolio Summary:")
        print(f"Number of positions: {result['portfolio_summary']['number_of_positions']}")
        print("\nPositions:")
        for position in result['portfolio_summary']['positions']:
            print(f"\n{position['symbol']}:")
            print(f"  Quantity: {position['quantity']}")
            print(f"  Purchase Price: ${position['purchase_price']:.2f}")
            print(f"  Current Price: ${position['current_price']:.2f}")
            print(f"  Position Value: ${position['position_value']:.2f}")
            print(f"  Return: {position['return_percentage']:.2f}%")
        
        # Print performance analysis
        print("\nPerformance Analysis:")
        perf = result['performance_analysis']
        print(f"Total Cost: ${perf['total_cost']:.2f}")
        print(f"Current Value: ${perf['current_value']:.2f}")
        print(f"Total Return: ${perf['total_return']:.2f}")
        print(f"Return Percentage: {perf['return_percentage']:.2f}%")
        
        # Print risk analysis
        print("\nRisk Analysis:")
        risk = result['risk_analysis']
        print(f"Risk Level: {risk['risk_level']}")
        print(f"Concentration Metrics:")
        print(f"  HHI: {risk['concentration_metrics']['hhi']:.4f}")
        print(f"  Top 3 Concentration: {risk['concentration_metrics']['top_3_concentration']:.2f}")
        
        # Print market sentiment
        print("\nMarket Sentiment:")
        sentiment = result['market_sentiment']
        print(f"Overall Sentiment: {sentiment['overall_sentiment']}")
        print(f"Sentiment Strength: {sentiment['sentiment_strength']:.2f}")
        print(f"Subjectivity: {sentiment['subjectivity']:.2f}")
        
        # Print recommendations
        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"\nType: {rec['type']}")
            print(f"Priority: {rec['priority']}")
            print(f"Action: {rec['action']}")
            print(f"Details: {rec['details']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_portfolio_analysis() 