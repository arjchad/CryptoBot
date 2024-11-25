import requests
from config import RUGCHECK_API_URL
import logging
# Analyze the quality of a Threads audience (adjusted from Twitter analysis)



def analyze_threads_audience(username, api_url="https://some-threads-audience-api.com/analyze"):
    """
    Analyze the quality of a Threads audience.

    Args:
        username (str): Threads username to analyze.
        api_url (str): API endpoint for Threads audience analysis.

    Returns:
        dict: Analysis results.
    """
    try:
        # Construct the request payload
        payload = {"username": username}

        # Make the API request
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        # Return the JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error analyzing Threads audience for {username}: {e}")
        return {}

# Analyze token contract via RugCheck API
def analyze_token_contract(mint_address):
    """
    Analyzes the token contract using RugCheck's new API.

    Args:
        mint_address (str): The mint address of the token.

    Returns:
        dict: A dictionary containing the rug score and other relevant metrics.
    """
    try:
        # Construct the URL for the token report
        endpoint = f"{RUGCHECK_API_URL}/tokens/{mint_address}/report/summary"
        logging.info(f"Analyzing token with mint address {mint_address} using RugCheck...")

        # Make the GET request to RugCheck API
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response
        data = response.json()

        # Validate data
        if "error" in data:
            logging.error(f"RugCheck API returned error for token {mint_address}: {data['error']}")
            return {"rug_score": 0, "holder_supply": "Error"}

        # Extract relevant information with defaults for missing fields
        rug_score = data.get("rug_score", 0)  # Default to 0 if unavailable
        holder_supply = data.get("holder_supply", "Unknown")  # Default to "Unknown"

        # Return extracted data
        return {
            "rug_score": rug_score,
            "holder_supply": holder_supply,
        }

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error analyzing token {mint_address}: {e}, Response: {response.text}")
        return {"rug_score": 0, "holder_supply": "HTTP Error"}
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error analyzing token {mint_address}: {e}")
        return {"rug_score": 0, "holder_supply": "Request Error"}
    except Exception as e:
        logging.error(f"Unexpected error analyzing token {mint_address}: {e}")
        return {"rug_score": 0, "holder_supply": "Unknown"}
