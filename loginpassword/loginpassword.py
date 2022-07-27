"""Generate logins and passwords for students and write into CSV-files (1.0)."""
import random
import csv
from datetime import datetime

# Определить глобальные константы.
A_B_C = 'AaBbCcDdEeFfGgHhIiJiKkLlMmNnJjPpQqRrSsTtUuVvWwXxYyZz'
NUMBERS = '0123456789'
SYMBOLS = A_B_C + NUMBERS

# Для транслитерирования используется принцип соотнесения латинских и русских
# букв, принятый при выдаче заграничных паспортов гражданам России.
TRANSLIT = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': 'ie', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'iu', 'я': 'ia', '_': '_', '-': '-'}


def main():
    """Функция генерирует логин и пароль и сохраняет их в CSV-файле."""
    # Инициализировать флаг, который будет повторять выполнение программы.
    another = 'д'

    # Сообщить о начале работы программы.
    print('Данная программа генерирует пароли и логины обучающимся.')
    print('Пароли и логины сохраняются в CSV-файле.')

    # Запустить цикл выполнения программы.
    while another == 'д'.lower():
        # Получить информацию о студенте.
        information = 'Error'
        while information == 'Error':
            information = get_info()

        # На основе полученных данных сгенерировать логин студента.
        login = get_login(information)
        print('\nСгенерированные данные:')
        print(f'\tлогин - {login}')

        # Сгенерировать корректный пароль студента.
        password = get_password(A_B_C, SYMBOLS)
        print(f'\tпароль - {password}')

        # Записать информацию в CVS-файл.
        save_info(information, login, password)
        print('\nИнформация записана в файл.')

        # Запросить у пользователя необходимость повтора программы
        # для генерации пароля и логина ещё одному студенту.
        print('\nПовторить операции для ещё одного студента?')
        another = input('\tд=да, всё остальное=нет: ')
        if another.lower() == 'да':
            another = another[0]

    # Сообщить о завершении программы.
    print('\nРабота программы завершена.')
    print('(c) Nobus, 2021')


def get_info():
    """
    Функция получает от пользователя корректную информацию о студенте.

    Запрашиваемая информация:
    - fullname - Ф.И.О. полностью (отчество указывается при наличии),
    - code - буквенный код направления подготовки (специальности),
    - year - год поступления,
    - group - номер учебной группы,
    - number - исходный номер студента в группе (при формировании группы),
    - form - форма обучения.
    :return: information - запрошенная информация в виде словаря (dict).
    """
    # Получить данные о студенте и проверить их на корректность ввода.
    try:
        fullname = input('\nВведите Ф.И.О. студента (при наличии): ').strip()
        assert type(fullname) == str and (2 <= len(fullname.split()) <= 3)

        code = input('Введите буквенный код направления подготовки \
(специальности): ').strip()
        assert len(code) > 0

        year = input('Введите год поступления студента (4 цифры): ').strip()
        assert len(year) == 4
        check_year = int(year)
        assert 1950 < check_year < 2025

        group = input('Введите цифрой номер учебной группы: ').strip()
        assert len(group) > 0
        check_group = int(group)
        group = str(check_group)

        number = input('Введите исходный номер студента \
в учебной группе: ').strip()
        assert len(group) > 0
        check_number = int(number)
        number = str(check_number)

        form = input('Введите форму обучения (1=очное, 2=заочное): ').strip()
        assert len(code) > 0 and form in '12'

        # Преобразовать данные в словарь.
        information = {'fullname': fullname,
                       'code': code,
                       'year': year,
                       'group': group,
                       'number': number,
                       'form': form}
    except (AssertionError, ValueError):
        # В случае ошибки повторить ввод данных.
        print('Данные введены неверно! Необходимо ввести их заново.\n')
        return 'Error'
    else:
        # Вернуть словарь с данными.
        return information


