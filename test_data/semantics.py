sum = 0
product = 0
term = 0
operator_expr = None
operator_term = None

def expr_enter(children):
    print('expr enter')

def expr_exit(children):
    print('expr exit')
    global sum
    print('result = %s' % sum)

def sum_enter(children):
    print('sum enter')

def sum_exit(children):
    print('sum exit')
    global product
    global sum
    global operator_expr
    if operator_expr == '+':
        sum += product
    else:
        sum -= product
    print(sum)

def sum_unary_enter(children):
    print('unary sum enter')

def sum_unary_exit(children):
    print('unary sum exit')
    global sum
    sum = product
    print(sum)

def product_enter(children):
    print('binary product enter')

def product_exit(children):
    print('binary product exit')
    global product
    global term
    global operator_term
    if operator_term == '*':
        product *= term
    else:
        product /= term
    print(product)

def product_unary_enter(children):
    print('unary product enter')

def product_unary_exit(children):
    print('unary product exit')
    global product
    product = term
    print(product)

def number_enter(children):
    print('number enter')

def number_exit(children):
    print('number exit')
    global term
    term = int(str(children[0].data))
    print(term)

def operator_expr_enter(children):
    pass

def operator_expr_exit(children):
    global operator_expr
    operator_expr = repr(children[0].data)

def operator_prod_enter(children):
    pass

def operator_prod_exit(children):
    global operator_term
    operator_term = repr(children[0].data)

def parentheses_enter(children):
    pass

def parentheses_exit(children):
    pass