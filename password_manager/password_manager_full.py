#!/usr/bin/env python3
"""
Collect, encrypt/decript, store and view service data with passwords.
Version 1.2

"""
import pathlib
import getpass
import bcrypt
import base64
import pickle
import pyperclip


def main():
    """Run main program."""
    print('Welcome to Password Manager!')
    print('----------------------------')
    print()

    # 1. Set default dir for data.
    pwd = set_data_dir()
    print(f'Your working directory is: {pwd}')
    print()

    # 2. Hash and store (if not exists) user's master password and check it.
    passed = True
    attempts = 1

    if check_password():
        print()
        print('Let\'s check your master password.')
        passed = validate_hash(load_hash())
    else:
        equal = False
        while not equal:
            print('You should define your master password.')
            store_hash(hash_password())
            print('Well, let\'s check your master password.')
            equal = validate_hash(load_hash())

            if equal:
                print('Your passwords match!')
            else:
                print('Your passwords do not match!')

    while not passed and attempts <= 3:
        print('Something\'s wrong with your input.')
        print(f'Re-enter right password, attempt # {attempts} of 3.')
        passed = validate_hash(load_hash())
        attempts += 1

    if passed:
        print('OK, your master password has been successfully validated.')

        # 3. Check if database of services exists, creates dicts for others.
        if check_database():
            enc_database = load_database()
            print('Your database of services and passwords was loaded.')
        else:
            enc_database = {}

        # 4. Run main menu.
        show_menu()

        # 5. Get the user's menu from main menu and process it.
        menu_choice = 'V'

        while menu_choice != 'Q':
            print()
            menu_choice = check_menu_choice()

            if menu_choice == 'V':
                if len(enc_database) > 0:
                    dec_database = decrypt_database(enc_database)
                    view_database(dec_database)
                else:
                    print('Your database of services and passwords is empty!')
            elif menu_choice == 'C':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    key = get_service_key(enc_database)
                    dec_database = decrypt_database(enc_database)
                    print(
                        f'Your login: {dec_database[key][0]},',
                        f'your password: {dec_database[key][1]}',
                    )
                    pyperclip.copy(dec_database[key][1])
                    print('Your password was copied to the clipboard!')
            elif menu_choice == 'A':
                proceed = check_proceed_choice()
                if proceed == 'Y':
                    add_service(enc_database)
                    store_database(enc_database)
                elif proceed == 'Q':
                    print('You\'ve canceled a database operation!')
            elif menu_choice == 'G':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    key = get_service_key(enc_database)
                    password = input('\t>>> Enter a new password: ')
                    enc_password = encrypt_password(password)
                    enc_database[key][1] = enc_password
                    dec_database = decrypt_database(enc_database)
                    print(
                        f'Your login: {dec_database[key][0]},',
                        f'your password: {dec_database[key][1]}',
                    )
                    print('Your password was changes!')
                    store_database(enc_database)
                elif len(enc_database) > 0 and proceed == 'Q':
                    print('You\'ve canceled a database operation!')
                elif len(enc_database) == 0:
                    print('Nothing to change, your database is empty!')
            elif menu_choice == 'D':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    key = get_service_key(enc_database)
                    del enc_database[key]
                    print(f'The service \'{key}\' was deleted!')
                    store_database(enc_database)
                elif len(enc_database) > 0 and proceed == 'Q':
                    print('You\'ve canceled a database operation!')
                elif len(enc_database) == 0:
                    print('Nothing to delete, your database is empty!')
            elif menu_choice == 'L':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    enc_database.clear()
                    print('Your database cleared!')
                    store_database(enc_database)
                elif len(enc_database) > 0 and proceed == 'Q':
                    print('You\'ve canceled a database operation!')
                elif len(enc_database) == 0:
                    print('Your database is already empty!')
    else:
        print('Sorry, your master password has not been validated.')

    print()
    print('---------------')
    print('(c) Nobus, 2022')


def show_menu():
    """Print the main menu of the program."""
    print()
    print('\tMenu:')
    print('\t(V)iew all services')
    print('\t(C)opy a password')
    print('\t(A)dd a new service')
    print('\tChan(G)e a password')
    print('\t(D)elete a service')
    print('\tC(L)ear all items')
    print('\t(Q)uit the program')


def set_data_dir():
    """Create (in not exists) and set a directory to store data."""
    home = pathlib.Path.home()
    working_dir = home.joinpath('.password_manager')
    working_dir.mkdir(parents=True, exist_ok=True)
    pwd = pathlib.Path(working_dir)

    return pwd


def check_password():
    """Check if master pasword (data file) exists."""
    path = pathlib.Path('/home/nobus/.password_manager/password.dat')
    return path.exists() and path.is_file()


def check_database():
    """Check if database of services (data file) exists."""
    path = pathlib.Path('/home/nobus/.password_manager/services.dat')
    return path.exists() and path.is_file()


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


def get_menu_choice():
    """Get user's menu_choice from menu's items."""
    try:
        menu_choice = input('\t>>> Enter your choice (V/C/A/G/D/L or Q): ')
        assert menu_choice.upper() in 'VCAGDLQ'
    except (AssertionError, ValueError):
        print('Enter a valid choice!')
        menu_choice = None

    finally:
        return menu_choice


def add_service(enc_database):
    """Add service names, logins and passwords to dict."""
    service = input('\t>>> Enter a service name: ')
    login = input('\t>>> Enter your login (or e-mail): ')
    password = input('\t>>> Enter your password: ')

    enc_database[service] = [login, encrypt_password(password)]


def encrypt_password(password):
    """Encrypt user's password using base64."""
    encoded_password = password.encode('UTF-8')

    return base64.b64encode(encoded_password)


def decrypt_password(enc_password):
    """Decrypt passwords using base64."""
    dec_password = base64.b64decode(enc_password)

    return dec_password.decode('UTF-8')


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

            print(
                f'{index+1}) {key} -', f'login: {data[0]}, password: {data[1]}'
            )
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


def check_menu_choice():
    """Get and check user's menu_choice."""
    menu_choice = get_menu_choice()

    while menu_choice is None:
        menu_choice = get_menu_choice()

    return menu_choice.upper()


def get_proceed_choice():
    """Input user's choice to proceed or cancel an operation."""
    try:
        user_choice = input('\t>>> Enter Y=proceed, Q=cancel: ')
        assert user_choice.upper() in 'YQ'
    except (AssertionError, ValueError):
        print('Enter valid choice (Y or Q).')
        user_choice = None

    finally:
        return user_choice


def check_proceed_choice():
    """Get and check user's procceed or cancel."""
    proceed_choice = get_proceed_choice()

    while proceed_choice is None:
        proceed_choice = get_proceed_choice()

    return proceed_choice.upper()


def get_service_choice(database):
    """Input user's choice to choose a service."""
    try:
        user_choice = int(input('\t>>> Enter your choice (number): '))
        assert user_choice in [number for number in range(1, len(database) + 1)]
    except (AssertionError, ValueError):

        print('Enter valid number of a service.')
        user_choice = None

    finally:
        return user_choice


def check_service_choice(database):
    """Get and check user's menu_choice."""
    service_choice = get_service_choice(database)

    while service_choice is None:
        service_choice = get_service_choice(database)

    return service_choice


def get_service_key(database):
    """Change a service from database."""
    view_services(database)
    list_services = []

    for key in database.keys():
        list_services.append(key)

    service_num = check_service_choice(database)

    return list_services[service_num - 1]


if __name__ == '__main__':
    main()
