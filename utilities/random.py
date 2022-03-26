import random
import string


def generate_random_string() -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(15))


def generate_random_int() -> int:
    return random.randrange(999999999)
