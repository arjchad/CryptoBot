
from config import RUGCHECK_API_URL
import requests
import logging
from config import HELIUS_API_URL



# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



TOKEN_LIST_URL = "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json"





def fetch_rugcheck_report(mint_address):
    """
    Fetches the RugCheck report for a given Solana token mint address.

    Args:
        mint_address (str): The Solana token's mint address.

    Returns:
        dict: The RugCheck report data or an error message.
    """
    RUGCHECK_API_BASE_URL = RUGCHECK_API_URL  # Replace with the actual RugCheck base URL
    try:
        api_url = f"{RUGCHECK_API_BASE_URL}/tokens/{mint_address}/report/summary"
        headers = {"Content-Type": "application/json"}

        logging.info(f"Fetching RugCheck report for mint address: {mint_address}...")
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        report = response.json()
        logging.debug(f"RugCheck report for {mint_address}: {report}")  # Add this line
        return report
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching RugCheck report for {mint_address}: {e}")
        return {"error": f"HTTP error occurred: {e}"}
    except Exception as e:
        logging.error(f"Unexpected error fetching RugCheck report for {mint_address}: {e}")
        return {"error": f"Unexpected error occurred: {e}"}

def fetch_token_mint(token_name):
    """
    Fetches the mint address of a token by its name.

    Args:
        token_name (str): The name of the token (e.g., "USDC").

    Returns:
        str: The mint address of the token if found, or "Unknown".
    """
    try:
        response = requests.get(TOKEN_LIST_URL)
        response.raise_for_status()
        token_list = response.json().get("tokens", [])

        # Match token name case-insensitively
        for token in token_list:
            if token["symbol"].lower() == token_name.lower():
                return token["address"]

        logging.info(f"Token {token_name} not found in the SPL token list.")
        return "Unknown"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching token list: {e}")
        return "Unknown"


def is_token_on_solana(token_name):
    """
    Determines if a token exists on Solana, retrieves its mint address,
    and fetches the RugCheck report.

    Args:
        token_name (str): The name of the token (e.g., "USDC").

    Returns:
        dict: RugCheck report data if the token exists, or None.
    """
    mint_address = fetch_token_mint(token_name)
    if mint_address == "Unknown":
        logging.warning(f"Token {token_name} not found on Solana.")
        return None

    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [
                mint_address,
                {"encoding": "jsonParsed"}
            ],
        }

        response = requests.post(HELIUS_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Check if account exists
        if data.get("result", {}).get("value") is not None:
            return mint_address  # Return mint address directly

        logging.info(f"Token {token_name} (mint address: {mint_address}) does not exist on Solana.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error verifying token on Solana: {e}")
        return None




# if __name__ == "__main__":
#     token_name = "USDC"  # Replace with your token name
#     result = is_token_on_solana(token_name)
#     if result["exists"]:
#         print(f"Token {token_name} exists on Solana. Mint Address: {result['mint_address']}")
#     else:
#         print(f"Token {token_name} does not exist on Solana.")



# def fetch_solana_contract(token_name):
#     """
#     Queries Solscan API to fetch the contract address for a Solana token.
#
#     Args:
#         token_name (str): The token's name or symbol.
#
#     Returns:
#         str: Contract address if found, or "Unknown".
#
#     Raises:
#         requests.exceptions.RequestException: For HTTP errors during the API call.
#     """
#     try:
#         # Encode token name for URL safety
#         encoded_token_name = quote(token_name)
#         api_url = f"https://api.solscan.io/token/{encoded_token_name}"
#         headers = {
#             "User-Agent": "Mozilla/5.0",
#             "accept": "application/json",
#             "token": SOLSCAN_TOKEN_LIST_API
#         }
#
#         logging.info(f"Fetching Solana contract for token: {token_name} from {api_url}...")
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()
#
#         # Parse JSON response
#         data = response.json()
#
#         # Validate and extract contract address
#         contract_address = data.get("data", {}).get("address", "Unknown")
#         if contract_address == "Unknown":
#             logging.warning(f"Contract address not found for token: {token_name}")
#         return contract_address
#
#     except requests.exceptions.RequestException as e:
#         logging.error(f"HTTP error while fetching Solana contract for {token_name}: {e}")
#         return "Unknown"
#     except Exception as e:
#         logging.error(f"Unexpected error fetching Solana contract for {token_name}: {e}")
#         return "Unknown"
