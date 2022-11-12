import random, os, re

BASE_DIR = os.path.dirname(__file__)
DATAFILE2 = BASE_DIR + '/data/words.txt'
DATAFILE3 = BASE_DIR + '/data/input.txt'
DATAFILE4 = BASE_DIR + '/data/pattern.txt'

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


    
    
