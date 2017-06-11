from parse import *

grammar = grammar.Grammar()
cb = context.ContextBuilder(grammar)
cb.build()
parser = earley.Parser(grammar)

inp = input()
while inp != 'quit':
    lst = parser.parse(inp)
    for t in lst:
        t.print()
        context.walk_tree(t)
    inp = input()