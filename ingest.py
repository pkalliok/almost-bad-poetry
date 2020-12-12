
import structure

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

