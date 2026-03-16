"""
evaluator.py
Handles scoring logic for each evaluation criterion.
Each function returns a score (1-10) and a short rationale.
"""


def score_clarity(response: str) -> tuple[int, str]:
    """
    Clarity: Is the response easy to understand?
    Heuristics: sentence length, use of jargon, structure.
    """
    sentences = [s.strip() for s in response.split('.') if s.strip()]
    avg_len = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)

    if avg_len <= 15:
        return 9, "Sentences are concise and easy to follow."
    elif avg_len <= 25:
        return 7, "Sentences are moderately clear but could be tightened."
    else:
        return 4, "Sentences are long and may be hard to follow."


def score_completeness(prompt: str, response: str) -> tuple[int, str]:
    """
    Completeness: Does the response address the prompt fully?
    Heuristic: keyword overlap between prompt and response.
    """
    prompt_words = set(prompt.lower().split())
    response_words = set(response.lower().split())
    # Remove common stop words for a cleaner signal
    stop_words = {'the', 'a', 'an', 'is', 'in', 'on', 'at', 'to', 'and', 'or', 'of', 'it', 'for'}
    prompt_keywords = prompt_words - stop_words
    overlap = len(prompt_keywords & response_words) / max(len(prompt_keywords), 1)

    if overlap >= 0.6:
        return 9, "Response addresses most key topics from the prompt."
    elif overlap >= 0.3:
        return 6, "Response partially addresses the prompt; some topics may be missing."
    else:
        return 3, "Response seems to miss several key points from the prompt."


def score_reasoning(response: str) -> tuple[int, str]:
    """
    Reasoning: Does the response explain the 'why' or 'how'?
    Heuristic: presence of reasoning signal words.
    """
    reasoning_signals = ['because', 'therefore', 'since', 'as a result',
                         'this means', 'which means', 'due to', 'thus', 'hence', 'so that']
    found = [w for w in reasoning_signals if w in response.lower()]

    if len(found) >= 3:
        return 9, f"Strong reasoning present. Signals found: {', '.join(found)}."
    elif len(found) >= 1:
        return 6, f"Some reasoning present ({', '.join(found)}), but could go deeper."
    else:
        return 3, "Little to no reasoning or explanation detected."


def score_examples(response: str) -> tuple[int, str]:
    """
    Example usage: Does the response include concrete examples?
    Heuristic: presence of example signal phrases or code blocks.
    """
    example_signals = ['for example', 'e.g.', 'such as', 'for instance',
                       'like ', 'consider ', '```', 'sample', 'illustration']
    found = [w for w in example_signals if w in response.lower()]

    if len(found) >= 2:
        return 9, "Response includes clear examples to illustrate the point."
    elif len(found) == 1:
        return 6, "At least one example present, but more would strengthen the response."
    else:
        return 3, "No concrete examples found. Adding examples would improve understanding."


def score_length_readability(response: str) -> tuple[int, str]:
    """
    Length and readability: Is the response an appropriate length?
    Heuristic: word count range and paragraph structure.
    """
    words = len(response.split())
    paragraphs = [p.strip() for p in response.split('\n\n') if p.strip()]

    if 80 <= words <= 400 and len(paragraphs) >= 2:
        return 9, f"Well-structured response ({words} words, {len(paragraphs)} paragraphs)."
    elif 50 <= words <= 600:
        return 6, f"Acceptable length ({words} words), but structure could be improved."
    elif words < 50:
        return 3, f"Response is too short ({words} words) to be thorough."
    else:
        return 4, f"Response may be too long ({words} words); consider trimming."
