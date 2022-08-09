#!/usr/bin/env python3
"""
Collect, encrypt/decrypt, store and view service data with passwords.
Version 1.2

"""
import pyperclip

import pathcreator
import keyvalidator
import dataencryptor


def main():
    """Run main program."""
    print('Welcome to Password Manager!')
    print('----------------------------')
    print()

    # 1. Set default dir for data.
    pwd = pathcreator.set_data_dir()
    print(f'Your working directory is: {pwd}')
    print()

    # 2. Hash and store (if not exists) user's master password and check it.
    passed = True
    attempts = 1

    if pathcreator.check_password():
        print()
        print('Let\'s check your master password.')
        passed = keyvalidator.validate_hash(keyvalidator.load_hash())
    else:
        equal = False
        while not equal:
            print('You should define your master password.')
            keyvalidator.store_hash(keyvalidator.hash_password())
            print('Well, let\'s check your master password.')
            equal = keyvalidator.validate_hash(keyvalidator.load_hash())

            if equal:
                print('Your passwords match!')
            else:
                print('Your passwords do not match!')

    while not passed and attempts <= 3:
        print('Something\'s wrong with your input.')
        print(f'Re-enter right password, attempt # {attempts} of 3.')
        passed = keyvalidator.validate_hash(keyvalidator.load_hash())
        attempts += 1

    if passed:
        print('OK, your master password has been successfully validated.')

        # 3. Check if database of services exists, creates dicts for others.
        if pathcreator.check_database():
            enc_database = dataencryptor.load_database()
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
                    dec_database = dataencryptor.decrypt_database(enc_database)
                    dataencryptor.view_database(dec_database)
                else:
                    print('Your database of services and passwords is empty!')
            elif menu_choice == 'C':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    key = get_service_key(enc_database)
                    dec_database = dataencryptor.decrypt_database(enc_database)
                    print(
                        f'Your login: {dec_database[key][0]},',
                        f'your password: {dec_database[key][1]}',
                    )
                    pyperclip.copy(dec_database[key][1])
                    print('Your password was copied to the clipboard!')
            elif menu_choice == 'A':
                proceed = check_proceed_choice()
                if proceed == 'Y':
                    dataencryptor.add_service(enc_database)
                    dataencryptor.store_database(enc_database)
                elif proceed == 'Q':
                    print('You\'ve canceled a database operation!')
            elif menu_choice == 'G':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    key = get_service_key(enc_database)
                    password = input('\t>>> Enter a new password: ')
                    enc_password = dataencryptor.encrypt_password(password)
                    enc_database[key][1] = enc_password
                    dec_database = dataencryptor.decrypt_database(enc_database)
                    print(
                        f'Your login: {dec_database[key][0]},',
                        f'your password: {dec_database[key][1]}',
                    )
                    print('Your password was changes!')
                    dataencryptor.store_database(enc_database)
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
                    dataencryptor.store_database(enc_database)
                elif len(enc_database) > 0 and proceed == 'Q':
                    print('You\'ve canceled a database operation!')
                elif len(enc_database) == 0:
                    print('Nothing to delete, your database is empty!')
            elif menu_choice == 'L':
                proceed = check_proceed_choice()
                if len(enc_database) > 0 and proceed == 'Y':
                    enc_database.clear()
                    print('Your database cleared!')
                    dataencryptor.store_database(enc_database)
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


def get_menu_choice():
    """Get user's menu_choice from menu's items."""
    try:

        menu_choice = input('\t>>> Enter your choice (V/C/A/G/D/L or Q): ')
        assert menu_choice.upper() in 'VCAGDLQ'
    except (AssertionError, ValueError):
        print('Enter a valid choice!')
        return None

    else:
        return menu_choice


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
        return None

    else:
        return user_choice


def check_proceed_choice():
    """Get and check user's proceed or cancel."""
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
        return None

    else:
        return user_choice


def check_service_choice(database):
    """Get and check user's menu_choice."""
    service_choice = get_service_choice(database)

    while service_choice is None:
        service_choice = get_service_choice(database)

    return service_choice


def get_service_key(database):
    """Change a service from database."""
    dataencryptor.view_services(database)
    list_services = []

    for key in database.keys():
        list_services.append(key)

    service_num = check_service_choice(database)

    return list_services[service_num - 1]


if __name__ == '__main__':
    main()