def get_login(information):
    """
    Функция генерирует логин на основании данных о студенте.

    Функция плучает:
    :param information: словарь с информацией о студенте.
    Уникальный логин включает:
    - фамилию и инициалы студента,
    - код направления подготовки (специальности),
    - год поступления студента,
    - номер учебной группы,
    - исходный номер студента в гучебной группе и
    - форму обучения.
    :return: login - сгенерированный логин пользователя (str).
    """
    # Распаковать данные из словаря.
    fullname = information['fullname']
    code = information['code']
    year = information['year']
    group = information['group']
    number = information['number']
    form = information['form']

    # Преобразовать в строчные буквы и транслитерировать имя и
    # инициалы студента c использованием глобального словаря.
    name = fullname.split()
    if len(name) == 2:
        name, firstname = name
        shortname = f'{name}_{firstname[0]}'
    else:
        name, firstname, patronymic = name
        shortname = f'{name}_{firstname[0]}{patronymic[0]}'
    transl_name = ''
    for ch in shortname.lower():
        transl_name += TRANSLIT[ch]

    # Преобразовать в строчные буквы и транслитерировать код направления
    # подготовки (специальности) c использованием глобального словаря.
    transl_code = ''
    for ch in code.lower():
        transl_code += TRANSLIT[ch]

    # При необходимости добавить к номеру группы и номеру студента начальный 0.
    # Также преобразовать сведения о форме обучения
    # (в логине студента будет отражена только заочная форма обучения).
    w_group = group if int(group) > 10 else '0' + group
    w_num = number if int(number) > 10 else '0' + number
    w_form = '' if form == '1' else 'z'

    # Сформировать логин студента.
    login = f'{transl_name}_{transl_code}{year[-2:]}{w_group}{w_form}_{w_num}'

    # Вернуть сформированный логин.
    return login


def get_password(A_B_C, SYMBOLS):
    """
    Функция генерирует пароль из 8 символов.

    Первый символ пароля не может быть цифрой.
    Остальные символы - буквы (в верхнем или нижнем регистре) или цифры.
    Для генерации пароля используются глобальные константы:
    :param A_B_C: прописные и с рочные латинские буквы,
    :param SYMBOLS: латинские буквы и цифры от 0 до 9.
    :return: password - возращается сгенерированный пароль (str).
    """
    # Сгенерировать пароль в цикле с использованием глобальных констант
    # (пока не будет удовлетворены все условия к формированию пароля).
    repeat = True
    password = ''
    while repeat:
        password = ''
        password += A_B_C[random.randint(0, 51)]
        for _ in range(7):
            password += SYMBOLS[random.randint(0, 61)]

        repeat = check_password(password)

    # Вернуть сгенерированный пароль.
    return password


def check_password(password):
    """
    Функция проверяет требования к паролю.

    Проводится посимвольная проверка вновь сгенерированного пароля,
    имеются ли в нём буквы разного регистра и цифры.
    :param password: проверяемый пароль.
    :return: is_not_valid для повторения или окончания проверки (bool).
    """
    # Определить переменные для проверки наличия в пароле цифр,
    # строчных и прописных букв.
    is_digit = False
    is_lower = False
    is_upper = False

    # Проверить наличие в пароле требуемых символов.
    for symbol in password:
        if symbol.isdigit():
            is_digit = True
        elif symbol.islower():
            is_lower = True
        elif symbol.isupper():
            is_upper = True

    # False в случае, если пароль удовлетворяет требованиям
    # (чтобы завершить цикл генерации пароля).
    is_not_valid = True
    if is_digit and is_lower and is_upper:
        is_not_valid = False

    # Вернуть информацию о необходимости заново генерировать пароль.
    return is_not_valid


def save_info(information, login, password):
    """
    Функция сохраняет всю информацию о студенте в датированном CSV-файле.

    В названии файла отражены дата его создания.
    В файл записываются:
    :param information: информация о студенте:
    - Ф.И.О.,
    - код направления подготовки(специальности),
    - год поступления,
    - номер учебной группы,
    - исходный номер студента в учебной группе,
    - форма обучения,
    :param login: логин и
    :param password: пароль студента.
    """
    # Распаковать словарь с информацией о студенте.
    fullname = information['fullname']
    code = information['code']
    year = information['year']
    group = information['group']
    number = information['number']

    # Скорректировать для записи в файл информацию о форме обучения
    # (в удобном для чтения виде).
    form = information['form']
    fullform = 'ОФО' if form == '1' else 'ЗФО'

    # Сформировать строку для записи в CSV-файл.
    w_info = [fullname, code, year, group, number, fullform, login, password]

    # Сформировать дату для имени файла.
    cur_datetime = datetime.now()
    w_datetime = f'{cur_datetime.year}-{cur_datetime.month}-{cur_datetime.day}'

    # Открыть файл для записи (дозаписи) и записать в него строку.
    with open(f'logins_{w_datetime}.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(w_info)


if __name__ == '__main__':
    main()
