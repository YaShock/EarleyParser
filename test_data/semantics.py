sum = 0
product = 0
term = 0
operator_expr = None
operator_term = None

def expr_enter(args):
    print('expr enter')

def expr_exit(args):
    print('expr exit')
    global sum
    print('result = %s' % sum)

def sum_enter(args):
    print('sum enter')

def sum_exit(args):
    print('sum exit')
    global product
    global sum
    global operator_expr
    if operator_expr == '+':
        sum += product
    else:
        sum -= product
    print(sum)

def sum_unary_enter(args):
    print('unary sum enter')

def sum_unary_exit(args):
    print('unary sum exit')
    global sum
    sum = product
    print(sum)

def product_enter(args):
    print('binary product enter')

def product_exit(args):
    print('binary product exit')
    global product
    global term
    global operator_term
    if operator_term == '*':
        product *= term
    else:
        product /= term
    print(product)

def product_unary_enter(args):
    print('unary product enter')

def product_unary_exit(args):
    print('unary product exit')
    global product
    product = term
    print(product)

def number_enter(args):
    print('number enter')

def number_exit(args):
    print('number exit')
    global term
    term = int(str(args[0].data))
    print(term)

def operator_expr_enter(args):
    pass

def operator_expr_exit(args):
    global operator_expr
    operator_expr = repr(args[0].data)

def operator_prod_enter(args):
    pass

def operator_prod_exit(args):
    global operator_term
    operator_term = repr(args[0].data)