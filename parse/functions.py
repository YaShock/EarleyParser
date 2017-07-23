dict = {}
def Formula_140563373374376_fn(tree):
        print('0 ' + repr(tree.children[0].data))


    
dict[140563373374376] = Formula_140563373374376_fn
def Expr_140563373409616_fn(tree):

        a = 0
        b = 0
        op = None
    
        print('0 ' + repr(tree.children[0].data))

        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    
dict[140563373409616] = Expr_140563373409616_fn
def Expr_140563373409784_fn(tree):

        a = 0
        b = 0
        op = None
    
        print('0 ' + repr(tree.children[0].data))
        print('1 ' + repr(tree.children[1].data))
        print('2 ' + repr(tree.children[2].data))

        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    
dict[140563373409784] = Expr_140563373409784_fn
def Number_140563373410064_fn(tree):
        print('0 ' + repr(tree.children[0].data))

        return 0
    
dict[140563373410064] = Number_140563373410064_fn
