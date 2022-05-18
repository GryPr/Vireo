import random


def generate_random_int(*, limit: int) -> int:
    """Generate and return a random int up to (and NOT including) a specified limit."""
    return random.randrange(limit)
