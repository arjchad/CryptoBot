import requests
import logging
from functools import lru_cache

PUMPFUN_API_BASE_URL = "https://api.pumpfunapis.com/api"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@lru_cache(maxsize=100)  # Cache up to 100 unique requests
def fetch_bonding_curve(mint):
    """
    Fetches bonding curve data for a given token. Results are cached to reduce duplicate requests.

    Args:
        mint (str): The mint address of the token.

    Returns:
        dict: Bonding curve data or an error message.
    """
    try:
        endpoint = f"{PUMPFUN_API_BASE_URL}/bonding-curve/{mint}"
        logging.info(f"Fetching bonding curve data for mint: {mint} from {endpoint}...")
        response = requests.get(endpoint)
        response.raise_for_status()

        # Parse and return JSON response
        data = response.json()
        if not data:
            logging.warning(f"No bonding curve data found for mint: {mint}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching bonding curve for mint {mint}: {e}")
        return {"error": str(e)}


@lru_cache(maxsize=100)  # Cache results for repeated queries
def fetch_balance(mint, owner_public_key):
    """
    Fetches the SPL token balance for a given mint and owner public key. Results are cached.

    Args:
        mint (str): The mint address of the token.
        owner_public_key (str): The public key of the token owner.

    Returns:
        dict: Token balance data or an error message.
    """
    try:
        endpoint = f"{PUMPFUN_API_BASE_URL}/balance"
        payload = {"mint": mint, "owner": owner_public_key}
        logging.info(f"Fetching balance for mint: {mint} and owner: {owner_public_key}...")
        response = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()

        # Parse and return JSON response
        data = response.json()
        if not data:
            logging.warning(f"No balance data found for mint: {mint} and owner: {owner_public_key}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching balance for mint {mint} and owner {owner_public_key}: {e}")
        return {"error": str(e)}


# @lru_cache(maxsize=100)  # Cache contract addresses for efficiency
# def fetch_ethereum_contract_DISCARD(token_name):
#     """
#     Fetches the Ethereum contract address for a given token name. Results are cached.
#
#     Args:
#         token_name (str): The name of the Ethereum token.
#
#     Returns:
#         str: Contract address if found, or "Unknown".
#     """
#     try:
#         url = f"{PUMPFUN_API_BASE_URL}/ethereum-token/{token_name}"
#         logging.info(f"Fetching Ethereum contract for {token_name} from {url}...")
#         response = requests.get(url)
#         response.raise_for_status()
#
#         contract_address = response.json().get("contract_address", "Unknown")
#         if contract_address == "Unknown":
#             logging.warning(f"Contract address not found for token: {token_name}")
#         return contract_address
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error fetching Ethereum contract for {token_name}: {e}")
#         return "Unknown"
