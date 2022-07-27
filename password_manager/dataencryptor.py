#!/usr/bin/env python3
"""Enter services data, encrypt/decrypt passwords, store and view databases."""
import getpass
import base64
import pickle


def add_service(enc_database):
    """Add service names, logins and passwords to dict."""
    service = input('\t>>> Enter a service name: ')
    login = input('\t>>> Enter your login (or e-mail): ')
    password = input('\t>>> Enter your password: ')

    enc_database[service] = [login, encrypt_password(password)]


def encrypt_password(password):
    """Encrypt user's password using base64."""
    bin_password = bytes(password, 'utf-8')

    return base64.b64encode(bin_password)


def decrypt_password(enc_password):
    """Decrypt passwords using base64."""
    bin_password = base64.b64decode(enc_password)

    return str(bin_password).lstrip('b').strip('\'')


def decrypt_database(enc_database):
    """View service names, logins and passwords from dict."""
    dec_database = {}

    for key in enc_database:
        data = enc_database.get(key)

        dec_database[key] = [data[0], decrypt_password(data[1])]

    return dec_database


def view_database(database):
    """View data (service names, logins and passwords) from dict."""
    if len(database) > 0:
        for index, key in enumerate(database.keys()):
            data = database.get(key)

            print(f'{index+1}) {key} -',
                  f'login: {data[0]}, password: {data[1]}')
    else:
        print('Your database is empty.')


def view_services(database):
    """View all services (service names as keys of dict)."""
    if len(database) > 0:
        print('Stored services:')

        for index, key in enumerate(database.keys()):
            print(f'{index+1}: {key}')
    else:
        ('Stored services not found!')


def store_database(enc_database):
    """Save dict (services, logins, encrypted passwords) to file."""
    with open('/home/nobus/.password_manager/services.dat', 'wb') as file:
        pickle.dump(enc_database, file)


def load_database():
    """Load and read dict (services, logins, encrypted passwords) from file."""
    with open('/home/nobus/.password_manager/services.dat', 'rb') as file:
        return pickle.load(file)
