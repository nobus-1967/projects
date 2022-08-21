# MemoPad

**MemoPad** - CLI-программа для создания, редактирования и просмотра заметок в терминале, использующая [`SQLite`](https://www.sqlite.org) как базу заметок.

Программа позволяет использовать в заметках форматирование элементы языка разметки [`Markdown`](https://www.markdownguide.org/basic-syntax).

Для многострочного ввода текста применяются возможности модуля [`Prompt Toolkit`](https://github.com/prompt-toolkit/python-prompt-toolkit).

Регистронезависмый поиск по кириллическому тексту реализован с помощью пакета [`sqlite-icu`](https://pypi.org/project/sqlite-icu).

Для копирования и вставки текста применяется модуль [`Pyperclip`](https://pyperclip.readthedocs.io/en/latest). В **GNU/Linux** использование данного модуля может потребовать установку одного из механизмов работы с буфером обмена: `xsel`, `xclip`, `gtk` или `PyQt4`.

Список внешних заимствований содержится в файле `requirements.txt`.

Для своей работы программа создаёт папку `~/.memopad/`в домашнем каталоге пользователя, где хранится база данных (`memos.db`) и резервная копия базы данных (`memos.db.backup`).

О программе подробнее: [*MemoPad* — консольный редактор и SQLite-база  заметок](https://avshcherbina.ru/#memopad)

Автор программы: **Анатолий Щербина** (https://github.com/nobus-1967).

Версия программы: `1.1.5`

Лицензия: [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
