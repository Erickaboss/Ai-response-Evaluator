"""
examples.py
Two example prompt/response pairs for demonstrating the evaluator.
Example 1 is a high-quality response; Example 2 is a weak one.
"""

EXAMPLES = [
    {
        "prompt": "Explain what a Python decorator is and how to use it.",
        "response": (
            "A Python decorator is a function that wraps another function to extend or modify "
            "its behavior without changing its source code. Decorators are widely used for "
            "logging, authentication, and caching.\n\n"
            "They work because functions in Python are first-class objects, which means they "
            "can be passed as arguments. A decorator takes a function, adds some behavior, "
            "and returns a new function. This means you can reuse the same logic across many "
            "functions without repeating yourself.\n\n"
            "For example, here is a simple decorator that logs when a function is called:\n\n"
            "```python\n"
            "def log_call(func):\n"
            "    def wrapper(*args, **kwargs):\n"
            "        print(f'Calling {func.__name__}')\n"
            "        return func(*args, **kwargs)\n"
            "    return wrapper\n\n"
            "@log_call\n"
            "def greet(name):\n"
            "    print(f'Hello, {name}')\n\n"
            "greet('Alice')  # prints: Calling greet, then Hello, Alice\n"
            "```\n\n"
            "The @log_call syntax is just shorthand for greet = log_call(greet). "
            "Since the wrapper returns the result of the original function, the decorated "
            "function behaves normally while gaining the extra logging behavior."
        ),
    },
    {
        "prompt": "Explain what a Python decorator is and how to use it.",
        "response": (
            "A decorator is something you put above a function with the @ symbol. "
            "It changes what the function does. You can use it for many things. "
            "It is a useful feature in Python."
        ),
    },
]
