"""
Лексический анализатор на базе конечного автомата входного
языка, описанного диаграммой состояний.
Функция lexer реализует алгоритм, описываемый конечным
автоматом. Переменная CS содержит значение текущего состояния
автомата. В начале работы программы – это начальное состояние H. Переход
из этого состояния в другие происходит только, если во входной
последовательности встречается символ, отличный от пробела, знака
табуляции или перехода на новую строку. После достижения границы лексемы
осуществляется возврат в начальное состояние. Из состояния ERR тоже
происходит возвращение в начальное состояние, таким образом, лексический
анализ не останавливает после обнаружения первой ошибки, а продолжается
до конца входной последовательности. Концом входной последовательности
является конец файла.
"""

import re

NUM_OF_KWORDS = 2

keywords = ["for", "do"]
states = {"H": 0, "ID": 1, "NM": 2, "ASGN": 3, "DLM": 4, "ERR": 5}
'''
States
H - начальное состояние
ID - идентификаторы
NM - числа
ASGN - знак присваивания
DLM - разделители
ERR - нераспознанные символы
'''

tok_names = {"KWORD": 0, "IDENT": 1, "NUM": 2, "OPER": 3, "DELIM": 4}


class Token:  # создание токенов
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value


class LexemeTable:  # таблица лексем
    def __init__(self, token, nex):
        self.tok = token
        self.next = nex


lt = None
lt_head = None


def is_kword(id):  # является ли идентиикатор ключевым словом
    return id in keywords


def add_token(tok):  # добавление токена в таблицу лексем
    global lt, lt_head
    if lt_head is None:
        lt = LexemeTable(tok, None)
        lt_head = lt
    else:
        new_lt = LexemeTable(tok, None)
        lt.next = new_lt
        lt = new_lt


def is_digit(buf):  # проверка на правильность записис числа
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    match = re.match(pattern, buf)
    return bool(match)


def lexer(filename):  # анализирует символы из файла и определяет их тип (идентификатор, число, оператор, разделитель)
    """
    Код использует состояния для управления процессом анализа и создает токены в соответствии с
    различными типами символов.
    """
    try:
        fd = open(str(filename), "r")
        c = fd.read(1)
        CS = states["H"]  # текущее состояние автомата
        err_count = 0
        while c:
            if CS == states["H"]:
                while c in [' ', '\t', '\n']:
                    c = fd.read(1)
                if c.isalpha() or c == '_':
                    CS = states["ID"]
                elif c.isdigit() or c == '.' or c == '+' or c == '-':
                    CS = states["NM"]
                elif c == ':':
                    CS = states["ASGN"]
                else:
                    CS = states["DLM"]

            elif CS == states["ASGN"]:
                colon = c
                c = fd.read(1)
                if c == '=':
                    tok = Token(tok_names["OPER"], ':=')
                    add_token(tok)
                    c = fd.read(1)
                    CS = states["H"]
                else:
                    err_symbol = colon
                    CS = states["ERR"]

            elif CS == states["DLM"]:
                if c in ['(', ')', ';']:
                    tok = Token(tok_names["DELIM"], c)
                    add_token(tok)
                    c = fd.read(1)
                    CS = states["H"]
                elif c in ['<', '>', '=']:
                    tok = Token(tok_names["OPER"], c)
                    add_token(tok)
                    c = fd.read(1)
                    CS = states["H"]
                else:
                    err_symbol = c
                    c = fd.read(1)
                    CS = states["ERR"]

            elif CS == states["ERR"]:
                print("Неизвестный символ или неправильно заданный токен:", err_symbol)
                err_count = err_count + 1
                CS = states["H"]

            elif CS == states["ID"]:
                buf = []
                buf.append(c)
                c = fd.read(1)
                while c.isalpha() or c.isdigit() or c == '_':
                    buf.append(c)
                    c = fd.read(1)
                buf.append('\0')
                buf = ''.join(buf)
                if is_kword(buf):
                    tok = Token(tok_names["KWORD"], buf)
                else:
                    tok = Token(tok_names["IDENT"], buf)
                add_token(tok)
                CS = states["H"]

            elif CS == states["NM"]:
                buf = [c]
                c = fd.read(1)
                while c.isdigit() or c in ['-', '+', 'e', 'E', '.', ' ']:
                    buf.append(c)
                    c = fd.read(1)
                buf = ''.join(buf)
                if is_digit(buf):
                    tok = Token(tok_names["NUM"], buf)
                    add_token(tok)
                    CS = states["H"]
                else:
                    err_symbol = buf
                    c = fd.read(1)
                    CS = states["ERR"]
        fd.close()
        print('Обработка завершена.')
        if err_count == 0:
            print('Ошибок нет.')
        else:
            print("Количество ошибок:", err_count)
    except FileNotFoundError:
        print('Файл не найден')
    except IOError:
        print('Ошибка ввода-вывода при открытии файла')


if __name__ == '__main__':
    lexer("r3.txt")
