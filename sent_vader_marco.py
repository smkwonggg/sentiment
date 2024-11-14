import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessary NLTK resources
nltk.download('vader_lexicon')

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Example sentences to analyze
sentences = [
    "YAY I MADE IT I AM SO NICE YES YES SO HAPPY EXCITING!!! I WON! I AM THE BEST!! i LOVE THE WORLD!!"
    "I don’t know why I am going back hku now bruh",
    "Fuck it I wasted whole afternoon",
    "Where’s my girlfriend",
    "I feel loved when I with Sabina",
    "I hope someone come approach me",
    "A girl gave me chocolate in library",
    "This Christmas I’m going to Japan with girlfriend",
    "Omg a girl is approaching me",
    "Why urban studies so many things do",
    "When can I take some rest",
    "fuck my life I must die I must die immediately die die die die DEATHDEATHDEATHDEATH"
]

# Analyze sentiment scores
sentiment_scores = {}
for sentence in sentences:
    score = sia.polarity_scores(sentence)['compound']  # Get the compound score
    sentiment_scores[sentence] = score

# Function to plot sentiment scores
def plot_sentiment_scores(sentiment_scores):
    plt.figure(figsize=(10, 8))
    sns.barplot(x=list(sentiment_scores.keys()), y=list(sentiment_scores.values()))
    plt.title('Sentiment Scores Using VADER')
    plt.ylabel('Sentiment Score')
    plt.xlabel('Sentences')
    plt.xticks(rotation=45, ha='right')
    plt.axhline(0, color='gray', lw=1)  # Add a line at y=0 for reference
    plt.show()

# Plot the sentiment scores
plot_sentiment_scores(sentiment_scores)
