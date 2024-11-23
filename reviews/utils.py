import string
import random


def slug_generator():
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
