from functools import wraps


def decor1(func):
    @wraps(func)
    def _decor_main(*args, **kwargs):
        print("START:\t", func.__name__)

        answer = func(*args, **kwargs)

        print('ANS:\t', answer['msg'])
        print("END:\t", func.__name__)
        print("=" * 40)

        return answer

    return _decor_main


def decor2(func):
    @wraps(func)
    def _decor_file(*args, **kwargs):
        print("|\tSTART:\t", func.__name__)

        answer = func(*args, **kwargs)

        print('|\tANS:\t', answer['msg'])
        print('|\tEND:\t', func.__name__)
        print("-" * 40)

        return answer

    return _decor_file


def decor3(func):
    @wraps(func)
    def _decor_text(*args, **kwargs):
        # print("|\t|\tSTART:\t", function.__name__)
        # print()
        answer = func(*args, **kwargs)

        print('|\t|\t' + func.__name__ + 'ANS:', answer['msg'], "\tEND:")  # , func.__name__)

        return answer

    return _decor_text


def decor4(func):
    @wraps(func)
    def _decor_text(*args, **kwargs):
        # print("|\t|\t|\tSTART:\t", )

        answer = func(*args, **kwargs)

        print('|\t|\t|\t', func.__name__, ' ANS:\t', answer['msg'])

        return answer

    return _decor_text
