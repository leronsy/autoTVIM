import codecs
import os
import re
from operator import itemgetter
from copy import deepcopy
from file_management import get_file_list, src_path
from dictionaries import structuring_dict, science_dict, country_dict
from decorators import decor1, decor2, decor3, decor4


@decor4
def abbr_space_replace(str_with_abbr):
    re_word = structuring_dict.get('re word_dot_space')
    match_iter = re.finditer(re_word, str_with_abbr)
    msg = 'Заменено: '
    for match in match_iter:
        word = match.group('word')
        if not word.endswith('\\;'):
            new_word = re.search('\w+?\.', word).group(0) + '\\;'
            str_with_abbr = str_with_abbr.replace(word, new_word, 1)
            msg += "'{0}'->'{1}' ".format(word, new_word)
    return {'abbr': str_with_abbr, 'msg': msg}


@decor4
def country_replace(str_with_country):
    msg = 'Не найдена страна!'
    for key, value in country_dict.items():
        position = str_with_country.find(key)
        if position != -1:
            str_with_country = str_with_country.replace(key, value)
            msg = 'Cтрана: ' + key
            break
    return {'country': str_with_country, 'msg': msg}


@decor4
def degree_replace(post):
    post_lst = post.split(',', 1)
    degree_from_text = post_lst[0]
    rest = post_lst[1]
    re_degree_key = structuring_dict.get('re degree')
    match_degree = re.search(re_degree_key, degree_from_text)
    msg = 'Не удалось заменить'
    result = post
    if match_degree:
        degree = match_degree.group('degree')

        if degree == 'к' or degree == 'К':
            degree = 'k'
        elif degree == 'д' or degree == 'Д':
            degree = 'd'
        else:
            degree = '?'

        science = science_dict.get(match_degree.group('science'))
        if not science:
            science = '_??_'
        degree_new = degree + science + 'n'
        result = '{\\' + degree_new + ',' + rest
        msg = degree_from_text[1:] + ' -> ' + degree_new
    return {'result': result, 'msg': msg}


@decor3
def unique_author(author_lst):
    msg = 'Количество авторов: '
    unique_lst = []
    surnames = set(tpl[0] for tpl in author_lst)
    authors_number = 0
    for tpl in author_lst:
        if tpl[0] in surnames:
            unique_lst.append(tpl)
            surnames.remove(tpl[0])
            authors_number += 1
    msg += str(authors_number)
    return {'unique_lst': unique_lst, 'msg': msg}


@decor2
def get_authorinfo(file_content):
    msg = 'good'
    authorinfo_lot = re.findall(structuring_dict.get('re authorinfo'), file_content)
    result_lol = []
    authors_clean = []
    for tpl in authorinfo_lot:
        author = []

        for item in tpl:
            item = item.replace('%', '').replace('\n', ' ').replace('  ', '')
            author.append(item)
        # степень и университет
        medskip = structuring_dict.get('medskip')
        authorinfo = structuring_dict.get('authorinfo')

        authors_clean.append(author[0].strip('{}') + ' ' + author[1].strip('{}'))

        author[0] = medskip + '\n' + authorinfo + author[0]
        author[2] = degree_replace(author[2])['result']
        # замена обычных пробелов между сокращением и следующим словом
        author[2] = abbr_space_replace(author[2])['abbr']
        # TODO:Менять только последнюю?????? тогда нужны изменения в коде
        author[2] = country_replace(author[2])['country']
        author[3] += '\n'
        result_lol.append(author)
    authors_clean.sort()
    for i, author in enumerate(authors_clean):
        name_lst = []
        author = author.split()
        for n, word in enumerate(author):
            if n != 0:
                word = word[0]
            name_lst.append(word)
        authors_clean[i] = name_lst

    # print('result_lol',result_lol)
    return {'msg': msg, 'authorinfo': result_lol, 'authors_clean': authors_clean}


def name_middle_surname(lst):
    nms = lst[1] + '.\\;' + lst[2] + '.\\;' + lst[0]
    return nms


def surname_name_middle(lst):
    snm = lst[0] + '\\;' + lst[1] + '.\\;' + lst[2][0] + '.'
    return snm


