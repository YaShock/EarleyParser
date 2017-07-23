dict = {}
def Formula_140684592426064_fn(tree):
        e = tree.children[0].fn(tree.children[0])

        print(e)
    
dict[140684592426064] = Formula_140684592426064_fn

def Num_140684592426568_fn(tree):
        return tree.children[0].data.value

dict[140684592426568] = Num_140684592426568_fn

def Operator_140684592533800_fn(tree):
        return tree.children[0].data.value

dict[140684592533800] = Operator_140684592533800_fn

def Operator_140684592534136_fn(tree):
        return tree.children[0].data.value

dict[140684592534136] = Operator_140684592534136_fn

def Expr_140684592535088_fn(tree):

        a = 0
        b = 0
        op = None
    
        a = tree.children[0].fn(tree.children[0])

        if op is None or op == '+':
            return a+b
        else:
            return a-b
    
dict[140684592535088] = Expr_140684592535088_fn

def Expr_140684592535368_fn(tree):

        a = 0
        b = 0
        op = None
    
        a = tree.children[0].fn(tree.children[0])
        op = tree.children[1].fn(tree.children[1])
        b = tree.children[2].fn(tree.children[2])

        if op is None or op == '+':
            return a+b
        else:
            return a-b
    
dict[140684592535368] = Expr_140684592535368_fn

def Number_140684592535648_fn(tree):
        num = tree.children[0].fn(tree.children[0])

        return int(num)
    
dict[140684592535648] = Number_140684592535648_fn

