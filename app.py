import earley, grammar, context

file = open('grammar.cf')
grammar = grammar.Grammar()
cb = context.ContextBuilder(grammar)
cb.read_file(file)
file.close()
parser = earley.Parser(grammar)

module = __import__('generated')
module.create()

for rule in grammar.rules:
    d = module.dict[id(rule)]
    rule.fn_enter = d[0]
    rule.fn_exit = d[1]

inp = input()
while inp != 'quit':
    lst = parser.parse(inp)
    for t in lst:
        t.print()
        context.walk_tree(t)
    inp = input()