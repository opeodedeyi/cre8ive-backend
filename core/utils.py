import random
import string

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6
SECOND_STRING_LENGTH = 15

def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


def generate_user_string(chars=ALPHANUMERIC_CHARS, length=SECOND_STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))