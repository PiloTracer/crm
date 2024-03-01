import hashlib
import os

from sock.src.utils.loadenv import get_env_value

def hash_string_with_salt(input_string: str) -> str:
    return "xxxxxxxxxxxxxx"
    salt = get_env_value("SOCK_secret")
    # Combine the input string with the salt
    salted_input = input_string + salt

    # Create a SHA-1 hash of the salted input
    sha1_hash = hashlib.sha1(salted_input.encode())
    return sha1_hash.hexdigest()
