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
    POSITIVE = auto()
    NEGATIVE = auto()
    MIXED = auto()
    NEUTRAL = auto()

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

def analyze_line(line: str,
                 sentiments: dict[set[str], set[str]]) -> Sentiment:
    """
    Counts the number of POS and NEG words in the line using regular
    expressions.
    Returns a 'Sentiment' enum.
    """
    pos_count = 0
    neg_count = 0
    
    # tokenizing words using regex
    line_lower = line.lower()
    for word in sentiments["positive"]:
        pos_count += len(re.findall(rf'\b{re.escape(word)}\b', line_lower))
    for word in sentiments["negative"]:
        neg_count += len(re.findall(rf'\b{re.escape(word)}\b', line_lower))

    # classify line
    if pos_count > 0 and neg_count == 0:
        sentiment = Sentiment.POSITIVE
    elif neg_count > 0 and pos_count == 0:
        sentiment = Sentiment.NEGATIVE
    elif pos_count > 0 and neg_count > 0:
        sentiment = Sentiment.MIXED
    else:
        sentiment = Sentiment.NEUTRAL

    return sentiment

def analyze_document(file_path: Path,
                     sentiments: dict[set[str], set[str]]) -> dict[str, int]:
    """
    Analyze the provided document and return a summary of sentiment counts.
    """
    logger.debug(f"Using dataset: {file_path}")
    logger.debug(f"Positive Words: {sentiments['positive']}")
    logger.debug(f"Negative Words: {sentiments['negative']}")

    data_lines = read_data(file_path)
    doc_summary = {
        "positive": 0,
        "negative": 0,
        "mixed": 0,
        "neutral": 0
    }

    # classify each line in the document and aggregate results
    for line in data_lines:
        sentiment = analyze_line(line=line, sentiments=sentiments)
        logger.debug(f"Line: '{line}'\nSentiment: {sentiment.name}")
        if sentiment == Sentiment.POSITIVE:
            doc_summary["positive"] += 1
        elif sentiment == Sentiment.NEGATIVE:
            doc_summary["negative"] += 1
        elif sentiment == Sentiment.MIXED:
            doc_summary["mixed"] += 1
        elif sentiment == Sentiment.NEUTRAL:
            doc_summary["neutral"] += 1
    
    # return aggregate results
    return doc_summary

def print_document_summary(doc_summary: dict) -> None:
    """
    Print document sentiment summary and the total verdict of the document.
    """
    # Print summary in required format
    print("Document Summary:")
    print(f"Positive = {doc_summary['positive']}, "
          f"Negative = {doc_summary['negative']}, "
          f"Mixed = {doc_summary['mixed']}, "
          f"Neutral = {doc_summary['neutral']} ")
    
    # Determine verdict
    if doc_summary["positive"] > doc_summary["negative"]:
        verdict = "Happier"
    elif doc_summary["negative"] > doc_summary["positive"]:
        verdict = "Sadder"
    else:
        verdict = "Tied"

    print(f"Document Verdict: {verdict}")

def generate_bar_chart(doc_summary: dict, file_path: Path) -> None:
    """Generate an *optional* bar chart."""

    categories = ["Positive", "Negative", "Mixed", "Neutral"]
    values = [doc_summary["positive"],
              doc_summary["negative"],
              doc_summary["mixed"],
              doc_summary["neutral"]]
    plt.bar(categories, values, color=["green", "red", "orange", "gray"])
    plt.title(f"Sentiment Analysis: {file_path.name}")
    plt.ylabel("Count")
    plt.show()

def main() -> None:
    sentiment_dict = {
        "positive": set(["happy", "excited", "thrilled", "love"]),
        "negative": set(["sad", "depressed", "angry", "upset"])
    }

    args = get_args()

    doc_summary = analyze_document(file_path=args.filepath, 
                                   sentiments=sentiment_dict)
    
    print_document_summary(doc_summary)

    if not args.no_chart:
        generate_bar_chart(doc_summary, args.filepath)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    main()    
    