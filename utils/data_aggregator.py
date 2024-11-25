# data_aggregator.py
import logging
from collections import defaultdict
from utils.price_fetcher import fetch_price_and_trend  # We'll implement this function next
import re

def aggregate_token_mentions(scraped_data_list):
    token_data = defaultdict(lambda: {
        "count": 0,
        "usernames": set(),
        "price": None,
        "trend": None
    })

    for scraped_data in scraped_data_list:
        for token_entry in scraped_data:
            token_name = token_entry["token_name"].strip().upper()
            token_name = re.sub(r'\W+', '', token_name)  # Remove any non-alphanumeric characters
            username = token_entry["username"]

            # Only count one mention per user
            if username not in token_data[token_name]["usernames"]:
                token_data[token_name]["count"] += 1
                token_data[token_name]["usernames"].add(username)

    # Fetch price and trend for each token
    for token_name in token_data:
        price_info = fetch_price_and_trend(token_name)
        token_data[token_name]["price"] = price_info.get("price")
        token_data[token_name]["trend"] = price_info.get("trend")

    return token_data
