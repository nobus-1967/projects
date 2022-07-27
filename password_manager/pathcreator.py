#!/usr/bin/env python3
"""Create and set a directory to store service data, check if data exists."""
import pathlib


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
