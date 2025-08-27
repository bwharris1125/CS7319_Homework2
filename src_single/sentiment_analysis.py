import argparse
import logging
import re
from enum import Enum, auto
from pathlib import Path

import matplotlib.pyplot as plt

# Set up logger
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Enum for sentiment state
class Sentiment(Enum):
    Positive = 1
    Negative = 2
    Mixed = 3
    Neutral = 4

def get_args() -> argparse.Namespace:
    """
    Parses command-line arguments for the sentiment analysis script.
    """
    # use example data when no filepath is provided
    example_data = Path(__file__).parent.parent.joinpath("sample_data",
                                               "data", 
                                               "sample_us_posts.txt")
    
    parser = argparse.ArgumentParser(
        description="Sentiment analysis of social media posts.")
    parser.add_argument("filepath", 
                        type=str, 
                        nargs="?", 
                        default=example_data, 
                        help="Path to input text file.")
    parser.add_argument("--no-chart",
                        action="store_true",
                        help="Do not display bar chart")
    args, _ = parser.parse_known_args()
    return args

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

def map_post(line: str, sentiments: dict[set[str], set[str]]) -> Sentiment:
    """
    Counts the number of POS and NEG words in the line using regular
    expressions.
    Returns a 'Sentiment' enum.
    """
    pos_count = 0
    neg_count = 0
    
    # tokenizing words using regex
    line_lower = line.lower()
    for word in sentiments["Positive"]:
        pos_count += len(re.findall(rf'\b{re.escape(word)}\b', line_lower))
    for word in sentiments["Negative"]:
        neg_count += len(re.findall(rf'\b{re.escape(word)}\b', line_lower))

    # classify line
    if pos_count > 0 and neg_count == 0:
        sentiment = Sentiment.Positive
    elif neg_count > 0 and pos_count == 0:
        sentiment = Sentiment.Negative
    elif pos_count > 0 and neg_count > 0:
        sentiment = Sentiment.Mixed
    else:
        sentiment = Sentiment.Neutral

    return sentiment

def compute_summary(file_path: Path,
                     sentiments: dict[set[str], set[str]]) -> dict[str, int]:
    """
    Analyze the provided document and return a summary of sentiment counts.
    """
    logger.debug(f"Using dataset: {file_path}")
    logger.debug(f"Positive Words: {sentiments['Positive']}")
    logger.debug(f"Negative Words: {sentiments['Negative']}")

    data_lines = read_data(file_path)
    totals = {
        "Positive": 0,
        "Negative": 0,
        "Mixed": 0,
        "Neutral": 0
    }

    # classify each line in the document and aggregate results
    for line in data_lines:
        sentiment = map_post(line=line, sentiments=sentiments)
        logger.debug(f"Line: '{line}'\nSentiment: {sentiment.name}")
        if sentiment == Sentiment.Positive:
            totals["Positive"] += 1
        elif sentiment == Sentiment.Negative:
            totals["Negative"] += 1
        elif sentiment == Sentiment.Mixed:
            totals["Mixed"] += 1
        elif sentiment == Sentiment.Neutral:
            totals["Neutral"] += 1
    
    # return aggregate results
    return totals

def print_document_summary(totals: dict) -> None:
    """
    Print document sentiment summary and the total verdict of the document.
    """
    # Print summary in required format
    print("Document Summary:")
    print(f"Positive = {totals['Positive']}, "
          f"Negative = {totals['Negative']}, "
          f"Mixed = {totals['Mixed']}, "
          f"Neutral = {totals['Neutral']} ")
    
    # Determine verdict
    if totals["Positive"] > totals["Negative"]:
        verdict = "Happier"
    elif totals["Negative"] > totals["Positive"]:
        verdict = "Sadder"
    else:
        verdict = "Tied"

    print(f"Document Verdict: {verdict}")

def generate_bar_chart(totals: dict, file_path: Path) -> None:
    """Generate an *optional* bar chart."""

    labels = list(totals.keys())
    values = [totals[k] for k in labels]
    plt.bar(labels, values, color=["green", "red", "orange", "gray"])
    plt.title(f"Sentiment Analysis: {file_path.name}")
    plt.ylabel("Count")
    plt.show()

def main() -> None:
    sentiment_dict = {
        "Positive": set(["happy", "excited", "thrilled", "love"]),
        "Negative": set(["sad", "depressed", "angry", "upset"])
    }

    args = get_args()

    summary = compute_summary(file_path=args.filepath, 
                                   sentiments=sentiment_dict)
    
    print_document_summary(summary)

    if not args.no_chart:
        generate_bar_chart(summary, args.filepath)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    main()    
    