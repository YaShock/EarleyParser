dict = {}
def Num_139972500368744_fn(node):
        return node.children[0].data.value

dict[139972500368744] = Num_139972500368744_fn

def OpExpr_139972500342208_fn(node):
        return node.children[0].data.value

dict[139972500342208] = OpExpr_139972500342208_fn

def OpExpr_139972500418856_fn(node):
        return node.children[0].data.value

dict[139972500418856] = OpExpr_139972500418856_fn

def OpProduct_139972500419472_fn(node):
        return node.children[0].data.value

dict[139972500419472] = OpProduct_139972500419472_fn

def OpProduct_139972500419864_fn(node):
        return node.children[0].data.value

dict[139972500419864] = OpProduct_139972500419864_fn

def Formula_139972500420480_fn(node):
        result = node.children[0].fn(node.children[0])

        print(result)
    
dict[139972500420480] = Formula_139972500420480_fn

def Expr_139972500421208_fn(node):

        a = 0
        b = 0
        op = '+'
    
        a = node.children[0].fn(node.children[0])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[139972500421208] = Expr_139972500421208_fn

def Expr_139972500421432_fn(node):

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
    
dict[139972500421432] = Expr_139972500421432_fn

def Term_139972500422048_fn(node):

        a = 0
        b = 1
        op = '*'
    
        a = node.children[0].fn(node.children[0])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[139972500422048] = Term_139972500422048_fn

def Term_139972500422272_fn(node):

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
    
dict[139972500422272] = Term_139972500422272_fn

def Factor_139972500426992_fn(node):
        a = node.children[0].fn(node.children[0])

        return a
    
dict[139972500426992] = Factor_139972500426992_fn

def Factor_139972500427272_fn(node):
        a = node.children[1].fn(node.children[1])

        return a
    
dict[139972500427272] = Factor_139972500427272_fn

def Number_139972500427720_fn(node):
        num = node.children[0].fn(node.children[0])

        return int(num)
    
dict[139972500427720] = Number_139972500427720_fn

