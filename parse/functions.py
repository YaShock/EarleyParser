dict = {}
def Formula_140518124841952_fn(tree):
        tree.children[0].fn()


    
dict[140518124841952] = Formula_140518124841952_fn
def Expr_140518124955016_fn(tree):

        a = 0
        b = 0
    
        tree.children[0].fn()

        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    
dict[140518124955016] = Expr_140518124955016_fn
def Expr_140518124955072_fn(tree):

        a = 0
        b = 0
    
        tree.children[0].fn()
        tree.children[1] = None
        tree.children[2].fn()

        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    
dict[140518124955072] = Expr_140518124955072_fn
def Number_140518124955464_fn(tree):
        tree.children[0] = None

        return int(num.value)
    
dict[140518124955464] = Number_140518124955464_fn
