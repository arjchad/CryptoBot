# price_fetcher.py
import requests
import logging
from config import COINMARKETCAP_API_KEY

def fetch_price_and_trend(token_symbol):
    """
    Fetches the current price and 24h trend for a cryptocurrency.

    Args:
        token_symbol (str): The symbol of the cryptocurrency.

    Returns:
        dict: A dictionary with 'price' and 'trend' (% change in last 24h).
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    params = {"symbol": token_symbol.upper(), "convert": "USD"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"]["error_code"] != 0:
            logging.error(f"Error fetching data for {token_symbol}: {data['status']['error_message']}")
            return {"price": None, "trend": None}

        if token_symbol.upper() not in data["data"]:
            logging.warning(f"Token {token_symbol} not found on CoinMarketCap.")
            return {"price": None, "trend": None}

        quote = data["data"][token_symbol.upper()]["quote"]["USD"]
        price = quote["price"]
        trend = quote["percent_change_24h"]

        return {"price": price, "trend": trend}

    except Exception as e:
        logging.error(f"Exception fetching data for {token_symbol}: {e}")
        return {"price": None, "trend": None}
