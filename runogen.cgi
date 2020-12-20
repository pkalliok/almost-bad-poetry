#!/usr/bin/env python

from ingest import load_url, save_state, load_state
from measures import measure_map, generate_poem
import html

STATE_FILE = 'used_stanzas.pickle'

HTTP_START = """Content-type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="fi">
<head><title>{} - runogeneraattori</title></head>
<body>
"""
HTTP_END = "</body></html>"

def show_form(form):
    print(HTTP_START.format('Anna aineisto'))
    print('<p>Teen runon antamastasi tekstistä. Täytä nämä tiedot:</p>')
    print('<form method=GET><fieldset><legend>Runoaineisto</legend>')
    print('<p><label for=url>Www-sivu, josta teen runon:</label>')
    print('<input type=text name=url id=url value="https://fi.wikipedia.org/wiki/Grimmin_sadut"></p>')
    print('<p><label for=tee_runo>Runomitta, jota yritän noudattaa:</label>')
    print('<select name=tee_runo id=tee_runo>')
    print('<option value=limerikki>Limerikki - A, A, B, B, A</option>')
    print('<option value=nelidaktyyli>Daktyyli - Humppapa, pumppapa</option>')
    print('<option value=perusruno>Perusriimi heksametriin</option>')
    print('</select></p></fieldset>')
    print('<input type=submit value="Runo tänne!"></form>')
    print(HTTP_END)

def make_poem(measure, corpus_url):
    if measure not in measure_map: raise ValueError("unknown measure")
    state = load_url(corpus_url)
    load_state(state, STATE_FILE)
    print(HTTP_START.format("{} numero {}".format(measure, len(state['used']))))
    print('<blockquote><cite>')
    for line in generate_poem(measure_map[measure], state, {'ei'}):
        print(html.escape(line) + '<br>')
    print('</cite></blockquote>')
    print(HTTP_END)
    save_state(state, STATE_FILE)

def handle_request(form):
    if 'tee_runo' in form:
        make_poem(form.getfirst('tee_runo'), form.getfirst('url'))
    else: show_form(form)

if __name__ == '__main__':
    import cgi
    try: handle_request(cgi.FieldStorage())
    except: cgi.print_exception()

