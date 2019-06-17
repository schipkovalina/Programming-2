from flask import Flask, render_template, request
import corpus_maker
app = Flask(__name__)
corpus_maker.corpora_maker()


@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ''
    if request.method == "POST":
        word = request.form['word']
        the_last_letters, clean_word = corpus_maker.last_letters(word)
        original_line, line, clean_word = corpus_maker.rhyme_match(the_last_letters, clean_word)
        answer = corpus_maker.answer_maker(original_line, line, clean_word)
    return render_template('index.html', answer=answer)


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
