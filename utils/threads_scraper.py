from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import time
import logging
from utils.blockchain_utils import determine_blockchain

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_threads(username, keywords):
    """
    Scrapes Threads posts for a specified username and searches for keywords.

    Args:
        username (str): Threads username to scrape.
        keywords (list): List of keywords to search for.

    Returns:
        list: Token names matching the keywords.
    """

    chromedriver_path = '/usr/local/bin/chromedriver'
    service = Service(chromedriver_path)

    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")  # Set a custom user agent

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the Threads page
        url = f"https://www.threads.net/{username}"
        logging.info(f"Scraping posts for @{username} at {url}")
        driver.get(url)
        time.sleep(5)  # Allow page to load fully

        # Save page source for debugging
        with open("threads_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Look for post content in <div> or <span> tags
        posts = soup.find_all('div', string=True)  # General search for <div> elements containing text
        logging.info(f"Found {len(posts)} potential posts.")

        post_data = []
        for post in posts:
            try:
                # Extract text content
                post_text = post.get_text(separator=" ", strip=True)
                logging.info(f"Extracted post text: {post_text}")

                # Check if any keywords match
                if any(keyword.lower() in post_text.lower() for keyword in keywords):
                    # Detect tokens in the $XXXX format
                    matches = re.findall(r"\$[A-Za-z0-9]{2,15}", post_text)
                    matches = [match for match in matches if not match[1:].isdigit()]
                    logging.info(f"Tokens detected: {matches}")

                    for match in matches:
                        token_name = match.strip("$")  # Remove the '$' symbol
                        blockchain = determine_blockchain(token_name)
                        # Add token to the post_data array
                        post_data.append({
                            "token_name": token_name,
                            "post_text": post_text,
                            "username": username,
                            "blockchain": blockchain,
                        })

            except Exception as e:
                logging.error(f"Error processing post: {e}")



        logging.info(f"Found {len(post_data)} tokens in posts by @{username}.")
        return post_data
    except Exception as e:
        logging.error(f"Error scraping Threads for @{username}: {e}")
        return []


    finally:
        # Quit the WebDriver
        driver.quit()

    # logging.info("\nTokens to Monitor:")
    # if tokens_to_monitor:
    #     for token in tokens_to_monitor:
    #         logging.info(token)
    # else:
    #     logging.warning("No valid tokens found to monitor.")

# if __name__ == "__main__":
#     test_post = "Check out $TESTTOKEN and $EXAMPLE for amazing crypto returns!"
#     matches = re.findall(r"\$[A-Za-z0-9]{2,15}", test_post)
#     logging.debug(f"Regex matches: {matches}")
