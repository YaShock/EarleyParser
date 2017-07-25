dict = {}
def TopKekz_140507442654344_fn(node):

        x = 'yey'
    
        node.children[0].fn(node.children[0],x)

        print('End')
    
dict[140507442654344] = TopKekz_140507442654344_fn

def Formula_140507442655072_fn(node,x):
        result = node.children[0].fn(node.children[0])

        print("Kekz: " + x)
        print(result)
    
dict[140507442655072] = Formula_140507442655072_fn

def Num_140507442766008_fn(node):
        return node.children[0].data.value

dict[140507442766008] = Num_140507442766008_fn

def OpExpr_140507442766736_fn(node):
        return node.children[0].data.value

dict[140507442766736] = OpExpr_140507442766736_fn

def OpExpr_140507442767016_fn(node):
        return node.children[0].data.value

dict[140507442767016] = OpExpr_140507442767016_fn

def OpProduct_140507442767632_fn(node):
        return node.children[0].data.value

dict[140507442767632] = OpProduct_140507442767632_fn

def OpProduct_140507442767856_fn(node):
        return node.children[0].data.value

dict[140507442767856] = OpProduct_140507442767856_fn

def Expr_140507442768584_fn(node):

        a = 0
        b = 0
        op = '+'
    
        a = node.children[0].fn(node.children[0])

        if op == '+':
            return a + b
        else:
            return a - b
    
dict[140507442768584] = Expr_140507442768584_fn

def Expr_140507442768864_fn(node):

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
    
dict[140507442768864] = Expr_140507442768864_fn

def Term_140507442769480_fn(node):

        a = 0
        b = 1
        op = '*'
    
        a = node.children[0].fn(node.children[0])

        if op == '*':
            return a * b
        else:
            return a / b
    
dict[140507442769480] = Term_140507442769480_fn

def Term_140507442769704_fn(node):

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
    
dict[140507442769704] = Term_140507442769704_fn

def Factor_140507442704848_fn(node):
        a = node.children[0].fn(node.children[0])

        return a
    
dict[140507442704848] = Factor_140507442704848_fn

def Factor_140507442705128_fn(node):
        a = node.children[1].fn(node.children[1])

        return a
    
dict[140507442705128] = Factor_140507442705128_fn

def Number_140507442705520_fn(node):
        num = node.children[0].fn(node.children[0])

        return int(num)
    
dict[140507442705520] = Number_140507442705520_fn

