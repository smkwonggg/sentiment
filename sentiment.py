import nltk
import random
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import twitter_samples
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier

nltk.download('twitter_samples')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# loading and preprocessing data (randomdize)
random.seed(99)

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')

tweets = positive_tweets + negative_tweets
labels = ['Positive'] * len(positive_tweets) + ['Negative'] * len(negative_tweets)

combined = list(zip(tweets, labels))
random.shuffle(combined)
tweets, labels = zip(*combined)

# tokenization
text = "qipao mum is gay and so do Marco. marco is a nice guy without girlfriend and he is a femboi who wear chastity cage. Marco running is better than kwong"
token = word_tokenize(text)

# remove stopwords
stopwords = stopwords.words('english')
duplicate = list(set(token).intersection(set(stopwords)))
for word in duplicate:
    while word in token:
        token.remove(word)
clean_token = token

# steaming and lemmatization
stemmer = PorterStemmer() # 字根, e.g. running -> run
lemmatizer = WordNetLemmatizer() # 字源, e.g. better -> good

stemmed_token = [stemmer.stem(word) for word in clean_token]
lemmatized_token = [lemmatizer.lemmatize(word) for word in clean_token]

# feature extraction for ML
all_words = []
for tweet in tweets:
    for word in word_tokenize(tweet):
        all_words.append(word.lower())
all_words_freq = FreqDist(all_words)

word_features = list(all_words_freq.keys())[:2000]

def document_features(document):
    document_words = set(document)
    features = {} # create an empty dict
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words) # the (bool) is the value for the [key] in the dict
    return features # a dict with {'key1': 'value1'}

feature_sets = []
for (tweet, label) in zip(tweets, labels):
    feature_sets.append((document_features(word_tokenize(tweet)), label))

train_set, test_set = feature_sets[1000:], feature_sets[:1000]

# Sentiment Analysis Model
classifier = NaiveBayesClassifier.train(train_set)

# training and evaluate the model
accuracy = nltk.classify.util.accuracy(classifier, test_set)
print(accuracy)
