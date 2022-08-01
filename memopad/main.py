#!/usr/bin/env python3
"""MemoPad - CLI program using SQLite to store memos."""
from pathlib import Path

from prompt_toolkit.shortcuts import set_title

from commandshelp import COMMANDS
from dbmanager import set_db_path, backup_db, remove_db, restore_db
from howtokeys import HOTKEYS
from howtomd import MARKDOWN
from mdprinter import print_new_memo, print_md
from memoeditor import create_new_memo
from messages import HOWTO, VIEW, EDIT, DEL, SEARCH, BACKUP
from messages import TITLE, INFO, COPYRIGHT
from prompter import check_command
from sqlconnector import add_memo, delete_memo, delete_all
from sqlconnector import check_db_integrity, check_db_path_and_table
from sqlconnector import create_db
from sqlconnector import edit_title, edit_body, edit_tag
from sqlconnector import search_memo_by_rowid, search_memo_by_date
from sqlconnector import search_memo_by_tag
from sqlconnector import search_memo_by_title, search_memo_by_text
from sqlconnector import show_recent, show_last, show_all, show_total_memos


def main() -> None:
    """Memopad - CLI program using SQLite to store memos."""
    set_title("MemoPad")

    print_md(TITLE)
    print_md(INFO)

    path: Path = set_db_path()
    check_db_path_and_table(path)

    command: str = check_command()

    while command not in ['quit', '-q']:
        if command in ['help', '-h']:
            print_md(COMMANDS)
        elif command in ['howto', '-w']:
            print_md(HOWTO)
        elif command in ['howto-md', '-wm']:
            print_md(MARKDOWN)
        elif command in ['howto-hotkeys', '-wk']:
            print_md(HOTKEYS)
        elif command in ['view', '-v']:
            print_md(VIEW)
        elif command in ['view-recent', '-vr']:
            show_recent(path)
        elif command in ['view-last', '-vl']:
            show_last(path)
        elif command in ['view-all', '-va']:
            show_all(path)
        elif command in ['count', '-c']:
            show_total_memos(path)
        elif command in ['add', '-a']:
            memo = create_new_memo()
            print_new_memo(memo)
            add_memo(path, memo)
        elif command in ['edit', '-e']:
            print_md(EDIT)
        elif command in ['edit-title', '-et']:
            edit_title(path)
        elif command in ['edit-text', '-ex']:
            edit_body(path)
        elif command in ['edit-tag', '-eg']:
            edit_tag(path)
        elif command in ['del', '-d']:
            print_md(DEL)
        elif command in ['del-memo', '-dm']:
            delete_memo(path)
        elif command in ['del-all', '-da']:
            delete_all(path)
        elif command in ['search', '-s']:
            print_md(SEARCH)
        elif command in ['search-id', '-si']:
            search_memo_by_rowid(path)
        elif command in ['search-date', '-sd']:
            search_memo_by_date(path)
        elif command in ['search-title', '-st']:
            search_memo_by_title(path)
        elif command in ['search-text', '-sx']:
            search_memo_by_text(path)
        elif command in ['search-tag', '-sg']:
            search_memo_by_tag(path)
        elif command in ['backup', '-b']:
            print_md(BACKUP)
        elif command in ['backup-db', '-bd']:
            backup_db(path)
        elif command in ['restore-db', '-od']:
            restore_db(path)
        elif command in ['check-db', '-kd']:
            check_db_integrity(path)
        elif command in ['recreate-db', '-ed']:
            remove_db(path)
            create_db(path)

        command = check_command()

    backup_db(path)
    print_md(COPYRIGHT)


if __name__ == '__main__':
    main()
