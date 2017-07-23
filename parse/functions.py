dict = {}
def Formula_140002614262976_fn(tree):
        result = tree.children[0].fn(tree.children[0])

        print(result)
    
dict[140002614262976] = Formula_140002614262976_fn

def Num_140002614263368_fn(tree):
        return tree.children[0].data.value

dict[140002614263368] = Num_140002614263368_fn

def OpExpr_140002614374584_fn(tree):
        return tree.children[0].data.value

dict[140002614374584] = OpExpr_140002614374584_fn

def OpExpr_140002614374920_fn(tree):
        return tree.children[0].data.value

dict[140002614374920] = OpExpr_140002614374920_fn

def OpProduct_140002614375760_fn(tree):
        return tree.children[0].data.value

dict[140002614375760] = OpProduct_140002614375760_fn

def OpProduct_140002614375984_fn(tree):
        return tree.children[0].data.value

dict[140002614375984] = OpProduct_140002614375984_fn

def Expr_140002614376712_fn(tree):

        a = 0
        b = 0
        op = '+'
    
        a = tree.children[0].fn(tree.children[0])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[140002614376712] = Expr_140002614376712_fn

def Expr_140002614376992_fn(tree):

        a = 0
        b = 0
        op = '+'
    
        a = tree.children[0].fn(tree.children[0])
        op = tree.children[1].fn(tree.children[1])
        b = tree.children[2].fn(tree.children[2])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[140002614376992] = Expr_140002614376992_fn

def Term_140002614377608_fn(tree):

        a = 0
        b = 1
        op = '*'
    
        a = tree.children[0].fn(tree.children[0])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[140002614377608] = Term_140002614377608_fn

def Term_140002614377832_fn(tree):

        a = 0
        b = 1
        op = '*'
    
        a = tree.children[0].fn(tree.children[0])
        op = tree.children[1].fn(tree.children[1])
        b = tree.children[2].fn(tree.children[2])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[140002614377832] = Term_140002614377832_fn

def Factor_140002614378448_fn(tree):
        a = tree.children[0].fn(tree.children[0])

        return a
    
dict[140002614378448] = Factor_140002614378448_fn

def Factor_140002614313256_fn(tree):
        a = tree.children[1].fn(tree.children[1])

        return a
    
dict[140002614313256] = Factor_140002614313256_fn

def Number_140002614313648_fn(tree):
        num = tree.children[0].fn(tree.children[0])

        return int(num)
    
dict[140002614313648] = Number_140002614313648_fn

