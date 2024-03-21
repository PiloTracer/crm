'''Helper for api endpoints'''
import random
import secrets
import string


def generate_secret_word(length=10):
    '''Generate an 10-leter secret word'''
    # Ensure the length is a positive integer
    if length < 1:
        raise ValueError("Length must be a positive integer")

    # Generate a random word using letters
    letters = string.ascii_lowercase  # You can also include uppercase if needed
    secret_word = ''.join(random.choice(letters) for _ in range(length))
    return secret_word


def generate_api_key(length=32):
    '''generate an api key'''
    # Ensure the length is a positive integer
    if length < 1:
        raise ValueError("Length must be a positive integer")

    characters = string.ascii_letters + string.digits
    # Optionally, you can include special characters
    # characters += string.punctuation

    api_key = ''.join(secrets.choice(characters) for _ in range(length))
    return api_key
