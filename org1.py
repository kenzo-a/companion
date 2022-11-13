from flask import Flask, render_template
from flask import request, redirect, Markup
import os, random, re

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATAFILE = BASE_DIR + '/data/board.txt'
DATAFILE2 = BASE_DIR + '/data/words.txt'
DATAFILE3 = BASE_DIR + '/data/input.txt'
DATAFILE4 = BASE_DIR + '/data/pattern.txt'


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
    re_msg = '>>>' + dialogue() + '\n'
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

def dialogue():
    x = random.randint(1, 100)

    if(x <= 76):
        return pattern_responder()
    if(77 <= x <= 90):
        return random_responder()
    if(91 <= x <= 100):
        return repeat_responder()

def pattern_responder():
    with open(DATAFILE3, 'rt', encoding='utf-8')as f:
        inpu= f.read()
        
    pfile = open(DATAFILE4, 'rt', encoding = 'utf-8')
    p_lines = pfile.readlines()
    pfile.close()

    new_lines = []
    for line in p_lines:
        str = line.rstrip('\n')
        if (str!=''):
            new_lines.append(str)

    pattern = {}
    for line in new_lines:
        ptn, prs = line.split('\t')
        pattern.setdefault('pattern', []).append(ptn)
        pattern.setdefault('phrases', []).append(prs)

    for ptn, prs in zip(
        pattern['pattern'],
        pattern['phrases']):

        m = re.search(ptn, inpu)
        if m:
            resp = random.choice(prs.split('|'))
            return re.sub('%match%', m.group(), resp)
    return random_responder()

def random_responder():
    with open(DATAFILE3, 'rt', encoding='utf-8')as f:
        inpu = f.read()

    rfile = open(DATAFILE2, 'rt', encoding = 'utf-8')
    r_lines = rfile.readlines()
    rfile.close()

    rando = []
    for line in r_lines:
        str = line.rstrip('\n')
        if (str!=''):
            rando.append(str)
    if not inpu in rando:
        inp = inpu + '\n'
        with open(DATAFILE2, 'at', encoding='utf-8')as f:
            f.write(inp)
            
    return random.choice(rando)

def repeat_responder():
    with open(DATAFILE3, 'rt', encoding = 'utf-8')as f:
        inpu = f.read()
    return '{}ですね'.format(inpu)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
