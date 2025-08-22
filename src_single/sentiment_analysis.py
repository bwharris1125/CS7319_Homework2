import logging
import re
from enum import Enum, auto
from pathlib import Path

# Set up logger
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Enum for sentiment state
class SentimentState(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    MIXED = auto()
    NEUTRAL = auto()

DATA_PATH = Path(__file__).parent.parent.joinpath("sample_data",
                                               "data", 
                                               "sample_us_posts.txt")
POS = set(["happy", "excited", "thrilled", "love"])
NEG = set(["sad", "depressed", "angry", "upset"])

logger.debug(f'Using dataset: {DATA_PATH}')
logger.debug(f'POS: {POS} \nNEG: {NEG}')


def read_data(file_path: Path) -> list[str]:
    """
    Reads a file and returns a list of strings, each string is a line from the 
    file (stripped of trailing newlines).
    """
    lines = []
    try:
        with open(file_path, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
    except Exception as e:
        logger.debug(f"Error reading file {file_path}: {e}")
    return lines


def analyze_line(line: str,
                 pos_set: set[str],
                 neg_set: set[str]) -> SentimentState:
    """
    Counts the number of POS and NEG words in the line using regular
    expressions.
    Returns a tuple: (pos_count, neg_count)
    """
    line_lower = line.lower()
    pos_count = 0
    neg_count = 0

    for word in pos_set:
        pos_count += len(re.findall(rf'\b{re.escape(word)}\b', line_lower))
    for word in neg_set:
        neg_count += len(re.findall(rf'\b{re.escape(word)}\b', line_lower))

    if pos_count > 0 and neg_count == 0:
        sentiment = SentimentState.POSITIVE
    elif neg_count > 0 and pos_count == 0:
        sentiment = SentimentState.NEGATIVE
    elif pos_count > 0 and neg_count > 0:
        sentiment = SentimentState.MIXED
    else:
        sentiment = SentimentState.NEUTRAL

    return sentiment

def analyze_document(file_path: Path) -> SentimentState:
    data_lines = read_data(file_path)
    pos_sum = 0
    neg_sum = 0
    mix_sum = 0
    neutral_sum = 0

    for line in data_lines:
        sentiment = analyze_line(line=line, pos_set=POS, neg_set=NEG)
        logger.debug(f"Line: '{line}'\nSentiment: {sentiment.name}")
        if sentiment == SentimentState.POSITIVE:
            pos_sum += 1
        elif sentiment == SentimentState.NEGATIVE:
            neg_sum += 1
        elif sentiment == SentimentState.MIXED:
            mix_sum += 1
        elif sentiment == SentimentState.NEUTRAL:
            neutral_sum += 1

    sums = {
    "POSITIVE": pos_sum,
    "NEGATIVE": neg_sum,
    "MIXED": mix_sum,
    "NEUTRAL": neutral_sum
    }
    file_sentiment  =  SentimentState[max(sums, key=sums.get)]

    print(f"\nOverall Sentiment Analysis for '{file_path.name}': {file_sentiment.name}")
    return file_sentiment


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    analyze_document(DATA_PATH)
    