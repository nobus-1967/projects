#!/usr/bin/env python3
"""Hash, store and validate user's master password."""
import getpass
import bcrypt
import pickle


def hash_password():
    """Secure input and encode master password."""
    password = getpass.getpass('\t>>> Enter your master password: ')
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def store_hash(hashed_password):
    """Save encrypted master password to file."""
    with open('/home/nobus/.password_manager/password.dat', 'wb') as file:
        pickle.dump(hashed_password, file)


def load_hash():
    """Load and read encrypted master password from file."""
    with open('/home/nobus/.password_manager/password.dat', 'rb') as file:
        return pickle.load(file)


def validate_hash(restored_hashed_password):
    """Validate encrypted password."""
    password = getpass.getpass('\t>>> Enter your master password: ')
    return bcrypt.checkpw(password.encode(), restored_hashed_password)
