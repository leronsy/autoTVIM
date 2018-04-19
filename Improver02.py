from structuring import structure
from correction import correct
from assembly import assemble
from stream_tee import *
import time
import sys


def main(c=True, s=True, a=True, file='file_list.txt', debug=True):
    """
    Определяем пути для записи вывода с помощью stream_tee.
    :param c:
    :param s:
    :param a:
    :param file:
    :param debug:
    :return:
    """
    # 1
    time_now = time.strftime("%y.%m.%d %H-%M")
    logfile = open("./logs/log" + time_now + ".txt", "w+")
    LastLog = open("./logs/_LastLog.txt", "w+")
    sys.stdout = stream_tee(sys.stdout, logfile, LastLog)
    # 2
    if c:
        correct(file, debug)
    # 3
    if s:
        structure(file, debug)
    # 4
    if a:
        assemble(file, debug)
    return


main(True, True, False)
