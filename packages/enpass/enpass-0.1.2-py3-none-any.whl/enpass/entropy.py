import math
from .base import calc_base

def calc_entropy(password):
    """
    Calculates the entropy of a password in bits.
    Password entropy equation = log2(B^L)
        B -> Base
        L -> Length
    """
    base = calc_base(password)
    length = len(password)

    return round(math.log2(base**length), 2)


def validate(entropy, min_entropy=60.0):
    """
    Checks if the password's entropy meets the specified minimum requirement.

    Passwords should ideally be > 60.
    Great Passwords should be between 70-90.
    """
    return entropy >= min_entropy

#Estimates the time it would take to brute-force a password with the given entropy.
def estimate_bruteforce_time(entropy, guesses_per_second):
    """
    This code assumes that cracking time scales linearly with the number of possible combinations.

    While this might hold for straightforward brute-force attacks, more sophisticated attacks,
    such as dictionary attacks or those exploiting weaknesses in password hashing algorithms, may have different time complexities.
    """
    combinations = 2**entropy
    seconds_to_crack = combinations / guesses_per_second

    units = [("year", 60*60*24*365), ("day", 60*60*24), ("hour", 60*60), ("minute", 60), ("second", 1)]
    for unit, value in units:
        if seconds_to_crack >= value:
            amount = seconds_to_crack // value
            return f"{amount:.2f} {unit}{'s' if amount > 1 else ''}"
    return "Less than 1 second"
