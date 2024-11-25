import requests
import logging
from config import COINMARKETCAP_API_KEY

BASE_URL = "https://pro-api.coinmarketcap.com"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_ethereum_contract(token_symbol):
    """
    Fetches the Ethereum contract address for a given token symbol using the CoinMarketCap API.

    Args:
        token_symbol (str): The symbol of the token (e.g., "USDC").

    Returns:
        str: Contract address if found, or "Unknown".
    """
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
        params = {"symbol": token_symbol.upper()}  # Ensure the symbol is uppercase

        logging.info(f"Fetching Ethereum contract for {token_symbol} from CoinMarketCap API...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        # Check if the API call was successful
        if data["status"]["error_code"] != 0:
            logging.error(f"API error fetching Ethereum contract for {token_symbol}: {data['status']['error_message']}")
            return "Unknown"

        token_data = data["data"].get(token_symbol.upper())
        if token_data:
            platforms = token_data.get("platforms", {})
            # Ethereum's platform ID is 1027
            contract_address = None
            for platform_name, address in platforms.items():
                if platform_name.lower() == "ethereum":
                    contract_address = address
                    break

            if contract_address:
                logging.info(f"Token {token_symbol} found on Ethereum with contract address {contract_address}.")
                return contract_address
            else:
                logging.warning(f"Contract address not found for token: {token_symbol} on Ethereum.")
                return "Unknown"
        else:
            logging.warning(f"Token {token_symbol} not found in CoinMarketCap data.")
            return "Unknown"

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error fetching Ethereum contract for {token_symbol}: {e}")
        return "Unknown"
    except Exception as e:
        logging.error(f"Unexpected error fetching Ethereum contract for {token_symbol}: {e}")
        return "Unknown"

def get_coin_id(symbol):
    """
    Fetch the CoinMarketCap ID for a given token symbol.

    Args:
        symbol (str): The token symbol (e.g., "BTC", "ETH").

    Returns:
        int: The CoinMarketCap ID for the token, or None if not found.

    Raises:
        ValueError: If the token symbol is not found in the response.
    """
    try:
        url = f"{BASE_URL}/v1/cryptocurrency/map"
        headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
        params = {"symbol": symbol.upper()}

        logging.info(f"Fetching CoinMarketCap ID for symbol: {symbol}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        for coin in data.get("data", []):
            if coin["symbol"].upper() == symbol.upper():
                return coin["id"]

        logging.warning(f"Token symbol '{symbol}' not found in CoinMarketCap data.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error fetching CoinMarketCap ID for {symbol}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching CoinMarketCap ID for {symbol}: {e}")
        return None


def get_latest_price(symbol):
    """
    Fetch the latest price and market data for a given token symbol.

    Args:
        symbol (str): The token symbol (e.g., "BTC", "ETH").

    Returns:
        dict: A dictionary containing:
            - "price" (float or str): The latest price.
            - "market_cap" (float or str): The market capitalization.
            - "volume_24h" (float or str): The 24-hour trading volume.

        or None if not found.

    Raises:
        ValueError: If the token's CoinMarketCap ID cannot be resolved or the price data is unavailable.
    """
    try:
        coin_id = get_coin_id(symbol)
        if not coin_id:
            logging.warning(f"Unable to resolve CoinMarketCap ID for symbol '{symbol}'.")
            return None

        url = f"{BASE_URL}/v2/cryptocurrency/quotes/latest"
        headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
        params = {"id": coin_id}

        logging.info(f"Fetching latest price for symbol: {symbol} (Coin ID: {coin_id})")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        # Validate response structure
        if str(coin_id) not in data.get("data", {}):
            logging.warning(f"No quote data found for CoinMarketCap ID '{coin_id}'.")
            return None

        quote = data["data"][str(coin_id)]["quote"]["USD"]
        return {
            "price": quote.get("price", "N/A"),
            "market_cap": quote.get("market_cap", "N/A"),
            "volume_24h": quote.get("volume_24h", "N/A"),
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error fetching latest price for {symbol}: {e}")
        return None
    except KeyError as e:
        logging.error(f"Unexpected response format fetching latest price for {symbol}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching latest price for {symbol}: {e}")
        return None
