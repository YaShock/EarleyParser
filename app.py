import earley, grammar, context, semantics

def walk_tree(tree):
    #[c for c in tree.children if c is not child]
    #if hasattr(tree, 'fn_enter') and tree.fn_enter:
        #print([c.data for c in tree.children if not grammar.is_terminal(c.data)])
    if tree.fn_enter:
        tree.fn_enter([c for c in tree.children])
    for child in tree.children:
        walk_tree(child)
    if tree.fn_exit:
        tree.fn_exit([c for c in tree.children])

file = open('math.cf')
grammar = grammar.Grammar()
cb = context.ContextBuilder(grammar)
cb.read_file(file)
file.close()
parser = earley.Parser(grammar)

# cb.parse_rule('P', 'S', semantics.expr_enter, semantics.expr_exit)
# cb.parse_rule('S', 'S \'+\' M', semantics.sum_enter, semantics.sum_exit)
# cb.parse_rule('S', 'M', semantics.sum_unary_enter, semantics.sum_unary_exit)
# cb.parse_rule('M', 'M \'*\' T', semantics.product_enter, semantics.product_exit)
# cb.parse_rule('M', 'T', semantics.product_unary_enter, semantics.product_unary_exit)
# cb.parse_rule('T', '\'1\' | \'2\' | \'3\' | \'4\' | \'5\' | \'6\' | \'7\' | \'8\' | \'9\' | \'0\'', semantics.terminal_enter, semantics.terminal_exit)

module = __import__('generated')
module.create()

# for key, value in module.dict.items():
#     print('%s %s' % (key, value))

for rule in grammar.rules:
    d = module.dict[id(rule)]
    rule.fn_enter = d[0]
    rule.fn_exit = d[1]
    #print('%i %s %s' % (id(rule), d[0], d[1]))

lst = parser.parse('2 * 4 + 3 * 3 + 10')
for t in lst:
    t.print()
    walk_tree(t)

# print()

# lst = parser.parse('load whatever')
# for t in lst:
#     t.print()

# lst = parser.parse("get,terms;frequency,between;1.5;and,4.8")
# for t in lst:
#     t.print()

# lst = parser.parse("delete words : lel asd 20")
# for t in lst:
#     t.print()