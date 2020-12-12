
import re

nucleus_def = r'(aa|ee|oo|ää|öö|[aeiou]u|[äeiöy]y|uo|yö|ie|[aieouyåäö]i?)'
nucleus_re = re.compile(nucleus_def, re.IGNORECASE)
consonant_def = r'[bcdfghjklmnpqrstvwxz]'
start_re = re.compile(r'( ?){}*{}'.format(consonant_def, nucleus_def),
        re.IGNORECASE)
syllable_re = re.compile(r'({}*){}([lrmnh]?[ptks]?(?![aeiouyåäö]))?'.format(
    consonant_def, nucleus_def), re.IGNORECASE)

def rhythm_structure(clause):
    return (list(zip(stress_structure(clause), length_structure(clause))),
            rhyme_structure(clause))

def fix_weights(weights):
    return [min(1.0, max(0.0,
                cur + 0.5 * (prev < 0.2 and next < 0.2) - (next > 0.7)))
            for prev, cur, next in
            zip([0.0]+weights[:-1], weights, weights[1:]+[0.0])]

def stress_structure(clause):
    return fix_weights([len(startp) + 0.5*len(nucl) - 0.5
        for startp, nucl in start_re.findall(clause)])

def length_structure(clause):
    return [min(1.0, (len(cons)>1)*0.1 + len(nucl)*0.8 + len(tail)*0.4 - 0.8)
            for cons, nucl, tail in syllable_re.findall(clause)]

def rhyme_structure(clause):
    return syllable_re.findall(clause)[-3:]

