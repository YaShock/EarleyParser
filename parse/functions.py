dict = {}
def Formula_139696158248016_fn(tree):
        e = tree.children[0].fn(tree.children[0])

        print(e)
    
dict[139696158248016] = Formula_139696158248016_fn

def Num_139696158248520_fn(tree):
        return tree.children[0].data.value

dict[139696158248520] = Num_139696158248520_fn

def Operator_139696158359848_fn(tree):
        return tree.children[0].data.value

dict[139696158359848] = Operator_139696158359848_fn

def Operator_139696158360184_fn(tree):
        return tree.children[0].data.value

dict[139696158360184] = Operator_139696158360184_fn

def Expr_139696158361136_fn(tree):

        a = 0
        b = 0
        op = None
    
        a = tree.children[0].fn(tree.children[0])

        if op is None or op == '+':
            return a+b
        else:
            return a-b
    
dict[139696158361136] = Expr_139696158361136_fn

def Expr_139696158361416_fn(tree):

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
    
dict[139696158361416] = Expr_139696158361416_fn

def Number_139696158361696_fn(tree):
        num = tree.children[0].fn(tree.children[0])

        return int(num)
    
dict[139696158361696] = Number_139696158361696_fn

