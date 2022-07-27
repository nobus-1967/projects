"""Create new memo with date_time, title, body and tag."""
from datetime import datetime

from mdprinter import print_md
from prompter import get_new_title, get_new_text, get_new_tag
from prompter import get_title_to_edit, get_text_to_edit, get_tag_to_edit


def create_new_memo() -> tuple:
    """Create new memo (as tuple) with date_time, title, body and tag."""
    memo: tuple = (set_datetime(), input_title(), input_body(), input_tag())

    return memo


def set_datetime() -> str:
    """Set date_time of new memo."""
    now: datetime = datetime.now()

    return now.strftime('%Y-%m-%d %H:%M:%S')


def input_title() -> str:
    """Input and return title of new memo."""
    no_title: str = '## [Без заголовка]'

    print_md('Введите заголовок или просто нажмите `ENTER`:')
    title: str = get_new_title().strip()

    if title:
        title = f'## {title}'
    else:
        title = no_title

    return title


def input_body() -> str:
    """Input and return text of new memo."""
    no_text: str = '[Пустая заметка]'

    print_md(
        'Напишите заметку, для выхода нажмите `ESC` и затем `ENTER`:',
    )
    text: str = get_new_text().strip()

    if not text:
        text = no_text

    return text


def input_tag() -> str:
    """Input and return tag of new memo."""
    no_tag: str = '#no_tag'

    print_md('Введите тэг или просто нажмите `ENTER`:')
    tag: str = get_new_tag().strip()

    if tag:
        tag = f'#{tag}'
    else:
        tag = no_tag

    return tag


def input_corrected_title() -> tuple[str, str]:
    """Paste (from clipboard) and correct title of existing memo."""
    no_title: str = '## [Без заголовка]'

    print_md(
        'Вставьте прежний текст из буфера (`CTRL+Y`) и внесите в него '
        + 'исправления, затем нажмите `ENTER`:'
    )
    corrected_title: str = get_title_to_edit().strip()

    if corrected_title:
        corrected_title = f'## {corrected_title}'
    else:
        corrected_title = no_title

    updated_date_time: str = set_datetime()

    return updated_date_time, corrected_title


def input_corrected_body() -> tuple[str, str]:
    """Paste (from clipboard) and correct text of existing memo."""
    no_text: str = '[Пустая заметка]'

    print_md(
        'Вставьте прежний текст из буфера (`CTRL+Y`) и внесите в него '
        + 'исправления, для выхода нажмите `ESCAPE` и затем `ENTER`:'
    )
    corrected_text: str = get_text_to_edit().strip()

    if not corrected_text:
        corrected_text = no_text

    updated_date_time: str = set_datetime()

    return updated_date_time, corrected_text


def input_corrected_tag() -> tuple[str, str]:
    """Paste (from clipboard) and correct tag of existing memo."""
    no_tag: str = '#no_tag'

    print_md(
        'Вставьте прежний текст из буфера (`CTRL+Y`) и внесите в него '
        + 'исправления, затем нажмите `ENTER`:'
    )
    corrected_tag: str = get_tag_to_edit().strip()

    if corrected_tag:
        corrected_tag = f'#{corrected_tag}'
    else:
        corrected_tag = no_tag

    updated_date_time: str = set_datetime()

    return updated_date_time, corrected_tag
