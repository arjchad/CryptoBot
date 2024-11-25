import requests
import asyncio
import logging
from config import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from discord.ext import commands
from discord import Intents
from utils.audience_analysis import analyze_token_contract
from utils.coinmarketcap_api import get_latest_price

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

intents = Intents.default()
intents.messages = True
# Initialize Discord bot
discord_client = commands.Bot(command_prefix="!", intents=intents)

logging.basicConfig(level=logging.INFO)

async def send_discord_message(message):
    """
    Sends a message to the specified Discord channel.
    """
    try:
        channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(message)
        else:
            logging.error("Discord channel not found.")
    except Exception as e:
        logging.error(f"Error sending message to Discord: {e}")

async def monitor_and_notify(tokens):
    for token in tokens:
        try:
            contract_address = token["contract_address"]
            token_name = token["token_name"]

            # Check if the token passes the RugCheck score threshold
            if not token.get("rug_score", 0) > 70:
                logging.info(f"Token {contract_address} failed RugCheck.")
                continue

            # Fetch price using CoinMarketCap API (optional if already fetched)
            price_data = get_latest_price(token_name)
            price = price_data["price"] if price_data else token.get("current_price", "Unknown")

            # Construct the message using data from `token`
            message = (
                f"Token Passed Criteria!\n"
                f"Token Name: {token_name}\n"
                f"Contract Address: {contract_address}\n"
                f"RugCheck Score: {token.get('rug_score')}\n"
                f"Holder Supply: {token.get('holder_supply', 'Unknown')}\n"
                f"Meta Match: {token.get('meta_match')}\n"
                f"Price: {price}"
            )
            logging.info(f"Notifying Discord about {contract_address}...")
            await send_discord_message(message)
            await asyncio.sleep(10)  # Pause between checks
        except Exception as e:
            logging.exception(f"Error processing token {token['token_name']}: {e}")


async def main(tokens):
    """
    Main function to monitor tokens and notify Discord.
    """
    try:
        await discord_client.start(DISCORD_TOKEN)  # Start Discord bot
        await monitor_and_notify(tokens)
    finally:
        await discord_client.close()  # Cleanly close the bot
