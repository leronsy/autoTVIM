import re

structuring_dict = dict([

    ('article beginning',
     '\\title{\\uppercase'),
    ('article ending',
     '\\end{thebibliography}'),

    ('input init_counters',
     '\\input{__init_counters__}\n'),
    ('input to_rus',
     '\\input{__to_rus__}\n'),

    ('markboth',
     '\\markboth'),
    ('medskip',
     '\\medskip'),
    ('bigskip',
     '\\bigskip'),

    ('authorinfo',
     '\\authorInfo'),

    ('referats splitter',
     '\\enlargethispage{4\\baselineskip}'),

    ('abstractline',
     '\\abstractLine{cm}{cm}\n\n'),

    # ('re word_dot_space',
    #  re.compile(r'(?P<full>(?P<word>\w*?\.)[^\w]*)')),

    ('re word_dot_space',
     re.compile(r'(?P<word>\w*?\.[^\w]*)')),
    ('re author',
     re.compile(r'\\author(?P<author_ru>{.+?}{.+?})')),
    ('re degree',
     re.compile(r'\W*(?P<full>(?P<degree>[кд])\.\W*?(?P<science>[А-Яа-яA-Za-z\-.]+\.)\W*?[н])\W*')),
    ('re abstract',
     re.compile(r'\\begin{abstract}{(?P<title>.+?)}\s*?{(?P<author>.+?)}\s*?(?P<abstract>.+?)\s*?\\end{abstract}',
                re.DOTALL)),
    ('re authorinfo',
     re.compile(r'\\authorInfo(?P<surname_name>{.+?})(?P<middlename>{.+?})(?P<post>{.+?})(?P<mail>{.+?})', re.DOTALL)),

    ('re addcontentsline',
     re.compile(r'\\addcontentsline{.+?}{.+?}{\\textbf{(?P<authors>.+?)}(?P<title>.+?)}')),

    ('re input init_counters',
     re.compile(r"(?P<input_init>\\input{__init_counters__})")),
    ('re input to_rus',
     re.compile(r"(?P<input_torus>\\input{__to_rus__})")),

    ('re title_author_ru',
     re.compile(r'\\begin{abstract}{(?P<title>.+?)}{(?P<author>.+?)}', re.DOTALL)),
    ('re title_author_en',
     re.compile(r'\\begin{abstractWithTitle}{(?P<title>.+?)}\s??{(?P<author>.+?)}', re.DOTALL)),

    ('re udc',
     re.compile(r'УДК:\s*?(?P<number>.+?)}')),

    ('re keywords ru',
     re.compile(r'Ключевые слова:\W*?{(?P<keywords>.+?)}', re.DOTALL)),

    ('re label Surname_begin',
     re.compile(r'(?P<begin_label>\\label{(?P<surname>[A-z-]+?)_begin})')),
    ('re label Surname_end',
     re.compile(r'(?P<end_label>\\label{(?P<surname>[A-z-]+?)_end})')),

])


correction_dict = dict([
    ('Длинное тире', (re.compile(r'(?P<pattern>\s*?~??---)'), '~---',)),
    ('Многоточие', (re.compile(r'(?P<pattern>\.\.\.)'), '\dots ',)),
])


science_dict = {
    'п.': 'p',
    'ф.-м.': 'fm',
    'ф-м.': 'fm',
    'т.': 't',
}


country_dict = {
    'РФ': '\\RU'
}
