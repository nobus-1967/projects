#!/usr/bin/env python3
"""Using custom editable prompt."""
from prompt_toolkit import prompt
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import ANSI

from mdprinter import print_md

COMMANDS: list[str] = [
    'help',
    '-h',
    'view',
    '-v',
    'view-recent',
    '-vr',
    'view-last',
    '-vl',
    'view-all',
    '-va',
    'count',
    '-c',
    'add',
    '-a',
    'edit',
    '-e',
    'edit-title',
    '-et',
    'edit-text',
    '-ex',
    'edit-tag',
    '-eg',
    'del',
    '-d',
    'del-memo',
    '-dm',
    'del-all',
    '-da',
    'search',
    '-s',
    'search-id',
    '-si',
    'search-date',
    '-sd',
    'search-title',
    '-st',
    'search-text',
    '-sx',
    'search-tag',
    '-sg',
    'howto',
    '-w',
    'howto-md',
    '-wm',
    'howto-hotkeys',
    '-wk',
    'backup',
    '-b',
    'backup-db',
    '-bd',
    'restore-db',
    '-od',
    'check-db',
    '-kd',
    'recreate-db',
    '-ed',
    'quit',
    '-q',
]
CONFIRMATIONS: list[str] = ['yes', '-y', 'no', '-n']


def get_command() -> str:
    """Input user's command."""
    command_completer: WordCompleter = WordCompleter(COMMANDS)

    command: str = prompt(
        ANSI('\033[34;1mmemopad\033[0m ' '\033[31;1m>>>\033[0m '),
        completer=command_completer,
    )

    return command


def check_command() -> str:
    """Check user's command."""
    command: str = get_command().strip().lower()

    while command not in COMMANDS:
        print_md('Такой команды нет, обратитесь к `help`!')
        command = get_command().strip()

    return command


def confirm_command() -> str:
    """Confirm or cancel operations with database."""
    confirm_completer: WordCompleter = WordCompleter(CONFIRMATIONS)

    command: str = prompt(
        ANSI(
            '\033[31;1m(\033[0m'
            '\033[34;1myes\033[0m'
            '\033[32;1m/\033[0m'
            '\033[34;1mno\033[0m'
            '\033[31;1m)\033[0m '
        ),
        completer=confirm_completer,
    )

    return command


def check_confirmation() -> str:
    """Check user's command."""
    confirmation: str = confirm_command().strip().lower()

    while confirmation not in CONFIRMATIONS:
        print_md('Неправильный ввод, введите `yes` или `no`!')
        confirmation = confirm_command().strip()

    return confirmation


def get_rowid() -> int:
    """Input user's choice to choose memo's ROWID."""
    try:
        print_md('Введите `ID` заметки:')
        rowid: int = int(
            prompt(
                ANSI(
                    '\033[31;1m(\033[0m'
                    '\033[34;1mID\033[0m'
                    '\033[31;1m)\033[0m '
                )
            )
        )
        assert rowid > 0

    except (AssertionError, ValueError):
        rowid = 0

        return rowid
    else:
        return rowid


def get_new_title() -> str:
    """Prompt to enter title for new memo."""
    new_title: str = prompt(ANSI('\033[32;1m##\033[0m '))

    return new_title


def get_new_text() -> str:
    """Prompt to enter text of body for new memo."""
    new_text: str = prompt('', multiline=True)

    return new_text


def get_new_tag() -> str:
    """Prompt to enter tag for new memo."""
    new_tag: str = prompt(ANSI('\033[32;1m#\033[0m'))

    return new_tag


def get_title_to_edit() -> str:
    """Prompt to enter title to edit or replace."""
    title_to_edit: str = prompt(
        ANSI('\033[32;1m##\033[0m '), clipboard=PyperclipClipboard()
    )

    return title_to_edit


def get_text_to_edit() -> str:
    """Prompt to enter text of body to edit or replace."""
    text_to_edit: str = prompt(
        '', multiline=True, clipboard=PyperclipClipboard()
    )

    return text_to_edit


def get_tag_to_edit() -> str:
    """Prompt to enter tag to edit or replace."""
    tag_to_edit: str = prompt(
        ANSI('\033[32;1m#\033[0m'), clipboard=PyperclipClipboard()
    )

    return tag_to_edit


def get_date_to_search() -> str:
    """Prompt to enter memo's date to search."""
    date_to_search: str = prompt(
        ANSI(
            '\033[31;1m(\033[0m'
            '\033[34;1mГГГГ\033[0m'
            '\033[32;1m-\033[0m'
            '\033[34;1mММ\033[0m'
            '\033[32;1m-\033[0m'
            '\033[34;1mДД\033[0m'
            '\033[31;1m)\033[0m '
        )
    )

    return date_to_search


def get_title_to_search() -> str:
    """Prompt to enter memo's title to search."""
    title_to_search: str = prompt(
        ANSI(
            '\033[31;1m(\033[0m'
            '\033[32;1m##\033[0m '
            '\033[34;1mЗаголовок\033[0m'
            '\033[31;1m)\033[0m '
        )
    )

    return title_to_search


def get_text_to_search() -> str:
    """Prompt to enter text in memo's body to search."""
    text_to_search: str = prompt(
        ANSI(
            '\033[31;1m(\033[0m' '\033[34;1mТекст\033[0m' '\033[31;1m)\033[0m '
        )
    )

    return text_to_search


def get_tag_to_search() -> str:
    """Prompt to enter memo's tag to search."""
    tag_to_search: str = prompt(
        ANSI(
            '\033[31;1m(\033[0m'
            '\033[32;1m#\033[0m'
            '\033[34;1mtag\033[0m'
            '\033[31;1m)\033[0m '
        )
    )

    return tag_to_search
