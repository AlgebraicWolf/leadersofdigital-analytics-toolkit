from config import APP_CONFIG
from enum import Enum

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

from instaclient import cl

# Class for different sentiments 
class Sentiment(Enum):
  POSITIVE = 1
  NEUTRAL = 2
  NEGATIVE = 3 

# Pull comments from an instagram post
def pull_instagram_comments(url: str):
  media_id = cl.media_id(cl.media_pk_from_url(url))
  comments = cl.media_comments(media_id)
  return list(map(lambda x: x.text, comments))

# Sentiment analysis wrapper
# Classes are mapped as follows:
# Positive -> Positive
# Negative -> Negative
# Speech, Neutral -> Neutral
# Skip is not included in the rating 
def analyze_messages(msgs: list[str]) -> list[Sentiment]:
  def preprocess_label(labels: str):
    if labels == 'positive':
      return Sentiment.POSITIVE
    elif (labels == 'neutral') or (labels == 'speech'):
      return Sentiment.NEUTRAL
    elif labels == 'negative':
      return Sentiment.NEGATIVE
    else:
      return None

  tokenizer = RegexTokenizer()
  m = FastTextSocialNetworkModel(tokenizer=tokenizer)

  estimates = m.predict(msgs, k=1)
  labels = map(lambda x: list(x.keys())[0], estimates) # Pull the most likely sentiment classes
  labels = map(preprocess_label, labels) # Turn strings into labels from Enum
  labels = filter(lambda x: x is not None, labels) # Drop comments that could not be processed 

  return list(labels)

# Calculate percentage for a given value
def calculate_percentage(arr, val) -> float:
  return len(list(filter(lambda x: x == val, arr))) / len(arr)

# Calculate percentage for each class
def calculate_statistics(msgs: list[Sentiment]) -> dict[str, float]:
  result = dict()
  result['positive'] = calculate_percentage(msgs, Sentiment.POSITIVE)
  result['neutral'] = calculate_percentage(msgs, Sentiment.NEUTRAL)
  result['negative'] = calculate_percentage(msgs, Sentiment.NEGATIVE)

  return result
