import requests
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PUMPFUN_BASE_URL = "https://pump.fun/coin"


def fetch_token_data(contract_address):
    """
    Fetches detailed data for a specific token from PumpFun using its contract address.

    Args:
        contract_address (str): The contract address of the token.

    Returns:
        dict: A dictionary containing token details, or None if an error occurs.
    """
    try:
        url = f"{PUMPFUN_BASE_URL}/{contract_address}"
        logging.info(f"Fetching data for token at {url}...")
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON or HTML (if API available, adjust accordingly)
        data = response.json()

        # Example structure (adjust based on actual API response)
        token_data = {
            "name": data.get("name", "Unknown"),
            "symbol": data.get("symbol", "Unknown"),
            "price": float(data.get("price", 0)),
            "volume": int(data.get("volume", 0)),
            "trend": data.get("trend", "Unknown").lower(),
            "contract_address": contract_address,
        }
        return token_data
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error fetching data for contract {contract_address}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching data for contract {contract_address}: {e}")
        return None


def fetch_multiple_tokens(contract_addresses):
    """
    Fetches data for multiple tokens using their contract addresses.

    Args:
        contract_addresses (list): List of contract addresses.

    Returns:
        pd.DataFrame: A DataFrame containing data for all fetched tokens.
    """
    tokens = []
    for contract_address in contract_addresses:
        token_data = fetch_token_data(contract_address)
        if token_data:
            tokens.append(token_data)

    # Convert to DataFrame for further analysis
    if tokens:
        return pd.DataFrame(tokens)
    else:
        logging.warning("No token data fetched.")
        return pd.DataFrame()


def analyze_tokens(token_df, volume_threshold=100000, trend='bullish'):
    """
    Filters and selects tokens based on volume and trend.

    Args:
        token_df (pd.DataFrame): DataFrame containing token information.
        volume_threshold (int): Minimum trading volume for selection.
        trend (str): Desired trend (e.g., "bullish", "bearish").

    Returns:
        pd.DataFrame: A DataFrame of selected tokens that meet the criteria.
    """
    try:
        logging.info(f"Analyzing tokens with volume >= {volume_threshold} and trend = '{trend}'...")
        if token_df.empty:
            logging.warning("Empty DataFrame passed to analyze_tokens.")
            return pd.DataFrame()

        # Filter tokens
        filtered_tokens = token_df[
            (token_df['volume'] >= volume_threshold) & (token_df['trend'] == trend.lower())
        ]

        # Sort by volume (descending)
        selected_tokens = filtered_tokens.sort_values(by='volume', ascending=False)
        logging.info(f"{len(selected_tokens)} tokens match the criteria.")
        return selected_tokens
    except Exception as e:
        logging.error(f"Error analyzing tokens: {e}")
        return pd.DataFrame()
