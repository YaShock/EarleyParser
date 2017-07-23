dict = {}
def Expr_140282372764560_fn(tree):

        a = 0
        b = 0
        op = None
    
        a = tree.children[0].fn(tree.children[0])

        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    
dict[140282372764560] = Expr_140282372764560_fn
def Expr_140282372764952_fn(tree):

        a = 0
        b = 0
        op = None
    
        a = tree.children[0].fn(tree.children[0])
        op = tree.children[1]
        b = tree.children[2].fn(tree.children[2])

        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    
dict[140282372764952] = Expr_140282372764952_fn
def Number_140282372763720_fn(tree):
        num = tree.children[0]

        return int(num.value)
    
dict[140282372763720] = Number_140282372763720_fn
