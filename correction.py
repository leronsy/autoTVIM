import re
import codecs
from dictionaries import correction_dict
from file_management import get_file_list

from decorators import decor2, decor1  # , decor3


@decor1
def correct(file_paths=None):
    """
    Главная функция модуля исправлений
    Получает список путей к статьям file_list из get_file_list()
    В цикле вызывает функцию correct_file для исправления каждого отдельного файла
    :return: сообщение 'msg'
    """
    msg=''
    file_list = get_file_list()['list']
    for file_name in file_list:
        try:
            correct_file(file_name)
        except FileNotFoundError:
            msg+=file_name+', '
    if len(msg):
        msg = 'WARN: Не найдены:\t'+msg
    else:
        msg = 'Успешно исправлены все файлы'
    return {'msg': msg}


"""  """


@decor2
def correct_file(file_name):
    """
    Считывает файл в строку file_content
    Применяет словарь регулярных выражений к строке file_content с помощью функции re.sub
        key - название блока замены
        regexp[0] - скомпилированный с re.compile pattern
        regexp[1] - строка для замены
    (NOTE:закомментированный блок позволяет увидеть какие исправления и где были применены)
    Записывает отредактированный файл по тому же пути но с прибавкой _cor
    (TODO:убрать для рабочей версии)
    :param file_name: строка, путь к файлу статьи
    :return: сообщение 'msg'
    """
    try:
        with codecs.open(file_name, 'r', 'cp1251') as fr:
            file_content = fr.read()
            for key, regexp in correction_dict.items():

                # matches=re.finditer(regexp[0],file_content)
                # dct={}
                # print('pattern:\t',"[",regexp[0],"]")
                # for match in matches:
                #     dct.update({match.span():match.groups()})
                # print( 'pattern\t','[',regexp[0],']' 'found:\t',len(dct))
                # for key,val in dct.items():
                #     print('Position: [%d:%d], Match:%s' %(key[0],key[1],val))
                file_content = re.sub(regexp[0], regexp[1], file_content)
    except FileNotFoundError:
        msg = 'ERR: Не найден файл статьи '+file_name
        raise
    else:
        with open(file_name[:-4] + "_cor.tex", 'w', newline='\n') as fw:
            fw.write(file_content)
            msg = 'Исправлен:\t' + file_name
    return {'msg': msg}
