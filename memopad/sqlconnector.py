"""Connect to database; insert, select, edit and delete data; search data."""
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, DatabaseError

from pyperclip import copy as copy_to_clipboard
from sqlite_icu import extension_path

from dbmanager import check_db, check_backup, set_backup_path, restore_db
from mdprinter import print_memo_from_db, print_md, print_total
from memoeditor import input_corrected_body
from memoeditor import input_corrected_title, input_corrected_tag
from prompter import check_confirmation, get_rowid
from prompter import get_date_to_search, get_title_to_search
from prompter import get_text_to_search, get_tag_to_search


def check_db_path_and_table(path: Path) -> None:
    """Check database path and create database if not exists."""
    is_db: bool = check_db(path)

    if is_db:
        print_md(f'Существующая база заметок: `{path}`.')
    else:
        is_backup: bool = check_backup(path)

        if is_backup:
            path_backup: Path = set_backup_path(path)

            print_md(f'База заметок `{path}` не найдена!')
            print_md(
                'Восстановить базу заметок из резервной копии '
                + f'`{path_backup}`?'
            )
            confirmation: str = check_confirmation()

            if confirmation == 'yes':
                restore_db(path)
        else:
            create_db(path)


def create_db(path: Path) -> None:
    """Create empty database for memos if not exists."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_create_table: str = '''CREATE TABLE IF NOT EXISTS memos
                               (
                               date_time DATETIME NOT NULL,
                               titles TEXT NOT NULL,
                               bodies TEXT NOT NULL,
                               tags TEXT NOT NULL
                               );'''

    try:
        print_md(f'Будет создана новая база заметок: `{path}`.')
        cursor.execute(sql_create_table)
        connection.commit()

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def show_recent(path: Path) -> None:
    """Show the latest memo."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_latest: str = '''SELECT ROWID, date_time, titles, bodies, tags
                                FROM memos
                                ORDER BY ROWID DESC;'''

    try:
        cursor.execute(sql_select_latest)
        memo: tuple | None = cursor.fetchone()

        if memo:
            print_md('Последняя заметка:')
            print_memo_from_db(memo)
        else:
            print_md('Заметка в базе не найдена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def show_last(path: Path) -> None:
    """Show last 5 memos."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_last: str = '''SELECT ROWID, date_time, titles, bodies, tags
                              FROM memos
                              ORDER BY ROWID DESC;'''

    try:
        cursor.execute(sql_select_last)
        memos: list | None = cursor.fetchmany(5)

        if memos:
            print_md('Последние заметки:')
            for memo in memos:
                print_memo_from_db(memo)
        else:
            print_md('Заметки в базе не найдены.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def show_all(path: Path) -> None:
    """Show all memos."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_all: str = '''SELECT ROWID, date_time, titles, bodies, tags
                             FROM memos
                             ORDER BY ROWID;'''

    try:
        cursor.execute(sql_select_all)
        memos: list | None = cursor.fetchall()

        if memos:
            print_md('Все заметки из базы (по порядку создания):')
            for memo in memos:
                print_memo_from_db(memo)
        else:
            print_md('Заметки в базе не найдены.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def show_total_memos(path: Path) -> None:
    """Show total of memos in database."""
    total: int = count_memos(path)

    print_total(total)


def add_memo(path: Path, memo: tuple) -> None:
    """Add new memo to database."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_add_memo: str = '''INSERT INTO memos (date_time, titles, bodies, tags)
                           VALUES (?, ?, ?, ?);'''

    try:
        cursor.execute(sql_add_memo, memo)
        connection.commit()
        print_md('Заметка добавлена в базу.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def edit_title(path: Path) -> None:
    """Edit title of existing memo."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_title: str = '''SELECT titles
                               FROM memos
                               WHERE ROWID = ?;'''
    sql_update_title: str = '''UPDATE memos
                               SET date_time = ?, titles = ?
                               WHERE ROWID = ?;'''
    rowid: int | None = search_memo_by_rowid(path)
    total: int = count_memos(path)

    try:
        if rowid is not None and 0 < rowid <= total:
            cursor.execute(sql_select_title, (rowid,))

            memo: tuple | None = cursor.fetchone()
            copy_to_clipboard(memo[0].lstrip('## '))

            updated: tuple = input_corrected_title()
            updated_date_time: str = updated[0]
            corrected_title: str = updated[1]

            print_md('Сохранить заметку с отредактированным заголовком?')
            confirmation: str = check_confirmation()

            if confirmation == 'yes':
                cursor.execute(
                    sql_update_title,
                    (updated_date_time, corrected_title, rowid),
                )
                connection.commit()
                print_md('Заметка обновлена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def edit_body(path: Path) -> None:
    """Edit body of existing memo."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_body: str = '''SELECT bodies
                              FROM memos
                              WHERE ROWID = ?;'''
    sql_update_body: str = '''UPDATE memos
                               SET date_time = ?, bodies = ?
                               WHERE ROWID = ?;'''
    rowid: int | None = search_memo_by_rowid(path)
    total: int = count_memos(path)

    try:
        if rowid is not None and 0 < rowid <= total:
            cursor.execute(sql_select_body, (rowid,))

            memo: tuple | None = cursor.fetchone()
            copy_to_clipboard(memo[0])

            updated: tuple = input_corrected_body()
            updated_date_time: str = updated[0]
            corrected_text: str = updated[1]

            print_md('Сохранить заметку с отредактированным текстом?')
            confirmation: str = check_confirmation()

            if confirmation == 'yes':
                cursor.execute(
                    sql_update_body, (updated_date_time, corrected_text, rowid)
                )
                connection.commit()
                print_md('Заметка обновлена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def edit_tag(path: Path) -> None:
    """Edit tag of existing memo."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_tag: str = '''SELECT tags
                              FROM memos
                              WHERE ROWID = ?;'''
    sql_update_tag: str = '''UPDATE memos
                               SET date_time = ?, tags = ?
                               WHERE ROWID = ?;'''
    rowid: int | None = search_memo_by_rowid(path)
    total: int = count_memos(path)

    try:
        if rowid is not None and 0 < rowid <= total:
            cursor.execute(sql_select_tag, (rowid,))

            memo: tuple | None = cursor.fetchone()
            copy_to_clipboard(memo[0].lstrip('#'))

            updated: tuple = input_corrected_tag()
            updated_date_time: str = updated[0]
            corrected_tag: str = updated[1]

            print_md('Сохранить заметку с отредактированным тегом?')
            confirmation: str = check_confirmation()

            if confirmation == 'yes':
                cursor.execute(
                    sql_update_tag, (updated_date_time, corrected_tag, rowid)
                )
                connection.commit()
                print_md('Заметка обновлена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def delete_memo(path: Path) -> None:
    """Delete memo from database (by ROWID)."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_delete_memo: str = '''DELETE FROM memos
                              WHERE ROWID == ?;'''
    rowid: int | None = search_memo_by_rowid(path)
    total: int = count_memos(path)

    try:
        if rowid is not None and 0 < rowid <= total:
            print_md(f'Удалить заметку с ID `{rowid}`?')
            confirmation: str = check_confirmation()

            if confirmation == 'yes':
                cursor.execute(sql_delete_memo, (rowid,))
                connection.commit()
                print_md('Заметка удалена из базы.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def delete_all(path: Path) -> None:
    """Delete all memos from database."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_delete_all: str = '''DELETE FROM memos;'''

    try:
        print_md('Удалить все заметки из базы?')
        confirmation: str = check_confirmation()

        if confirmation == 'yes':
            cursor.execute(sql_delete_all)
            connection.commit()
            print_md('Все заметки удалены из базы.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def search_memo_by_date(path: Path) -> None:
    """Search memo in database (by date)."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_date: str = '''SELECT ROWID, date_time, titles, bodies, tags
                              FROM memos
                              WHERE DATE(date_time) = ?;'''
    print_md(
        'Введите дату создания (редактирования) заметки '
        + 'в формате `ГГГГ-ММ-ДД`:'
    )
    date: str = get_date_to_search().strip()

    try:
        cursor.execute(sql_select_date, (date,))
        memos: list | None = cursor.fetchall()

        if memos:
            for memo in memos:
                print_memo_from_db(memo)
        else:
            if date == '':
                print_md('Дата не задана, заметка не найдена.')
            else:
                print_md(f'Заметка от `{date}` не найдена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def search_memo_by_title(path: Path) -> None:
    """Search memo in database (by text)."""
    connection: Connection = connect(path)
    connection.enable_load_extension(True)
    connection.load_extension(extension_path().replace('.so', ''))
    cursor: Cursor = connection.cursor()

    sql_select_title: str = '''SELECT ROWID, date_time, titles, bodies, tags
                               FROM memos
                               WHERE lower(titles, "ru_RUS") LIKE ?;'''
    print_md('Введите фрагмент заголовка заметки:')
    title: str = get_title_to_search().strip()

    if title != '':
        title_to_search: str = f'%{title.lower()}%'
    else:
        title_to_search = title

    try:
        cursor.execute(sql_select_title, (title_to_search,))
        memos: list | None = cursor.fetchall()

        if memos:
            for memo in memos:
                print_memo_from_db(memo)
        else:
            if title == '':
                print_md('Заголовок не задан, заметка не найдена.')
            else:
                print_md(f'Заметка с `{title}` в заголовке не найдена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def search_memo_by_text(path: Path) -> None:
    """Search memo in database (by text)."""
    connection: Connection = connect(path)
    connection.enable_load_extension(True)
    connection.load_extension(extension_path().replace('.so', ''))
    cursor: Cursor = connection.cursor()

    sql_select_text: str = '''SELECT ROWID, date_time, titles, bodies, tags
                              FROM memos
                              WHERE lower(bodies, "ru_RUS") LIKE ?'''
    print_md('Введите фрагмент текста заметки:')
    text: str = get_text_to_search().strip()

    if text != '':
        text_to_search: str = f'%{text.lower()}%'
    else:
        text_to_search = text

    try:
        cursor.execute(sql_select_text, (text_to_search,))
        memos: list | None = cursor.fetchall()

        if memos:
            for memo in memos:
                print_memo_from_db(memo)
        else:
            if text == '':
                print_md('Текст не задан, заметка не найдена.')
            else:
                print_md(f'Заметка с текстом `{text}` не найдена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def search_memo_by_tag(path: Path) -> None:
    """Search memo in database (by tag)."""
    connection: Connection = connect(path)
    connection.enable_load_extension(True)
    connection.load_extension(extension_path().replace('.so', ''))
    cursor: Cursor = connection.cursor()

    sql_select_tag: str = '''SELECT ROWID, date_time, titles, bodies, tags
                             FROM memos
                             WHERE lower(tags, "ru_RUS") LIKE ?;'''
    print_md('Введите фрагмент тега заметки:')
    tag: str = get_tag_to_search().strip()

    if tag != '':
        tag_to_search: str = f'%{tag.lower()}%'
    else:
        tag_to_search = tag

    try:
        cursor.execute(sql_select_tag, (tag_to_search,))
        memos: list | None = cursor.fetchall()

        if memos:
            for memo in memos:
                print_memo_from_db(memo)
        else:
            if tag == '':
                print_md('тег не задан, заметка не найдена.')
            else:
                print_md(f'Заметка с `{tag}` в теге не найдена.')

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
    finally:
        connection.close()


def search_memo_by_rowid(path: Path) -> int | None:
    """Search memo in database (by ROWID)."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select_rowid: str = '''SELECT ROWID, date_time, titles, bodies, tags
                               FROM memos
                               WHERE ROWID = ?;'''
    rowid: int | None = get_rowid()

    try:
        if rowid != 0:
            cursor.execute(sql_select_rowid, (rowid,))
            memo: tuple | None = cursor.fetchone()

            if memo:
                print_memo_from_db(memo)
            else:
                print_md(f'Заметка с `ID` {rowid} не найдена.')

                rowid = None
        else:
            print_md('Неверный ввод `ID`.')

            rowid = None

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')

        rowid = None
    finally:
        connection.close()

        return rowid


def count_memos(path: Path) -> int:
    """Show a number of memos in database."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_select: str = '''SELECT * FROM memos;'''
    total: int = 0

    try:
        cursor.execute(sql_select)
        total = len(cursor.fetchall())

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')

    finally:
        connection.close()

        return total


def check_db_integrity(path: Path) -> None:
    """Check integrity of database."""
    connection: Connection = connect(path)
    cursor: Cursor = connection.cursor()

    sql_integrity_check: str = '''PRAGMA integrity_check;'''

    try:
        cursor.execute(sql_integrity_check)
        result: str = cursor.fetchone()[0]

        if result == 'ok':
            print_md(f'База заметок `{path}` в порядке!')
            print_md(
                'Если всё же обратиться к ней не удалось, '
                + 'попробуйте восстановить её из резервной копии '
                + '(`restore-db`) или пересоздать (`recreate-db`).'
            )
        else:
            print_md(f'База заметок `{path}` повреждена!')
            print_md(
                'Попробуйте восстановить её из резервной копии '
                + '(`restore-db`) или пересоздать (`recreate-db`).'
            )

    except DatabaseError:
        print_md('Ошибка обращения к базе заметок.')
        print_md(
            'Попробуйте восстановить её из резервной копии '
            + '(`restore-db`) или пересоздать (`recreate-db`).'
        )
    finally:
        connection.close()
