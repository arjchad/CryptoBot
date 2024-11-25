import tweepy
import time
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN

# Authenticate with Twitter API
def authenticate_twitter_api():
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,  # Use your Bearer Token here
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET,
    )
    return client

# Fetch the user ID for a given username
def get_user_id(api, username):
    try:
        user = api.get_user(username=username)
        return user.data.id
    except Exception as e:
        print(f"Error fetching user ID for {username}: {e}")
        return None

# Fetch all lists owned by a user and return their list IDs and names
def get_user_lists(api, user_id):
    try:
        # Fetch lists owned by the user using their ID
        lists = api.get_owned_lists(id=user_id).data
        # Build a dictionary with list names and their corresponding IDs
        list_data = {lst.name: lst.id for lst in lists}
        return list_data
    except Exception as e:
        print(f"Error fetching lists for user ID {user_id}: {e}")
        return {}

# A utility function to safely handle API calls with retry
def safe_api_call(api_function, *args, **kwargs):
    """Safely calls a Tweepy API function, handling rate limits."""
    while True:
        try:
            # Attempt the API call
            return api_function(*args, **kwargs)
        except tweepy.TooManyRequests:
            print("Rate limit exceeded. Retrying in 15 minutes...")
            time.sleep(15 * 60)  # Wait 15 minutes and retry
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

