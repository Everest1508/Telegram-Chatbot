from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def summary(string):
    # Input paragraph
    parser = PlaintextParser.from_string(string, Tokenizer("english"))

    # Initialize the LexRank summarizer
    summarizer = LexRankSummarizer()

    # Specify the number of sentences in the summary
    summary_size = 2

    # Generate the summary
    summary = summarizer(parser.document, summary_size)
    sentences = ""
    # Print the summarized sentences
    for sentence in summary:
        sentence+=sentence

    return sentences