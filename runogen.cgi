#!/usr/bin/env python3
# coding: utf-8

from ingest import load_url, save_state, load_state
from measures import measure_map, generate_poem
import html, sys

STATE_FILE = 'used_stanzas.pickle'

HTTP_START = """Content-type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="fi">
<head><title>{} - runogeneraattori</title></head>
<body>
"""
HTTP_END = "</body></html>"

def p(html): sys.stdout.buffer.write((html + '\n').encode('utf-8'))

def show_form(form):
    p(HTTP_START.format('Anna aineisto'))
    p('<p>Teen runon antamastasi tekstistä. Täytä nämä tiedot:</p>')
    p('<form method=GET><fieldset><legend>Runoaineisto</legend>')
    p('<p><label for=url>Www-sivu, josta teen runon:</label>')
    p('<input type=text name=url id=url value="https://fi.wikipedia.org/wiki/Grimmin_sadut"></p>')
    p('<p><label for=tee_runo>Runomitta, jota yritän noudattaa:</label>')
    p('<select name=tee_runo id=tee_runo>')
    p('<option value=limerikki>Limerikki - A, A, B, B, A</option>')
    p('<option value=nelidaktyyli>Daktyyli - Humppapa, pumppapa</option>')
    p('<option value=perusruno>Perusriimi heksametriin</option>')
    p('</select></p></fieldset>')
    p('<input type=submit value="Runo tänne!"></form>')
    p('<p>(tässä saattaa kestää....)</p>')
    p(HTTP_END)

def make_poem(measure, corpus_url):
    if measure not in measure_map: raise ValueError("unknown measure")
    p(HTTP_START.format(measure.capitalize() + ' sinulle'))
    p('<p>(tässä saattaa kestää....)</p>')
    state = load_url(corpus_url)
    load_state(state, STATE_FILE)
    p('<p>Tässä runosi, ole hyvä!</p>')
    p('<blockquote><cite>')
    for line in generate_poem(measure_map[measure], state, {'ei', 'iii'}):
        p(html.escape(line) + u'<br>')
    p('</cite></blockquote>')
    p(HTTP_END)
    save_state(state, STATE_FILE)

def handle_request(form):
    if 'tee_runo' in form:
        make_poem(form.getfirst('tee_runo'), form.getfirst('url'))
    else: show_form(form)

if __name__ == '__main__':
    import cgi
    try: handle_request(cgi.FieldStorage())
    except: cgi.print_exception()

