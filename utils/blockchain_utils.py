import logging
import re

import requests
from utils.solana_utils import is_token_on_solana
from utils.coinmarketcap_api import fetch_ethereum_contract

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_tokens(tokens):
    """
    Processes a list of token dictionaries and removes duplicates based on unique identifiers.

    Args:
        tokens (list): List of token dictionaries.

    Returns:
        list: A list of unique token dictionaries.
    """
    seen = set()
    unique_tokens = []
    for token in tokens:
        # Use a tuple of unique identifiers (e.g., name and contract_address) as a key
        token_key = (token.get("token_name"), token.get("contract_address"))
        if token_key not in seen:
            seen.add(token_key)
            unique_tokens.append(token)
    return unique_tokens


def determine_blockchain(token_name):
    """
    Determines the blockchain(s) for a given token by checking Solana and Ethereum.

    Args:
        token_name (str): Token name.

    Returns:
        str: "Solana", "Ethereum", or "Unknown".
    """
    try:
        # Check if token exists on Solana
        solana_mint_address = is_token_on_solana(token_name)
        if solana_mint_address:
            logging.info(f"Token {token_name} found on Solana with mint address {solana_mint_address}.")
            return "Solana"

        # Check if token exists on Ethereum
        ethereum_contract = fetch_ethereum_contract(token_name)
        if ethereum_contract != "Unknown":
            logging.info(f"Token {token_name} found on Ethereum with contract address {ethereum_contract}.")
            return "Ethereum"

        logging.warning(f"Token {token_name} not found on known blockchains.")
        return "Unknown"
    except Exception as e:
        logging.error(f"Error determining blockchain for {token_name}: {e}")
        return "Unknown"

def is_valid_token(token_name):
    """
    Validates the token name format using regex.

    Args:
        token_name (str): Token name.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.match(r"^[A-Za-z0-9._-]+$", token_name))


def fetch_contract_details(token_name, blockchain):
    """
    Fetches the contract address for a token based on its blockchain.

    Args:
        token_name (str): Token name.
        blockchain (str): Blockchain type ("Solana" or "Ethereum").

    Returns:
        str: Contract address or "Unknown".
    """
    try:
        if not is_valid_token(token_name):
            logging.warning(f"Invalid token name: {token_name}. Skipping.")
            return "Unknown"

        if blockchain == "Ethereum":
            logging.info(f"Fetching Ethereum contract for {token_name}...")
            return fetch_ethereum_contract(token_name)

        elif blockchain == "Solana":
            logging.info(f"Fetching Solana token details for {token_name}...")
            return is_token_on_solana(token_name)

        else:
            logging.warning(f"Unsupported blockchain type for {token_name}: {blockchain}")
            return "Unknown"

    except Exception as e:
        logging.error(f"Error fetching contract details for {token_name} on {blockchain}: {e}")
        return "Unknown"