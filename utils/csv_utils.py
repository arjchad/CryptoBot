import csv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def save_tweets_to_csv(tweets, file_path="data/tweets.csv"):
    """
    Saves tweets to a CSV file.

    Args:
        tweets (list): List of tweet strings.
        file_path (str): Path to the CSV file.

    Returns:
        None
    """
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tweet"])
            for tweet in tweets:
                writer.writerow([tweet])
        logging.info(f"Successfully saved tweets to {file_path}.")
    except IOError as e:
        logging.error(f"Error saving tweets to {file_path}: {e}")


def save_threads_to_csv(data, file_path="data/threads_data.csv"):
    """
    Saves scraped Threads token data to a CSV file, ensuring no duplicates
    and using mint address as fallback for Solana coins without a contract address.

    Args:
        data (list): List of dictionaries containing token details.
        file_path (str): Path to the CSV file.

    Returns:
        None
    """
    headers = [
        "Date & Time",
        "Contract Address",
        "Mint Address",
        "Scraped By Username",
        "Blockchain",
        "Post Content",
        "Token Name",
    ]

    # Add current timestamp to each row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Deduplicate data using a set
    unique_data = set()
    deduplicated_rows = []
    for item in data:
        # Debug log to ensure Solana tokens have mint addresses
        logging.debug(f"Processing item: {item}")

        # For Solana, use mint address if contract address is missing
        contract_address = item.get("contract_address", "N/A")
        if item.get("blockchain", "").lower() == "solana" and contract_address == "N/A":
            mint_address = item.get("mint_address", "N/A")
            if mint_address != "N/A":
                contract_address = mint_address
                logging.info(f"Fallback to mint address for {item.get('token_name', 'N/A')}: {mint_address}")
            else:
                logging.warning(f"No contract or mint address for {item.get('token_name', 'N/A')}")

        # Use a tuple of key fields to ensure uniqueness
        row_key = (contract_address, item.get("post_text", "N/A"), item.get("username", "N/A"))
        if row_key not in unique_data:
            unique_data.add(row_key)
            # Update the contract_address in the row
            item["contract_address"] = contract_address
            deduplicated_rows.append(item)

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            # Write headers
            writer.writeheader()

            # Write data rows
            for item in deduplicated_rows:
                writer.writerow({
                    "Date & Time": timestamp,
                    "Contract Address": item.get("contract_address", "N/A"),
                    "Mint Address": item.get("mint_address", "N/A"),
                    "Scraped By Username": item.get("username", "N/A"),
                    "Blockchain": item.get("blockchain", "N/A"),
                    "Post Content": item.get("post_text", "N/A"),
                    "Token Name": item.get("token_name", "N/A"),
                })

        logging.info(f"Successfully saved Threads data with Solana fallback to {file_path}.")
    except IOError as e:
        logging.error(f"Error saving Threads data to {file_path}: {e}")


