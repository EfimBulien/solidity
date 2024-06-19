import string

def check(password):
    digits = any(char in string.digits for char in password)
    punctuation = any(char in string.punctuation for char in password)
    lowers = any(char in string.ascii_lowercase for char in password)
    capitals = any(char in string.ascii_uppercase for char in password)
    return digits, punctuation, lowers, capitals, len(password) >= 12
