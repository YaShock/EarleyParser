import re
import collections

grammar_text = '''#Example: algebric expression evaluator

Digit: "[0-9]"
OpExpr: '+' | '-'
OpProduct: '*' | '/'

Formula():
    expansion:
        result = Expr()
    end:
    {
        return result
    }

Expr():
    begin: {
        a = 0
        b = 0
        op = '+'
    }
    expansion:
        a = Term() |
        a = Expr(), op = OpExpr, b = Term()
    end:
    {
        if op == '+':
            return a + b
        else:
            return a - b
    }

Term():
    begin: {
        a = 0
        b = 0
        op = '*'
    }
    expansion:
        a = Factor() |
        a = Term(), op = OpProduct, b = Factor()
    end: {
        if op == '*':
            return a * b
        else:
            return a / b
    }

Factor():
    expansion:
        a = Num() |
        '(', a = Expr(), ')'
    end: {
        return a
    }

Num():
    begin: {
        digit = '0'
        num = 0
    }
    expansion:
        digit = Digit |
        num = Num(), digit = Digit
    end: {
        return num*10+int(digit)
    }'''

# COMMENT       = r'(?P<COMMENT>#.*)'
# DOUBLE_QUOTED = r'(?P<DOUBLE_QUOTED>\".*?\")'
# SINGLE_QUOTED = r'(?P<SINGLE_QUOTED>\'.*?\')'
# ID            = r'(?P<ID>\w+)'
# NUMBER        = r'(?P<NUMBER>\d+)'
# LPAREN        = r'(?P<LPAREN>\()'
# RPAREN        = r'(?P<RPAREN>\))'
# LBRACKET      = r'(?P<LBRACKET>\{)'
# RBRACKET      = r'(?P<RBRACKET>\})'
# COLON         = r'(?P<COLON>:)'
# EQUALS        = r'(?P<EQUALS>=)'
# LESS_THAN     = r'(?P<LESS_THAN><)'
# GREATER_THAN  = r'(?P<GREATER_THAN>>)'
# OR            = r'(?P<GREATER_THAN>|)'
# WS            = r'(?P<WS>\s+)'

# master_pattern = re.compile('|'.join((COMMENT, DOUBLE_QUOTED, SINGLE_QUOTED, NUMBER, ID, LPAREN, RPAREN, LBRACKET, RBRACKET, COLON, EQUALS, LESS_THAN, GREATER_THAN, OR, WS)))

# Token = collections.namedtuple('Token', ['type', 'value'])

# def generate_tokens(pattern, text):
#   scanner = pattern.scanner(text)
#   for m in iter(scanner.match, None):
#     token = Token(m.lastgroup, m.group())
#     if token.type != 'WS':
#         yield token

# tokens = generate_tokens(master_pattern, grammar_text)

# for t in tokens:
#   print(t)

#tokens = [s.strip() for s in pattern.split(grammar_text) if s.strip()]


Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

def tokenize(s):
    keywords = {'begin', 'expansion', 'end'}
    token_specification = [
        ('COMMENT',  r'#.*'),
        ('PYTHON_CODE',  r'{(.|\n)*?}'),
        ('DOUBLE_QUOTED',  r'\".*?\"'),
        ('SINGLE_QUOTED',     r'\'.*?\''),
        ('ID',      r'\w+'),
        ('NUMBER',      r'\d'),
        ('LPAREN', r'\('),
        ('RPAREN',    r'\)'),
        ('COLON',    r':'),
        ('EQUALS',    r'='),
        ('LESS_THAN',    r'<'),
        ('GREATER_THAN',    r'>'),
        ('OR',    r'\|'),
        ('COMMA',    r','),
        ('SKIP',    r'[ \t]'),
        ('NEWLINE',    r'\n'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line = 1
    pos = line_start = 0
    mo = get_token(s)
    while mo is not None:
        typ = mo.lastgroup
        if typ == 'NEWLINE':
            line_start = pos
            line += 1
        elif typ != 'SKIP':
            val = mo.group(typ)
            if typ == 'ID' and val in keywords:
                typ = val
            yield Token(typ, val, line, mo.start()-line_start)
        pos = mo.end()
        mo = get_token(s, pos)
    if pos != len(s):
        raise RuntimeError('Unexpected character %r on line %d' %(s[pos], line))

statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

for token in tokenize(grammar_text):
    print(token)
    
    