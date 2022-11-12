from flask import Flask, render_template
from flask import request, redirect, Markup
import os, responder

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATAFILE = BASE_DIR + '/data/board.txt'
DATAFILE2 = BASE_DIR + '/data/words.txt'
DATAFILE3 = BASE_DIR + '/data/input.txt'

@app.route('/')
def index():
    text = ''
    if os.path.exists(DATAFILE):
        with open(DATAFILE, 'rt',encoding='utf-8') as f:
            text = f.read()
            
    return render_template('write_form.html',
            board = text)

@app.route('/write', methods=['POST'])
def write():
    if 'msg' in request.form:
        msg = str(request.form['msg'])
        with open(DATAFILE3, 'wt', encoding='utf-8')as f:
            f.write(msg)
        msg2 = msg + '\n'
        if os.path.exists(DATAFILE):
            with open(DATAFILE,'at', encoding='utf-8')as f:
                f.write(msg2)
        else:
            with open(DATAFILE,'wt', encoding='utf-8')as f:
                f.write(msg2)
    return redirect('/write_re')

@app.route('/write_re')
def write_re():
    re_msg = '>>>' + responder.dialogue() + '\n'
    with open(DATAFILE, 'at',encoding='utf-8')as f:
        f.write(re_msg)
    return redirect('/')
    
@app.route('/delete')
def delete():
    if os.path.exists(DATAFILE):
        os.remove(DATAFILE)
    return redirect('/')

@app.template_filter('linebreak')
def linebreak_filter(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;')\
        .replace('>', '&gt;').replace('\n', '<br>')
    return Markup(s)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
