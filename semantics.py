sum = 0
product = 0
term = 0
operator = None

def expr_enter(args):
	print('expr enter')
	# print(args[0].data)

def sum_unary_enter(args):
    print('unary sum enter')
    # print(args[0].data)
    # print(args[2].data)

def sum_enter(args):
    print('sum enter')
    # print(args[0].data)
    # print(args[2].data)

def product_unary_enter(args):
	print('unary product enter')
	# print(args[0].data)

def product_enter(args):
    print('binary product enter')
    # print(args[0].data)
    # print(args[2].data)

def terminal_enter(args):
	print('terminal enter')
	# print(args[0].data)

def expr_exit(args):
	print('expr exit')
	global sum
	print('result = %s' % sum)
	# print(args[0].data)

def sum_exit(args):
    print('sum exit')
    global expr
    global sum
    sum += product
    print(sum)
    # print(args[0].data)
    # print(args[2].data)

def sum_unary_exit(args):
    print('unary sum exit')
    global sum
    sum = product
    print(sum)
    # print(args[0].data)
    # print(args[2].data)

def product_exit(args):
    print('binary product exit')
    global product
    global term
    product *= term
    print(product)
    # print(args[0].data)
    # print(args[2].data)

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