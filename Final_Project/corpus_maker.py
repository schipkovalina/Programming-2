import re
import gensim
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

corpus_num = {}
corpus_word = {}
corpus_last_num = {}
corpus_last_word = {}


def corpora_maker():
    with open('brodsky.txt', 'r', encoding='utf-8') as file:
        text = file.readlines()
        n = 0
        for line in text:
            line = re.sub('[:,.?!;]', '', line)
            line = re.sub('"', '', line)
            line = re.sub('\n', '', line)
            line = re.sub('\d', '', line)
            line = re.sub('J', 'ё', line)
            if line == '':
                continue
            test = re.sub('[^А-Яа-яЁё]', '', line)
            if test == '':
                continue
            last_word = line.split()[-1]
            n += 1
            corpus_num.update({n:line})
            corpus_word.update(({line:n}))
            corpus_last_num.update({n:last_word})
            corpus_last_word.update({last_word:n})
    m = 'model.bin'
    global model
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)


def last_letters(word):
    word = word.lower()
    clean_word = re.sub('[^А-Яа-яЁё]', '', word)
    the_last_letters = word[-2:]
    return the_last_letters, clean_word


def rhyme_match(the_last_letters, clean_word):
    no_rhyme = 'yes'
    n = 0
    last_words = list(corpus_last_word.keys())
    while no_rhyme == 'yes':
        i = list(corpus_last_word.keys())[n]
        if clean_word not in last_words:
            no_rhyme = 'no'
            original_line = ''
            line = 'Для этого слова рифмы не нашлось'
            break
        if i == clean_word:
            original_line_num = corpus_last_word[i]
            original_line = corpus_num[original_line_num]
            previous_line_num = original_line_num - 1
            next_line_num = original_line_num + 1
            prev_word = corpus_last_num[previous_line_num]
            next_word = corpus_last_num[next_line_num]
            if prev_word[-2:] == the_last_letters:
                line = corpus_num[previous_line_num]
                no_rhyme = 'no'
            elif next_word[-2:] == the_last_letters:
                line = corpus_num[next_line_num]
                no_rhyme = 'no'
            else:
                previous_line_num = original_line_num - 2
                next_line_num = original_line_num + 2
                prev_word = corpus_last_num[previous_line_num]
                next_word = corpus_last_num[next_line_num]
                if prev_word[-2:] == the_last_letters:
                    line = corpus_num[previous_line_num]
                    no_rhyme = 'no'
                elif next_word[-2:] == the_last_letters:
                    line = corpus_num[next_line_num]
                    no_rhyme = 'no'
                else:
                    no_rhyme = 'yes'
                    n += 1
        else:
            if n == len(list(corpus_last_word.keys())) - 1:
                original_line = ''
                line = 'На это слово рифмы не нашлось'
                no_rhyme = 'no'
            else:
                no_rhyme = 'yes'
                n += 1
    return original_line, line, clean_word


# cotags are taken from nevmeandr
def answer_maker(original_line, line, clean_word):
    cotags = {'ADJF': 'ADJ',  # pymorphy2: word2vec
              'ADJS': 'ADJ',
              'ADVB': 'ADV',
              'COMP': 'ADV',
              'GRND': 'VERB',
              'INFN': 'VERB',
              'NOUN': 'NOUN',
              'PRED': 'ADV',
              'PRTF': 'ADJ',
              'PRTS': 'VERB',
              'VERB': 'VERB',
              'NPRO': 'NOUN'}
    if original_line == '':
        test = re.sub('[^А-Яа-яЁё]', '', clean_word)
        if test == '':
            answer = 'Введите другое слово, это не очень подходит'
        else:
            answer = 'К сожалению, рифм не нашлось, зато есть синонимы из русскоязычных новостей! ' + '\n'
            analysis = morph.parse(clean_word)[0]
            pos = analysis.tag.POS
            try:
                pos = cotags[pos]
                syn = morph.parse(clean_word)[0][2] + '_' + str(pos)
                if syn in model:
                    for synonym in model.wv.most_similar(syn, topn=3):
                        if synonym[0].split('_')[0] != clean_word:
                            answer += synonym[0].split('_')[0] + ', '
                else:
                    answer = 'Нет, ни рифм, ни синонимов для этого слова'
            except KeyError:
                answer = 'Введите другое слово, это не очень подходит'
    else:
        answer = original_line + '\n' + line
    print(answer)
    return answer


def main():
    corpora_maker()
    word = 'sss'
    while word != 'stop':
        print('insert')
        word = input()
        the_last_letters, clean_word = last_letters(word)
        original_line, line, clean_word = rhyme_match(the_last_letters, clean_word)
        answer_maker(original_line, line, clean_word)


if __name__ == '__main__':
    main()

