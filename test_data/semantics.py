def expr_enter(node):
    print('expr enter')

def expr_exit(node):
    print('expr exit')
    node.value = node[0].value
    print('result = %s' % node.value)

def sum_enter(node):
    print('sum enter')

def sum_exit(node):
    print('sum exit')
    if node[1].value == '+':
        node.value = node[0].value + node[2].value
    else:
        node.value = node[0].value - node[2].value
    print(node.value)

def sum_unary_enter(node):
    print('unary sum enter')

def sum_unary_exit(node):
    print('unary sum exit')
    node.value = node[0].value
    print(node.value)

def product_enter(node):
    print('binary product enter')

def product_exit(node):
    print('binary product exit')
    if node[1].value == '*':
        node.value = node[0].value * node[2].value
    else:
        node.value = node[0].value / node[2].value
    print(node.value)

def product_unary_enter(node):
    print('unary product enter')

def product_unary_exit(node):
    print('unary product exit')
    node.value = node[0].value
    print(node.value)

def num_factor_enter(node):
    pass

def num_factor_exit(node):
    print('factor exit')
    node.value = node[0].value
    print(node.value)

def number_enter(node):
    pass

def number_exit(node):
    print('number exit')
    node.value = node[0].value * 10 + node[1].value
    print(node.value)

def number_digit_enter(node):
    print('number enter')

def number_digit_exit(node):
    print('number digit exit')
    node.value = node[0].value
    print(node.value)

def digit_enter(node):
    pass

def digit_exit(node):
    print('digit exit')
    node.value = int(str(node[0].data))
    print(node.value)

def parentheses_enter(node):
    pass

def parentheses_exit(node):
    print('parentheses exit')
    node.value = node[1].value
    print(node.value)

def operator_expr_enter(node):
    pass

def operator_expr_exit(node):
    node.value = repr(node[0].data)

def operator_prod_enter(node):
    pass

def operator_prod_exit(node):
    node.value = repr(node[0].data)
