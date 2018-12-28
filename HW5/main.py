from flask import Flask
from flask import request, render_template
import WorkWithDataBase

app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        searchString = request.args['search_string']
        print(searchString)
        answers = WorkWithDataBase.search(searchString)
        return render_template('index.html',
                               answers=answers,
                               field=searchString)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
