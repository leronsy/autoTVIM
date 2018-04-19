from decorators import decor2
import sys
import os
@decor2
def src_path(input_file_name="file_list.txt"):
    """
    Открывает файл, читает первую строку в path и удаляет все после слова articles
    Добавляет к path \src и возвращает
    Простой способ найти папку src, если в файле первая строка вроде tvim/articles/author_name/
    :param input_file_name: имя файла для парсинга, по умолчанию - file_list.txt
    :return: словарь 'msg' и 'path' с абсолютным путём к папке src
    """
    try:
        with open(input_file_name) as f:
            first_line = f.readline()
            path = first_line.split('articles')[0]
            path += '\\src'
    except FileNotFoundError:
        print('В папке ', os.getcwd(),'\\','\nне обнаружен файл со списком статей "',input_file_name,
                         '".\nРабота программы будет остановлена.',sep='')
        sys.exit()
            # TODO:
             # '"\nФайлы authors.tex и referats.tex будут помещены в текущую папку',sep='')
        # path=os.getcwd()
        path='не найден'
    msg = 'путь к src: ' + path
    return {'path': path, 'msg': msg}


@decor2
def get_file_list(input_file_name="file_list.txt"):
    """
    Построчно читает пути к файлам из текстового файла input_file_name
    (по умолчанию "file_list.txt")
    :param input_file_name: строка, содержащая имя файла со списком статей
    :return: словарь из 'msg' сообщения о результате работы и список 'list' со строками,
    содержащими пути к файлам статей
    """
    try:
        with open(input_file_name) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print('В папке ', os.getcwd(),'\\',
                         '\nне обнаружен файл со списком статей "',input_file_name,
                         '".\nРабота программы будет остановлена.',sep='')
        sys.exit()
    else:
        msg = "Чтение путей из " + input_file_name + " завершено."
        file_path_list = [path.strip() for path in lines]
    return {'list': file_path_list, 'msg': msg}
