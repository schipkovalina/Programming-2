import sqlite3
from pymystem3 import Mystem
import re


def search(str):
    # подключаемся к базе данных
    conn = sqlite3.connect('selskayapravda.db')

    answers = []
    c = conn.cursor()

    mystem = Mystem()
    lemSearchStr = ''.join(mystem.lemmatize(str))[:-1]

    dataBaseAsk = ('%' + lemSearchStr + '%', lemSearchStr + '%',
                   '%' + lemSearchStr)

    for row in c.execute(
            "select * from texts where mystem_content like ? "
            "or mystem_content like ? or mystem_content like ?", dataBaseAsk):
        ask = '.*?(' + str + ')'
        disc = re.search(ask, row[2])
        if disc:
            disc = disc.group()
        answers.append({'url': row[3], 'title': row[0], 'disc': disc})

    conn.close()
    return answers
