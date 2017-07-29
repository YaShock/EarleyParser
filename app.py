from parse import *
import generated.grammar

g = generated.grammar.grammar
parser = earley.Parser(g)
inp = input()
while inp != 'quit':
    res = parser.parse(inp)
    for r in res:
        r.print()
        r.walk()
    inp = input()