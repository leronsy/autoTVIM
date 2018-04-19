import re
import codecs
from decorators import decor2, decor1, decor3, decor4
from dictionaries import structuring_dict
from file_management import get_file_list


class MyException(Exception):
    pass


@decor4
def search_pattern(file_content, pattern_key):
    """
    Упрощаем получение match с помощью библиотеки re
    Возвращает True и match, если совпадение найдено.
    Возвращает False и None, если не найдено
    :param file_content:
    :param pattern_key:
    :return:
    """
    pattern = structuring_dict.get(pattern_key)
    match = re.search(pattern, file_content)
    if match:
        msg = 'Есть совпадение c шаблоном\t' + pattern_key
    else:
        msg = 'Нет совпадения c шаблоном\t' + pattern_key
    return {'match': match, 'msg': msg}


@decor3
def string_insert(string, insert_string, start, end=None):
    if start > len(string) or start < 0:
        msg = "Ошибка в start"
        result_str = string
    else:
        if not end:
            end = start
        msg = "Успешная вставка"
        result_str = string[:start] + insert_string + string[end:]

    return {'result_str': result_str, 'msg': msg}


def is_string_ends_with_dot(word):
    if word.endswith('.'):
        return ''
    return word.strip()


def collect_surnames(authors):
    authors_mod = authors.replace(',', '\\').replace(';', '').replace(' ', '\\')
    # authors_mod = authors_mod
    # authors_mod = authors_mod.replace
    authors_list = authors_mod.split('\\')

    surnames = ''.join(map(is_string_ends_with_dot, authors_list))  # for word in authors_list
    return surnames


@decor4
def create_labels(file_content):
    """
    TODO: добавить проверку

    :param file_content:
    :return:
    """
    match = search_pattern(file_content, 're title_author_en')['match']
    authors = match.group('author')
    surnames = collect_surnames(authors)
    label_begin = '\label{' + surnames + '_begin}\n'
    label_end = '\label{' + surnames + '_end}\n'
    msg = 'Метки успешно созданы.'
    return {'label_begin': label_begin, 'label_end': label_end, 'surnames': surnames, 'msg': msg}


@decor3
def add_author_labels(file_content):
    """
    Проверяет наличие меток. Если не найдены, и есть данные для их создания,
    то добавляет метки \label{Фамилия_begin} и \label{Фамилия_end}
    :param file_content:
    :return:
    """
    changes = 0
    msg = None
    res_dict = create_labels(file_content)
    label_begin = res_dict['label_begin']
    label_end = res_dict['label_end']
    surnames = res_dict['surnames']

    match_surnames_begin = search_pattern(file_content, 're label Surname_begin')['match']
    if match_surnames_begin is None:
        msg = ('Не найден\t', 're label Surname_begin')
        article_beginning = file_content.find(structuring_dict['article beginning'])
        if article_beginning == -1:
            msg += ("\nНе найден\t", 'article beginning')
            return {'file_content': file_content, 'changes': changes, 'msg': msg}
        # Если найден, но фамилии не совпадают

        file_content = string_insert(file_content, label_begin, article_beginning)['result_str']
        match_surnames_begin = search_pattern(file_content, 're label Surname_begin')['match']
        msg += ("\nДобавлено", label_begin)
        changes += 1

    match_surnames_end = search_pattern(file_content, 're label Surname_end')['match']
    # print('match_surnames_end',match_surnames_end)
    if match_surnames_end is None:

        msg = ('Не найден\t', 're label Surname_end')
        article_ending = file_content.find(structuring_dict['article ending'])
        if article_ending == -1:
            msg += ("Не найден", 'article ending')
            return {'file_content': file_content, 'changes': changes, 'msg': msg}

        file_content = string_insert(file_content, label_end, article_ending)['result_str']
        msg += ("\nДобавлено", label_end)
        match_surnames_begin = search_pattern(file_content, 're label Surname_begin')['match']
        changes += 1
    if not (match_surnames_begin.group('surname') == surnames and match_surnames_end.group(
            'surname') == surnames):
        # print("!!!\n",file_content[26100:26150],"!!!")
        file_content = string_insert(file_content, surnames,
                                     match_surnames_begin.span('surname')[0],
                                     match_surnames_begin.span('surname')[1])['result_str']
        match_surnames_end = search_pattern(file_content, 're label Surname_end')['match']
        file_content = string_insert(file_content, surnames,
                                     match_surnames_end.span('surname')[0],
                                     match_surnames_end.span('surname')[1])['result_str']
        msg = "Фамилии в исходном label не совпадают с полученными. Произведена замена."
    if not msg:
        msg = 'label уже существуют'

    return {'file_content': file_content, 'changes': changes, 'msg': msg}


@decor3
def clean_above_separator(file_content):
    """ Принимает содержимое файла file_content и разделитель separator
    Делит строку с помощью partition
    Удаляет содержимое файла перед разделителем
    TODO:replace
    Возвращает отредактированный файл """
    changes = 0
    # считаем, что если эта строка первая, то лишних строк в начале файла нет
    found = search_pattern(file_content, 're input init_counters')['match']
    if found:
        msg = "Найден init counters, удаление не нужно."
        return {'file_content': file_content, 'changes': changes, 'msg': msg}
    changes += 1
    separator = structuring_dict.get('markboth')
    tuple_of_parts = file_content.partition(separator)
    if len(tuple_of_parts[1]) == 0:
        print()
    file_content = tuple_of_parts[1] + tuple_of_parts[2]
    msg = "Строки до разделителя " + structuring_dict.get('markboth') + " удалены"
    return {'file_content': file_content, 'changes': changes, 'msg': msg}


