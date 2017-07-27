from parse import *

text = ''
with open('generated/grammar.cf', 'r') as grammar_file:
    text = grammar_file.read()

mg = metagrammar.Metagrammar()
g = mg.process_grammar(text, 'generated/functions.py')
parser = earley.Parser(g)    
res = parser.parse(input())
for r in res:
    r.print()
    r.walk()