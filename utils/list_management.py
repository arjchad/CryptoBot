import tweepy

# Add influencers to a Twitter list
def add_to_list(api, list_slug, owner_screen_name, influencers):
    """Add influencers to the specified Twitter list."""
    for influencer in influencers:
        try:
            api.add_list_member(slug=list_slug, owner_screen_name=owner_screen_name, screen_name=influencer)
            print(f"Added {influencer} to the list {list_slug}.")
        except tweepy.TweepError as e:
            print(f"Error adding {influencer}: {e}")
