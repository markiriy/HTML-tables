import urllib.request
from html_table_parser import HTMLTableParser
from bs4 import BeautifulSoup as bs

import pandas as pd
import validators


urladd = 'empty'


# Открывает веб-сайт и читает его содержимое (HTTP Response Body)
def url_get_contents(url):
    # отправка запроса на веб-сайт
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    # чтение содержимого веб-сайта
    return f.read()

# выборка таблиц из html-кода страницы
def extract_tables(html):

    html_tables = []

    soup = bs(clean_html(html), "lxml")
    html_tables = soup.find_all('table')

    return html_tables


# подчистка html-кода
def clean_html(html):

    return html.replace('\n', '')

# структурирование и вывод таблиц
def print_tables(urladd):
    # определение html-содержимого URL-адреса.
    xhtml2 = url_get_contents(urladd).decode('utf-8')

    # Определение объекта HTMLTableParser
    p = HTMLTableParser()

    # передача содержимого html в объект HTMLTableParser
    p.feed(xhtml2)

    html_tables = []
    html_tables.append(extract_tables(xhtml2))

    print('\n {}НАЙДЕННЫЕ ТАБЛИЦЫ:{}\n \n '.format(yellow, reset))
    print("Найдено таблиц:", len(p.tables))

    for i in range(len(p.tables)):
        df = pd.DataFrame(p.tables[i])
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.max_colwidth', None,
                               ):

            count_row = df.shape[0]
            count_col = df.shape[1]

            print(df, '\n \n {}Количество строк: {}{} \n {}Количество столбцов: {}{}'.format(blue,count_row,reset,
                                                                                            blue,count_col,reset))

            print('\n{}ПРОВЕРКА ПОДЛИННОСТИ ТАБЛИЦЫ{}'.format(yellow, reset))
            if '.png' in str(html_tables[0][i]) or '.jpg' in str(html_tables[0][i]) or count_row <= 2 or count_col <= 2:
                print("{}Таблица {} не подлинна{}\n".format(red, i+1, reset))
            else:
                print('{}Таблица {} подлинна{}\n'.format(green, i+1, reset))


def FindTable(word): # поиск таблиц по слову
    xhtml = url_get_contents(urladd).decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)

    while True:
        for i in range(len(p.tables)):
            if word in p.tables[i][0]:
                df = pd.DataFrame(p.tables[i])
                with pd.option_context('display.max_rows', None,
                                       'display.max_columns', None,
                                       'display.max_colwidth', None,
                                       ):
                    print(df)
            else:
                pass
        print('\n{}Если вывод пуст - заголовок не был найден.{}'.format(green,reset))
        break

while True:
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    reset = "\033[0m"


    choice = input(' \n{}1{} - Найти таблицы по URL-адресу;  \n{}2{} - Поиск таблиц по заголовку;'
                   '  \n{}0 - ВЫХОД {}\n \n       '
                   '{}Введите номер для вывода таблиц по темам:{} '.format(green,reset,green,reset,red,
                                                                           reset,blue,reset))

    if choice == '1':
        urladd = input('\n \n {}Введите URL-адрес страницы:{} '.format(yellow,reset))
        if not validators.url(urladd):
            print(' \n{}ОШИБКА URL, ПОПРОБУЙТЕ ЕЩЕ РАЗ ИЛИ ИЗМЕНИТЕ ЕГО {}\n  {}(пример валидного URL-адреса: '
                  'https://habr.com/ru/articles/556852/){}'.format(red,reset,yellow,reset))
            continue
        else:
            print_tables(urladd)

    elif choice == '2':
        if urladd == 'empty':
            print('\n   {}URL НЕ НАЙДЕН: Сначала выведите таблицы по URL-адресу{}'.format(red,reset))
            continue
        else:
            headchoice = input('\n \n {}Введите заголовок:{} '.format(yellow,reset))
            FindTable(headchoice)

    elif choice == '0':
        print('\n{}Закрываемся...{}'.format(red,reset))
        break

    else:
        print(" \n{}Неверный ввод, попробуйте еще раз{}".format(red,reset))
        continue
