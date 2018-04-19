from functools import wraps


def retry(function):
    @wraps(function)
    def _retry(*args, **kwargs):
        try:
            reply = function(*args, **kwargs)
            #print("Ответ: ", reply['msg'])
            return reply
        except ZeroDivisionError as msg:
            print("ERROR:\t", msg)
        except:
            print("ERROR:\t unknown error")

    return _retry


def decor1(function):
    @wraps(function)
    def _decor_main(*args, **kwargs):

        print("START:\t", function.__name__)

        answer = function(*args, **kwargs)

        print('ANS:\t', answer['msg'])
        print("END:\t", function.__name__)
        print("=" * 40)

        return answer

    return _decor_main


def decor2(function):
    @wraps(function)
    def _decor_file(*args, **kwargs):

        print("|\tSTART:\t", function.__name__)

        answer = function(*args, **kwargs)

        print('|\tANS:\t', answer['msg'])
        print('|\tEND:\t', function.__name__)
        print("-" * 40)

        return answer

    return _decor_file


def decor3(function):
    @wraps(function)
    def _decor_text(*args, **kwargs):
        #print("|\t|\tSTART:\t", function.__name__)
        #print()
        answer = function(*args, **kwargs)

        print('|\t|\t'+function.__name__+'ANS:', answer['msg'],"\tEND:")#, function.__name__)

        return answer

    return _decor_text

def decor4(function):
    @wraps(function)
    def _decor_text(*args, **kwargs):
        #print("|\t|\t|\tSTART:\t", )

        answer = function(*args, **kwargs)

        print('|\t|\t|\t',function.__name__,' ANS:\t', answer['msg'])

        return answer

    return _decor_text