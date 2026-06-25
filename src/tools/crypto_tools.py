import os
import requests
from typing import List, Dict, Any, Optional

def get_crypto_price(symbol: str, vs_currency: str = "usd") -> Dict[str, Any]:
    """
    Get the current price of a cryptocurrency using CoinGecko API.
    """
    # Map symbol to id (simplified for common ones)
    symbol_to_id = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "bnb": "binancecoin"
    }
    coin_id = symbol_to_id.get(symbol.lower(), symbol.lower())

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}"
    api_key = os.getenv("COINGECKO_API_KEY")
    headers = {"x-cg-demo-api-key": api_key} if api_key else {}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if coin_id in data:
            return {"symbol": symbol, "price": data[coin_id][vs_currency.lower()], "currency": vs_currency}
        return {"error": f"Coin {symbol} not found."}
    except Exception as e:
        return {"error": f"Failed to fetch price: {str(e)}"}

def get_market_data(coin_id: str) -> Dict[str, Any]:
    """
    Get detailed market data for a specific coin.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    api_key = os.getenv("COINGECKO_API_KEY")
    headers = {"x-cg-demo-api-key": api_key} if api_key else {}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "name": data.get("name"),
            "market_cap": data.get("market_data", {}).get("market_cap", {}).get("usd"),
            "volume": data.get("market_data", {}).get("total_volume", {}).get("usd"),
            "description": data.get("description", {}).get("en", "")[:500] + "..."
        }
    except Exception as e:
        return {"error": f"Failed to fetch market data: {str(e)}"}
