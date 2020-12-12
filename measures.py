
from structure import rhythm_structure, rhyme_structure
from similarity import find_most_similar_unused, last_word

limerick_measure = (
    [[(1.0, 0.4), (0.0, 0.7), (1.0, 0.4), (0.0, 0.7),
        (1.0, 0.4), (0.0, 0.7), (1.0, 1.0)],
     [(1.0, 0.6), (0.0, 0.4), (1.0, 0.4), (0.0, 0.4)]],
    [0, 0, 1, 1, 0])

nelidaktyyli = (
    [[(1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0), (0.5, 1.0)],
     [(1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0), (0.5, 1.0)],
     [(1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0), (0.5, 1.0)]],
    [0, 1, 1, 0, 2, 2, 0])

tasaruno = (
    [[(1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0)],
     [(0.0, 0.4), (0.0, 0.4), (1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0), (0.5, 1.0)],
     [(1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0)],
     [(0.0, 0.4), (0.0, 0.4), (1.0, 0.9), (0.0, 0.4), (0.0, 0.4),
      (1.0, 0.9), (0.0, 0.4), (0.0, 0.4), (1.0, 1.0), (0.5, 1.0)]],
    [0, 1, 0, 1, 2, 3, 2, 3])

def generate_poem(measure, clause_db):
    rhythms, succession = measure
    rhymes = {}
    used_end_words = set()
    def generate_clause(stanza_class):
        rhyme = rhymes.get(stanza_class, [('',)*3]*3)
        dist, clause = find_most_similar_unused(
                (rhythms[stanza_class], rhyme), clause_db, used_end_words)
        used_end_words.add(last_word(clause))
        if stanza_class not in rhymes:
            rhymes[stanza_class] = rhyme_structure(clause)
        return clause
    return map(generate_clause, succession)