@decor4
def referat_to_string(referat):
    referat_str = '\\tvimRef\n{'
    for name in referat[0]:
        referat_str += name + ', '
    referat_str = referat_str[:-2] + '}\n{'
    for name in referat[1]:
        referat_str += name + ', '
    referat_str = referat_str[:-2] + '}\n'
    for item in referat[2:]:
        referat_str += '{' + item + '}\n'
    referat_str += structuring_dict.get('abstractline')
    msg = 'Успешно преобразован:\t' + referat[2][:15] + '...'
    return {'referat_str': referat_str, 'msg': msg}


@decor1
def assemble():
    path = src_path()['path']
    file_list = get_file_list('file_list_cor_struct.txt')['list']

    authorinfo_list = []
    referat_lol = []
    for file_name in file_list:

        referat_lst = []
        print('Работа над файлом:\t', file_name, sep='')
        with codecs.open(file_name, 'r', 'cp1251') as fr:
            file_content = fr.read()
            result_authorinfo = get_authorinfo(file_content)
            authorinfo = result_authorinfo['authorinfo']
            for lst in authorinfo:
                authorinfo_list.append(lst)

            # 1 - Первый автор (можно нескольких, а можно и всех) в формате Фамилия И. О.
            # 2 - Все авторы в формате И. О. Фамилия
            authors_snm = result_authorinfo['authors_clean']
            authors_nms = deepcopy(authors_snm)
            for i, author in enumerate(authors_snm):
                authors_snm[i] = surname_name_middle(author)
                authors_nms[i] = name_middle_surname(author)
            referat_lst.append(authors_snm)
            referat_lst.append(authors_nms)

            # 3 - Название статьи
            re_abstract = structuring_dict.get('re abstract')
            full_abstract = re.search(re_abstract, file_content)
            if full_abstract:
                abstract_title = full_abstract.group('title').lower().capitalize()
                # 7 - Аннотация на русском языке
                abstract_content = full_abstract.group('abstract').replace('%', ''). \
                    replace(
                    'Обязательна русская короткая аннотация. Для статей на английском указать название статьи и ФИО!!!',
                    '') \
                    .replace('\n', '')
                # 8 - Ключевые слова на русском языке
                re_keywords_ru = structuring_dict.get('re keywords ru')
                keywords_ru = re.search(re_keywords_ru, file_content).group('keywords')
                keywords_ru = keywords_ru.replace('%', '').replace('\n', '')
            else:
                abstract_title = "NO TITLE!"
                abstract_content = "NO ABSTRACT!"
                keywords_ru = "NO KEYWORDS!"

            referat_lst.append(abstract_title)
            # 4 - Первая страница
            re_lb_begin = structuring_dict.get('re label Surname_begin')
            lb_begin = re.search(re_lb_begin, file_content).group('begin_label')
            referat_lst.append(lb_begin)
            # 5 - Последняя страница
            re_lb_end = structuring_dict.get('re label Surname_end')
            lb_end = re.search(re_lb_end, file_content).group('end_label')
            referat_lst.append(lb_end)
            # 6 - УДК
            re_udc = structuring_dict.get('re udc')
            udc = re.search(re_udc, file_content).group('number')
            referat_lst.append(udc)

            referat_lst.append(abstract_content)
            referat_lst.append(keywords_ru)

        referat_lol.append(referat_lst)
    authorinfo_list = unique_author(authorinfo_list)['unique_lst']
    authorinfo_list = sorted(authorinfo_list, key=itemgetter(0))

    os.chdir(path)
    # без newline='\n' портятся переводы строк
    with codecs.open("authors.tex", 'r', 'cp1251') as fr:
        authors_orig = fr.read()
        medskip = structuring_dict.get('medskip')
        authorinfo = structuring_dict.get('authorinfo')
        authors_file_head = authors_orig.split(medskip + '\n' + authorinfo, 1)[0]

    with open("authors" + "_new.tex", 'w', newline='\n') as fw:
        fw.write(authors_file_head)
        for lst in authorinfo_list:
            fw.write("%s\n" % ''.join(lst))

    with codecs.open("referats.tex", 'r', 'cp1251') as fr:
        referats_orig = fr.read()
        splitter = structuring_dict.get('referats splitter')
        referats_file_head = referats_orig.split(splitter)[0]

    with open("referats" + "_new.tex", 'w', newline='\n') as fw:
        fw.write(referats_file_head)
        for referat in referat_lol:
            entry = referat_to_string(referat)['referat_str']
            fw.write(entry)
    msg = 'Сборка файлов завершена'
    return {'msg': msg}
