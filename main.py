# main.py
import logging
from utils.threads_scraper import scrape_threads  # Your provided function
from utils.data_aggregator import aggregate_token_mentions
import pandas as pd
from config import USERNAMES, KEYWORDS
from utils.truncate import truncate_float

def main():
    logging.basicConfig(level=logging.INFO)

    # List to hold all scraped data
    scraped_data_list = []

    # Step 1: Scrape posts from all users.
    for username in USERNAMES:
        scraped_data = scrape_threads(username, KEYWORDS)
        scraped_data_list.append(scraped_data)

    # Step 2: Aggregate token mentions.
    token_data = aggregate_token_mentions(scraped_data_list)

    # Step 3: Prepare data for reporting.
    report_data = []
    for token_name, data in token_data.items():
        price = data["price"]
        if price is not None:
            price = truncate_float(price, 3)
        report_data.append({
            "Token": token_name,
            "Mentions": data["count"],
            "Usernames": ', '.join(data["usernames"]),
            "Current Price (USD)": price,
            "24h Trend (%)": data["trend"],
        })

    # Step 4: Create a DataFrame and save to CSV.
    df = pd.DataFrame(report_data)
    df.sort_values(by="Mentions", ascending=False, inplace=True)
    df.to_csv("token_mentions_report.csv", index=False)
    logging.info("Report generated: token_mentions_report.csv")

if __name__ == "__main__":
    main()





































# from config import *
# import asyncio
# import logging
# from utils.audience_analysis import analyze_token_contract
# from utils.minting_bot import main, monitor_and_notify
# from utils.solana_utils import fetch_rugcheck_report, is_token_on_solana
# from utils.threads_scraper import scrape_threads
# from utils.blockchain_utils import fetch_contract_details, process_tokens, determine_blockchain
# from utils.csv_utils import save_threads_to_csv
# from utils.coinmarketcap_api import get_latest_price
# from utils.blockchain_utils import process_tokens
#
# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#
#
# def fetch_and_monitor_tokens(usernames, keywords):
#     tokens_to_monitor = []
#     threads_data = []
#     extracted_tokens = []
#     skipped_tokens = []
#
#     logging.info("Starting to scrape Threads posts for tokens...")
#     for username in usernames:
#         try:
#             logging.info(f"Scraping posts for @{username}...")
#             tokens = scrape_threads(username, keywords)
#             if not tokens:
#                 logging.info(f"No tokens found for @{username}.")
#                 continue
#             extracted_tokens.extend(tokens)
#             threads_data.extend(tokens)
#         except Exception as e:
#             logging.error(f"Error scraping Threads for @{username}: {e}")
#             continue
#
#     processed_tokens = process_tokens(extracted_tokens)
#
#     for token_detail in processed_tokens:
#         try:
#             token_name = token_detail.get("token_name", "N/A")
#             blockchain = determine_blockchain(token_name)
#             token_detail['blockchain'] = blockchain
#
#             if blockchain == "Unknown":
#                 logging.warning(f"Skipping token {token_name} as it was not found on any known blockchain.")
#                 skipped_tokens.append(token_name)
#                 continue
#
#             # Fetch contract address
#             contract_address = fetch_contract_details(token_name, blockchain)
#             token_detail['contract_address'] = contract_address
#
#             if contract_address == "Unknown":
#                 logging.warning(f"Skipping token {token_name} due to missing contract address.")
#                 skipped_tokens.append(token_name)
#                 continue
#
#             # Fetch contract address
#             contract_address = fetch_contract_details(token_name, blockchain)
#             token_detail['contract_address'] = contract_address
#
#             if contract_address == "Unknown":
#                 logging.warning(f"Skipping token {token_name} due to missing contract address.")
#                 skipped_tokens.append(token_name)
#                 continue
#
#             if blockchain == "Solana":
#                 mint_address = contract_address
#                 rugcheck_report = fetch_rugcheck_report(mint_address)
#                 rug_score = rugcheck_report.get("rug_score", 0)
#                 if rug_score < 70:
#                     logging.info(
#                         f"Token {token_name} (mint: {mint_address}) failed RugCheck with score {rug_score}. Skipping.")
#                     continue
#                 holder_supply = rugcheck_report.get("tokenMeta", {}).get("holder_supply", "N/A")
#             else:
#                 mint_address = "N/A"
#                 holder_supply = "N/A"
#                 rug_score = "N/A"
#
#             # Fetch latest price
#             price_data = get_latest_price(token_name)
#             price = price_data.get("price", "Unknown")
#
#             # Prepare token data
#             token_data = {
#                 "token_name": token_name,
#                 "contract_address": contract_address,
#                 "mint_address": mint_address,
#                 "blockchain": blockchain,
#                 "meta_match": True,
#                 "post_text": token_detail.get("post_text", "N/A"),
#                 "rug_score": rug_score,
#                 "holder_supply": holder_supply,
#                 "current_price": price,
#             }
#
#             tokens_to_monitor.append(token_detail)
#         except Exception as e:
#             logging.error(f"Error processing token {token_name}: {e}")
#
#     if skipped_tokens:
#         logging.warning(f"Skipped tokens due to missing contract address or unknown blockchain: {skipped_tokens}")
#
#     return {"tokens_to_monitor": tokens_to_monitor, "threads_data": threads_data}
#
#
#
# if __name__ == "__main__":
#     # Keywords to search for in Threads posts
#     keywords = [
#         "$", "buy", "sell", "trade", "crypto", "blockchain", "token",
#         "altcoin", "investment", "defi", "ethereum", "solana"
#     ]
#
#     # Threads usernames to scrape
#     usernames = ["jesselivermoretrade", "cryptovlogz", "investingwithrome"]
#
#
#     # Fetch tokens dynamically and prepare them for monitoring
#     token_data = fetch_and_monitor_tokens(usernames, keywords)
#     tokens_to_monitor = token_data["tokens_to_monitor"]
#     threads_data = token_data["threads_data"]
#
#     # Save raw Threads data to CSV
#     save_threads_to_csv(threads_data)
#
#     # Print the tokens dynamically fetched
#     logging.info("\nTokens to Monitor:")
#     for token in tokens_to_monitor:
#         logging.info(token)
#
#     # Run the bot with the dynamically generated tokens
#     asyncio.run(monitor_and_notify(tokens_to_monitor))
