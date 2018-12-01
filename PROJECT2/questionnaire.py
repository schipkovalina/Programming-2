from flask import Flask
from flask import render_template, url_for, request, redirect
import work_with_files

app = Flask(__name__)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def index():
    urls = {'Main': url_for('index'),
            'Take a survey': url_for('form'),
            'Show stats': url_for('stats'),
            'Get json': url_for('json'),
            'Search': url_for('search'), }
    return render_template('index.html', urls=urls)


@app.route('/form')
def form():
    if request.args:
        first_name = request.args['first_name']
        last_name = request.args['last_name']
        lang = request.args['language']
        gender = ''
        if 'gender' in request.args:
            gender = request.args['gender']
        ans1 = request.args['q1']
        ans2 = request.args['q2']
        ans3 = request.args['q3']
        ans4 = request.args['q4']
        ans5 = request.args['q5']
        ans6 = request.args['q6']
        que = [first_name, last_name, gender,
               lang, ans1, ans2, ans3, ans4, ans5, ans6]
        if '' in que:
            return render_template('form.html', err=True,
                                   url='/', text='return to main')
        work_with_files.write_to_csv(que[2:])
        work_with_files.create_user(que)
        return redirect(url_for('thx'))
    return render_template('form.html', err=False)


@app.route('/thx')
def thx():
    return render_template('thx.html', url='/', text='main')


@app.route('/stats')
def stats():
    work_with_files.creating_graph()
    return render_template('stats.html', url='/', text='main')


@app.route('/json')
def json():
    return render_template('json.html', users=work_with_files.get_json())


@app.route('/search')
def search():
    if request.args:
        search_text = request.args['search']
        gen_list = {'male': True if 'male' in request.args else False,
                    'female': True if 'female' in request.args else False,
                    'other': True if 'other' in request.args else False}
        res = work_with_files.search(search_text, gen_list)
        return render_template('results.html', list=res, url='/', text='main')
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