@decor3
def comment_after_separator(file_content):
    """ Комментирует строки после "\bigskip"
    Принимает содержимое файла file_content и разделитель separator ("\bigskip")
    Делит строку с помощью str.partition
    Комментирует все строки после разделителя с помощью '%'
    TODO:replace
    Возвращает отредактированный файл """

    changes = 0
    match_end = search_pattern(file_content, 're label Surname_end')['match']
    separator = match_end.group('end_label')
    tuple_of_parts = file_content.partition(separator)
    file_content = tuple_of_parts[0] + tuple_of_parts[1]
    ending = tuple_of_parts[2].split('\n')
    for line in ending:
        if len(line) and line[0] != r'%':
            line = '%' + line
        file_content = '\n'.join([file_content, line])
    msg = "Строки после label _end закомментированы."
    return {'file_content': file_content, 'changes': changes, 'msg': msg}


@decor3
def add_input_lines(file_content):
    """ Добавляет \input... в начале файла
    Принимает содержимое файла file_content
    Ищет в тексте совпадения с ключами, название которых начинается на "re input",
    а если не найдено, добавляет в header соответствующий input
    Дописывает header в начало файла
    Возвращает отредактированный файл
    NOTE: Для работы с английским необходимо добавить дополнительное условие """
    changes = 0
    header = ''
    for key in structuring_dict:
        if key.startswith("re input"):
            match = search_pattern(file_content, key)['match']
            if not match:
                changes += 1
                header = header + structuring_dict[key[3:]]
    file_content = header + '\n' + file_content
    msg = "Добавлены input строки в начало файла"
    return {'file_content': file_content, 'changes': changes, 'msg': msg}


def build_contentsline(match):
    title = match.group('title').replace('\n', ' ')
    author = match.group('author').replace('\n', ' ')
    return '\\addcontentsline{toc}{art}{\\textbf{' + author + '} ' + title + '}'


@decor3
def add_addcontentsline(file_content):
    """ Добавляет \addcontentsline в начале файла
    Принимает содержимое файла file_content
    Из словаря берёт скомпилированные re.compile выражения для поиска
    "\abstract" и "\abstractWithTitle",достаёт из них title и author
    создаёт строки \addcontentsline и вставляет их в начало файла
    Возвращает отредактированный файл"""
    changes = 0
    # TODO: можно проверять наличие обеих строк через match_contentsline.groups
    match_contentsline = search_pattern(file_content, 're addcontentsline')['match']
    if match_contentsline:
        msg = "addcontentsline уже существуют."
    else:
        msg = ''
        info_list = ['re title_author_ru', 're title_author_en']
        for info in info_list:
            try:
                match = search_pattern(file_content, info)['match']
                if match:
                    contentsline = build_contentsline(match)
                if len(contentsline):
                    # Разделение по init, если есть
                    # TODO: имеет ли значение порядок addcontentsline?
                    separator_input = structuring_dict.get('input to_rus')
                    if separator_input != -1:
                        file_content_list = file_content.partition(separator_input)
                        file_content = file_content_list[0] + file_content_list[1]\
                                       + '\n' + contentsline + '\n' + file_content_list[2]
                    else:
                        file_content = contentsline + '\n' + file_content
                    changes += 1
                    msg += "Успешная вставка addcontentsline " + info[-2:].upper()
            except :
                msg = 'ERR: Не найдены данные для создания contentsline ' + info[-2:].upper()

    return {'file_content': file_content, 'changes': changes, 'msg': msg}


"""Список основных функций, применяемых по порядку к каждому файлу"""
function_list = [clean_above_separator, add_author_labels, comment_after_separator,
                 add_addcontentsline,
                 add_input_lines]


@decor2
def structure_file(file_name, debug):
    """ Функция создания структуры для отдельного файла
    Принимает путь к файлу и словарь структурирования
    Читает содержимое файла в file_content
    Проверяет, необходимо ли структурирование с помощью is_structured()
    Применяет функциии структурирования
    Записывает отредактированный файл по тому же пути но с прибавкой _struct
    (NOTE: в рабочей версии убрать) """
    if debug:
        file_name = file_name[:-4] + '_c.tex'
    try:
        with codecs.open(file_name, 'r', 'cp1251') as fr:
            file_content = fr.read()
            change_list = list()
            for idx, fun in enumerate(function_list):
                res = fun(file_content)
                file_content = res.get('file_content')
                changes = res.get('changes')
                change_list.append(changes)
    except FileNotFoundError:
        msg = 'ERR: Не найден файл статьи ' + file_name
        raise
    else:
        # без newline='\n' портятся переводы строк
        with open(file_name[:-4] + "s.tex", 'w', newline='\n') as fw:
            fw.write(file_content)
        if sum(change_list) > 0:
            msg = file_name + " структурирован. " + str(change_list)
        else:
            msg = file_name + "не нуждается в структурировании."
    return {'msg': msg}


@decor1
def structure(file, debug):
    """ Главная функция модуля структурирования
    Загружает список путей к файлам file_list из из file_list_cor.txt с помощью get_file_paths()
    (NOTE:список путей к файлам для тестовой версии отличается от списка файла для коррекции) """

    msg = ''
    file_list = get_file_list(file)['list']
    for file_name in file_list:
        try:
            structure_file(file_name, debug)
        except FileNotFoundError:
            msg += file_name + ', '
    if len(msg):
        msg = 'WARN: Не найдены статьи:\t' + msg
    else:
        msg = 'Успешно структурированы все файлы'
    return {'msg': msg}
