dict = {}
def Num_139624092122640_fn(node):
        return node.children[0].data.value

dict[139624092122640] = Num_139624092122640_fn

def OpExpr_139624092237952_fn(node):
        return node.children[0].data.value

dict[139624092237952] = OpExpr_139624092237952_fn

def OpExpr_139624092238288_fn(node):
        return node.children[0].data.value

dict[139624092238288] = OpExpr_139624092238288_fn

def OpProduct_139624092238904_fn(node):
        return node.children[0].data.value

dict[139624092238904] = OpProduct_139624092238904_fn

def OpProduct_139624092239296_fn(node):
        return node.children[0].data.value

dict[139624092239296] = OpProduct_139624092239296_fn

def Formula_139624092239912_fn(node):
        result = node.children[0].fn(node.children[0])

        print(result)
    
dict[139624092239912] = Formula_139624092239912_fn

def Expr_139624092240640_fn(node):

        a = 0
        b = 0
        op = '+'
    
        a = node.children[0].fn(node.children[0])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[139624092240640] = Expr_139624092240640_fn

def Expr_139624092240864_fn(node):

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
    
dict[139624092240864] = Expr_139624092240864_fn

def Term_139624092241480_fn(node):

        a = 0
        b = 1
        op = '*'
    
        a = node.children[0].fn(node.children[0])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[139624092241480] = Term_139624092241480_fn

def Term_139624092241704_fn(node):

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
    
dict[139624092241704] = Term_139624092241704_fn

def Factor_139624092180944_fn(node):
        a = node.children[0].fn(node.children[0])

        return a
    
dict[139624092180944] = Factor_139624092180944_fn

def Factor_139624092181224_fn(node):
        a = node.children[1].fn(node.children[1])

        return a
    
dict[139624092181224] = Factor_139624092181224_fn

def Number_139624092181616_fn(node):
        num = node.children[0].fn(node.children[0])

        return int(num)
    
dict[139624092181616] = Number_139624092181616_fn

