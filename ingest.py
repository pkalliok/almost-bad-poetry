
import structure
import requests, re
from html import unescape
from pickle import load, dump

def file_words(f):
    return (w for line in f for w in line.split())

def clauses(words):
    memory = []
    for w in words:
        memory.append(w)
        to_pop = 0
        for start in range(len(memory)):
            clause = ' '.join(memory[start:])
            c_struct = structure.rhythm_structure(clause)
            if len(c_struct[0]) >= 4: yield (clause, c_struct)
            if len(c_struct[0]) >= 16: to_pop += 1
        memory = memory[to_pop:]

def load_data(filename):
    return dict(db=list(clauses(file_words(open(filename)))), used=set())

tag_re = re.compile(r'''<([^>]|"[^"]*"|'[^']*')*>''')
def only_text(html): return unescape(tag_re.sub(' ', html))

def url_words(url):
    return only_text(requests.get(url).text).split()

def load_url(url):
    return dict(db=list(clauses(url_words(url))), used=set())

def save_state(state, filename):
    dump(state['used'], open(filename, "wb"))

def load_state(state, filename):
    try: f = open(filename, "rb")
    except FileNotFoundError: return state
    try: state['used'] |= load(f)
    except EOFError: return state
    return state

