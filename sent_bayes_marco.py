import nltk
import random
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Create your own dataset
# Format: (message, sentiment_score)
my_dataset = [
    ('I love this product!', 1),
    ('This is the worst experience ever.', -1),
    ('I am very happy with my purchase.', 1),
    ('I am not satisfied with the service.', -1),
    ('It was okay, nothing special.', 0),
    ('Absolutely fantastic!', 1),
    ('I would not recommend this.', -1),
    ('Just fine, I guess.', 0),
    # Add more messages with sentiment scores
]

# Randomize the dataset
random.seed(1)
random.shuffle(my_dataset)

# Separate messages and labels
messages, labels = zip(*my_dataset)

# Preprocess text and remove stopwords
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

# Feature extraction for ML
all_words = []
for message in messages:
    all_words.extend(preprocess_text(message))

all_words_freq = FreqDist(all_words)
word_features = list(all_words_freq.keys())[:2000]  # Use the top 2000 words

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features[f'contains({word})'] = (word in document_words)
    return features

feature_sets = []
for (message, label) in zip(messages, labels):
    feature_sets.append((document_features(word_tokenize(message)), label))

# Split into training and test sets (e.g., 80% train, 20% test)
train_set, test_set = feature_sets[:int(len(feature_sets) * 0.8)], feature_sets[int(len(feature_sets) * 0.8):]

# Train the Naive Bayes Classifier
classifier = NaiveBayesClassifier.train(train_set)

# Evaluate the classifier
print("Classifier accuracy:", nltk.classify.accuracy(classifier, test_set))

# Classifying new messages
def classify_message(message):
    features = document_features(preprocess_text(message))
    return classifier.classify(features)

# Example usage
new_messages = [
    "I am so excited about this!",
    "This is the worst thing I've ever bought.",
    "It's okay, I suppose."
]

for message in new_messages:
    sentiment_value = classify_message(message)
    print(f'Message: "{message}" - Sentiment Score: {sentiment_value}')
