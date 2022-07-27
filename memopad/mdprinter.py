"""Print help and memos using Markdown markup language."""
from rich.console import Console
from rich.markdown import Markdown


def print_new_memo(memo: tuple) -> None:
    """Print memo using Markdown markup language."""
    console: Console = Console()

    date_time: str = memo[0]
    title: str = memo[1]
    body: str = memo[2]
    tag: str = memo[3]

    console.print(f'\n{date_time} {tag}')
    console.print(Markdown(title))
    console.print(Markdown(body))


def print_memo_from_db(memo: tuple) -> None:
    """Print memo using Markdown markup language."""
    console: Console = Console()

    rowid: int = memo[0]
    date_time: str = memo[1]
    title: str = memo[2]
    body: str = memo[3]
    tag: str = memo[4]

    console.print(f'\n{date_time} {tag} (ID: {rowid})')
    console.print(Markdown(title))
    console.print(Markdown(body))


def print_md(text: str) -> None:
    """Print help and messages using Markdown markup language."""
    console: Console = Console()

    console.print(Markdown(text))
