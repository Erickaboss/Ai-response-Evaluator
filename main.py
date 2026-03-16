"""
main.py
Entry point for the AI Response Evaluator.
Run directly for interactive mode, or import evaluate() for programmatic use.
"""

from evaluator import (
    score_clarity,
    score_completeness,
    score_reasoning,
    score_examples,
    score_length_readability,
)
from feedback import generate_report


def evaluate(prompt: str, response: str) -> str:
    """
    Run all criteria evaluations and return a formatted report string.
    This function is the core pipeline: score -> collect -> report.
    """
    # Score each criterion and collect results
    results = {
        "Clarity":              score_clarity(response),
        "Completeness":         score_completeness(prompt, response),
        "Reasoning":            score_reasoning(response),
        "Example Usage":        score_examples(response),
        "Length & Readability": score_length_readability(response),
    }

    # Unpack scores and rationales into separate dicts for the report
    scores    = {k: v[0] for k, v in results.items()}
    rationales = {k: v[1] for k, v in results.items()}

    return generate_report(prompt, response, scores, rationales)


def interactive_mode():
    """Prompt the user to enter a prompt and response, then print the report."""
    print("\n=== AI Response Evaluator ===")
    print("Enter the user prompt (press Enter twice when done):")
    prompt_lines = []
    while True:
        line = input()
        if line == "":
            break
        prompt_lines.append(line)
    prompt = " ".join(prompt_lines)

    print("\nEnter the model response (press Enter twice when done):")
    response_lines = []
    while True:
        line = input()
        if line == "":
            break
        response_lines.append(line)
    response = " ".join(response_lines)

    report = evaluate(prompt, response)
    print(report)


def run_examples():
    """Load and evaluate the built-in examples from examples.py."""
    from examples import EXAMPLES
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"\n{'#'*60}")
        print(f"  EXAMPLE {i}")
        print(f"{'#'*60}")
        report = evaluate(ex["prompt"], ex["response"])
        print(report)


if __name__ == "__main__":
    import sys
    # Pass --examples flag to run built-in examples instead of interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--examples":
        run_examples()
    else:
        interactive_mode()
