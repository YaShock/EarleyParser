sum = 0
product = 0
term = 0
operator = None

def expr_enter(args):
	print('expr enter')

def sum_unary_enter(args):
    print('unary sum enter')

def sum_enter(args):
    print('sum enter')

def product_unary_enter(args):
	print('unary product enter')

def product_enter(args):
    print('binary product enter')

def terminal_enter(args):
	print('terminal enter')

def expr_exit(args):
	print('expr exit')
	global sum
	print('result = %s' % sum)

def sum_exit(args):
    print('sum exit')
    global expr
    global sum
    sum += product
    print(sum)

def sum_unary_exit(args):
    print('unary sum exit')
    global sum
    sum = product
    print(sum)

def product_exit(args):
    print('binary product exit')
    global product
    global term
    product *= term
    print(product)

def product_unary_exit(args):
	print('unary product exit')
	global product
	product = term
	print(product)

def terminal_exit(args):
	print('terminal exit')
	global term
	term = int(str(args[0].data))
	print(term)