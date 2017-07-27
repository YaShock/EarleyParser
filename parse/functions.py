dict = {}
def Formula_140015861788008_fn(node):
        result = node.children[0].fn(node.children[0])

        print(result)
    
dict[140015861788008] = Formula_140015861788008_fn

def Num_140015861788456_fn(node):
        return node.children[0].data.value

dict[140015861788456] = Num_140015861788456_fn

def OpExpr_140015861825888_fn(node):
        return node.children[0].data.value

dict[140015861825888] = OpExpr_140015861825888_fn

def OpExpr_140015861826224_fn(node):
        return node.children[0].data.value

dict[140015861826224] = OpExpr_140015861826224_fn

def OpProduct_140015861827064_fn(node):
        return node.children[0].data.value

dict[140015861827064] = OpProduct_140015861827064_fn

def OpProduct_140015861827288_fn(node):
        return node.children[0].data.value

dict[140015861827288] = OpProduct_140015861827288_fn

def Expr_140015861828016_fn(node):

        a = 0
        b = 0
        op = '+'
    
        a = node.children[0].fn(node.children[0])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[140015861828016] = Expr_140015861828016_fn

def Expr_140015861828240_fn(node):

        a = 0
        b = 0
        op = '+'
    
        a = node.children[0].fn(node.children[0])
        op = node.children[1].fn(node.children[1])
        b = node.children[2].fn(node.children[2])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[140015861828240] = Expr_140015861828240_fn

def Term_140015861828856_fn(node):

        a = 0
        b = 1
        op = '*'
    
        a = node.children[0].fn(node.children[0])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[140015861828856] = Term_140015861828856_fn

def Term_140015861829080_fn(node):

        a = 0
        b = 1
        op = '*'
    
        a = node.children[0].fn(node.children[0])
        op = node.children[1].fn(node.children[1])
        b = node.children[2].fn(node.children[2])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[140015861829080] = Term_140015861829080_fn

def Factor_140015861837952_fn(node):
        a = node.children[0].fn(node.children[0])

        return a
    
dict[140015861837952] = Factor_140015861837952_fn

def Factor_140015861838232_fn(node):
        a = node.children[1].fn(node.children[1])

        return a
    
dict[140015861838232] = Factor_140015861838232_fn

def Number_140015861838624_fn(node):
        num = node.children[0].fn(node.children[0])

        return int(num)
    
dict[140015861838624] = Number_140015861838624_fn

