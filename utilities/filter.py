import string
from typing import List

default_censor: List[str] = ["@everyone", "@here"]


def filter_words(original_message: str, censored_words: List[str] = None) -> str:
    if censored_words is None:
        censored_words = default_censor
    censored_message: str = original_message
    for censor in censored_words:
        censored_message = censored_message.replace(censor, "#" * len(censor))
    return censored_message
