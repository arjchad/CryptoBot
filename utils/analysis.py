import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Ensure necessary NLTK data is downloaded
nltk.download("punkt")
nltk.download("stopwords")

# Analyze popular narratives and tokens
def analyze_narratives(tweets):
    stop_words = set(stopwords.words("english"))
    all_tokens = []

    for tweet in tweets:
        tokens = word_tokenize(tweet)
        # Remove stopwords, mentions, URLs, and non-alphanumeric tokens
        filtered_tokens = [
            word.lower()
            for word in tokens
            if word.isalnum() and word.lower() not in stop_words
        ]
        all_tokens.extend(filtered_tokens)

    # Count token frequencies
    token_counts = Counter(all_tokens)
    return token_counts.most_common(20)  # Return top 20 tokens
