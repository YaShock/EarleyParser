from grammar import Grammar, Term, Variable, Rule, Production
from earley import Parser
import importlib
import string
import collections
import re
import os

def contains_whitespace(s):
    return any([c in s for c in string.whitespace])

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'col'])

class Metagrammar(object):
    """docstring for Metagrammar"""
    def __init__(self):
        token_specification = [
            ('COMMENT',  r'#.*'),
            ('PYTHON_CODE',  r'{(.|\n)*?}'),
            ('DOUBLE_QUOTED',  r'\".*?\"'),
            ('SINGLE_QUOTED',     r'\'.*?\''),
            ('ID',      r'[a-zA-Z_]\w*'),
            ('NUMBER',      r'\d'),
            ('LPAREN', r'\('),
            ('RPAREN',    r'\)'),
            ('COLON',    r':'),
            ('EQUALS',    r'='),
            ('LT',    r'<'),
            ('GT',    r'>'),
            ('OR',    r'\|'),
            ('COMMA',    r','),
            ('SKIP',    r'[ \t]'),
            ('NEWLINE',    r'\n'),
        ]
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        self.get_token = re.compile(self.tok_regex).match
        self.keywords = {'begin', 'expansion', 'end'}

    def _tokenize(self, s):
        line = 1
        pos = line_start = 0
        mo = self.get_token(s)
        while mo is not None:
            typ = mo.lastgroup
            if typ == 'NEWLINE':
                line_start = pos
                line += 1
            elif typ != 'SKIP':
                val = mo.group(typ)
                if typ == 'ID' and val in self.keywords:
                    typ = val
                yield Token(typ, val, line, mo.start()-line_start)
            pos = mo.end()
            mo = self.get_token(s, pos)
        if pos != len(s):
            raise RuntimeError('Unexpected character %r on line %d' %(s[pos], line))

    def _next(self):
        self.current_token, self.next_token = self.next_token, next(self.tokens, None)
        return self.current_token

    def _expect(self, typ):
        t = self.current_token
        if t.typ != typ:
            raise SyntaxError("Expected symbol %s, got %s on line %d, column %d" % (typ, t.typ, t.line, t.col))

    def _accept(self, typ):
        self._expect(typ)
        val = self.current_token.value
        self._next()
        return val

    def process_grammar(self, grammar_text, output_filename):
        # curpath = os.path.abspath(os.curdir)
        # print("Current path is: %s" % curpath)
        with open(output_filename, 'w') as o:
            self.output = o
            o.write('dict = {}\n')
            self._parse_grammar(grammar_text)
        self._set_rule_functions(output_filename)
        return self.grammar

    def _set_rule_functions(self, output_filename):
        # import generated.functions
        module = importlib.import_module(output_filename[0:-3])
        #module.create()
        for rule in self.grammar.rules:
            value = module.dict.get(id(rule))
            rule.fn = value

    def _parse_grammar(self, grammar_text):
        self.grammar = Grammar()
        self.tokens = self._tokenize(grammar_text)
        self.current_token = self.next_token = None
        self._next()
        self._parse_stmt_list()

    def _parse_stmt_list(self):
        while(self.next_token):
            try:
                self._next()
                #print(self.current_token)
                self._parse_stmt()
            except SyntaxError as error:
                print(error)
                #raise SyntaxError("Invalid syntax: %s, at line: %i" % (self.token, self.line_index))

    def _parse_stmt(self):
        t = self.current_token
        if t.typ == 'COMMENT':
            print('Found comment: ' + repr(self.current_token.value))
            #pass
        elif t.typ == 'LT':
            self._parse_option()
        elif t.typ == 'ID':
            nt = self.next_token
            if nt.typ == 'COLON':
                self._parse_token()
            elif nt.typ == 'LPAREN':
                self._parse_rule()
            else:
                raise SyntaxError("Expected symbol \'(\' or \':\', got %s on line %d, column %d" % (nt.typ, nt.line, nt.col))
        else:
            SyntaxError("Expected symbol \'<\' or an identifier, got %s on line %d, column %d" % (t.typ, t.line, t.col))

    def _parse_option(self):
        self._next()
        opt = self._accept('ID')
        t = self.current_token
        if opt != 'delim':
            raise SyntaxError("Unknown option on line %d, column %d" % (t.line, t.col))
        self._accept('GT')
        self._accept('COLON')
        val = self._parse_terminal()
        self.grammar.delim = val
        print('Found option: ' + repr((opt, val)))

    def _parse_token(self):
        name = self.current_token.value
        self._next()
        self._accept('COLON')
        product = self._parse_token_product()
        for term in product:
            self.grammar.add_rule(Rule(Variable(name), Production(term)))
        print('Found token: ' + repr((name, product)))

    def _parse_token_product(self):
        t = self.current_token
        prod = []
        prod.append(Term(self._parse_terminal()))
        print('Found a token term: ' + t.value)
        while self.next_token.typ == 'OR':
            self._next()
            t = self._next()
            prod.append(Term(self._parse_terminal()))
            print('Found a token term: ' + t.value)
        return prod

    def _parse_rule(self):
        rule_name = self._parse_rule_name()
        print('Found rule name: ' + repr(rule_name))
        self._accept('COLON')
        body = self._parse_rule_body()
        choices = body[0]
        for choice in choices:
            prod = Production(*[term[0] for term in choice])
            rule = Rule(Variable(rule_name[0]), prod)
            self.grammar.add_rule(rule)
            self._write_rule_function(rule, choice, body[1], body[2])

    def _write_rule_function(self, rule, choice, begin, end):
        self.output.write('def %s_%s_fn(tree):\n' % (rule.variable.name, id(rule)))
        if begin:
            self.output.write(begin + '\n')
        self._write_rule_choice(rule, choice)
        if end:
            self.output.write(end + '\n')
        self.output.write('dict[%i] = %s_%s_fn\n' % (id(rule), rule.variable.name, id(rule)))

    def _write_rule_choice(self, rule, choice):
        print(repr(rule))
        for idx, term in enumerate(choice):
            # self.output.write('        print(\'%s \' + repr(tree.children[%i].data))\n' % (idx, idx))
            var = 'tree.children[%i]' % idx
            if term[0] is not None:
                assign = '%s = ' % term[0]
            else:
                assign = ''
            if term[1].terminal:
                if assign:
                    self.output.write('        %s%s\n' % (assign, var))
            else:
                self.output.write('        %s%s.fn(%s)\n' % (assign, var, var))

    def _parse_rule_body(self):
        t = self.current_token
        begin = end = None
        if t.typ == 'begin':
            begin = self._parse_begin_block()
            self._next()
            print('Found begin block: ' + begin)
        choices = self._parse_expansion_block()
        t = self.current_token
        if t.typ == 'end':
            end = self._parse_end_block()
            print('Found end block: ' + end)
        return (choices, begin, end)

    def _parse_begin_block(self):
        self._accept('begin')
        self._accept('COLON')
        self._expect('PYTHON_CODE')
        return self.current_token.value[1:-1]
        # python_code = self._accept('PYTHON_CODE')
        # return python_code[1:-1]

    def _parse_expansion_block(self):
        self._accept('expansion')
        self._accept('COLON')
        choices = self._parse_exp_choices()
        print('Found expansion choices: ' + repr(choices))
        return choices

    def _parse_end_block(self):
        self._accept('end')
        self._accept('COLON')
        self._expect('PYTHON_CODE')
        return self.current_token.value[1:-1]
        # python_code = self._accept('PYTHON_CODE')
        # return python_code[1:-1]

    def _parse_exp_choices(self):
        choices = [self._parse_exp_product()]
        print('Found expansion product: ' + repr(choices[0]))
        while self.current_token.typ == 'OR':
            self._next()
            prod = self._parse_exp_product()
            print('Found expansion product: ' + repr(prod))
            choices.append(prod)
        return choices

    def _parse_exp_product(self):
        prod = [self._parse_exp_term()]
        print('Found expansion term: ' + repr(prod[0]))
        while self.current_token.typ == 'COMMA':
            self._next()
            term = self._parse_exp_term()
            print('Found expansion term: ' + repr(term))
            prod.append(term)
        return prod

    def _parse_exp_term(self):
        assignment = None
        term = None
        if self.next_token.typ == 'EQUALS':
            assignment = self._accept('ID')
            self._next()
        t = self.current_token
        if t.typ == 'SINGLE_QUOTED':
            term = Term(self._accept('SINGLE_QUOTED'))
        elif t.typ == 'DOUBLE_QUOTED':
            term = Term(self._accept('DOUBLE_QUOTED'))
        elif t.typ == 'ID':
            if self.next_token.typ == 'LPAREN':
                rule = self._parse_rule_name()
                var = Variable(rule[0])
                var.terminal = False
                term = var
            else:
                token = self._accept('ID')
                var = Variable(token)
                var.terminal = True
                term = var
        else:
            raise SyntaxError("Expected symbol \'TERMINAL\', \"REGEX\", TOKEN NAME or RULE NAME, got %s on line %d, column %d" % (t.typ, t.line, t.col))
        return (assignment, term)

    def _parse_rule_name(self):
        name = self.current_token.value
        self._next()
        self._accept('LPAREN')
        t = self.current_token
        params = None
        if t.typ == 'ID':
            params = self._parse_params()
            print('Found params: ' + repr(params))
        elif t.typ == 'RPAREN':
            pass
        else:
            raise SyntaxError("Expected symbol \')\' or a parameter, got %s on line %d, column %d" % (t.typ, t.line, t.col))
        self._accept('RPAREN')
        return (name, params)

    def _parse_params(self):
        params = [self._accept('ID')]
        while self.current_token.typ != 'RPAREN':
            self._accept('COMMA')
            params.append(self._accept('ID'))
        return params

    def _parse_terminal(self):
        t = self.current_token
        if t.typ == 'SINGLE_QUOTED':
            val = re.escape(t.value.strip('\''))
        elif t.typ == 'DOUBLE_QUOTED':
            val = t.value.strip('\"')
        else:
            raise SyntaxError("Expected symbol \'PLAIN STRING\' or \"REGEX\", got %s on line %d, column %d" % (t.typ, t.line, t.col))
        return val

# class ContextBuilder(object):
#     """docstring for ContextBuilder"""
#     def __init__(self, grammar):
#         self.grammar = grammar

#     def parse_line(self, line):
#         if (line[0] == '/' and line[1] == '/') or line.isspace():
#             return
#         lst = line.split('->')
#         if len(lst) != 2:
#             raise ValueError('Invalid rule syntax: ->')
#         if contains_whitespace(line[0]):
#             raise ValueError('Invalid rule syntax: whitespace in the variable')
#         var_name = lst[0].strip()
#         if var_name[0] == '<' and var_name[-1] == '>':
#             self.parse_option(var_name.strip('<>'), lst[1])
#         else:
#             self.parse_rule(var_name, lst[1])

#     def parse_rule(self, var_name, val):
#         lst = val.split('::=')
#         if len(lst) > 2:
#             raise ValueError('Invalid rule syntax: more than one ::=')
#         elif len(lst) == 2:
#             fn = lst[1].strip()
#             fn_enter = 'semantics.' + fn + '_enter'
#             fn_exit = 'semantics.' + fn + '_exit'
#         else:
#             fn_enter = None
#             fn_exit = None
            
#         variable = self.grammar.variables.setdefault(var_name, Variable(var_name))
#         rules = lst[0].split('|')
#         for rule in rules:
#             terms = rule.split()
#             term_list = []
#             for term in terms:
#                 if term[0] == '\"' and term[-1] == '\"':
#                     term_list.append(Term(term.strip('\"')))
#                 elif term[0] == '\'' and term[-1] == '\'':
#                     term_list.append(Term(re.escape(term.strip('\''))))
#                 else:
#                     var = self.grammar.variables.setdefault(term, Variable(term))
#                     term_list.append(var)
#             r = Rule(variable, Production(*term_list))
#             self.grammar.add_rule(r)
#             self.generated_file.write('    dict[%i] = (%s, %s)\n' % (id(r), fn_enter, fn_exit))

#     def parse_option(self, var_name, val):
#         val = val.strip()
#         if val[0] != '\'' or val[-1] != '\'':
#             raise ValueError('Invalid option syntax: the value must be enclosed in \'')
#         val = val.strip('\'')
#         if var_name == 'delim':
#             self.grammar.delim = val
#         else:
#             raise ValueError('Invalid option syntax: unknown option name')

#     def read_file(self, file):
#         self.generated_file = open('./generated/generated.py', 'w')
#         self.generated_file.write('from . import semantics\n')
#         self.generated_file.write('dict = {}\n')
#         self.generated_file.write('def create():\n')
#         for line in file:
#             self.parse_line(line)
#         self.generated_file.close()

#     def build(self):
#         file = open('generated/grammar.cf')
#         self.read_file(file)
#         file.close()
#         module = importlib.import_module('generated.generated')
#         module.create()
#         for rule in self.grammar.rules:
#             d = module.dict[id(rule)]
#             rule.fn_enter = d[0]
#             rule.fn_exit = d[1]

if __name__ == "__main__":
    text = '''<delim>:"\s"

#Formula():
#    expansion:
#        Expr()
#    end: {
#
#    }

Num: "[0-9]+"
Operator: '+' | '-'

Expr():
    begin:
    {
        a = 0
        b = 0
        op = None
    }
    expansion:
        a = Number() |
        a = Expr(), op = Operator, b = Number()        
    end:
    {
        if op is None or op.value == '+':
            return a+b
        else:
            return a-b
    }

Number():
    expansion:
        num = Num
    end: {
        return int(num.value)
    }'''

    mg = Metagrammar()
    g = mg.process_grammar(text, 'functions.py')
    print('------------CREATED GRAMMAR------------')
    print('Delim option: ' + g.delim)
    print('Terminals: ' + repr(g.terminals))
    print('Rules:')
    for rule in g.rules:
        print(rule)
        # if rule.fn:
        #     print('Functions: ' + repr(rule.fn))

    print('Top rule: ' + repr(g.topRule))
    print('Parsing input:')
    parser = Parser(g)    
    res = parser.parse(input())
    #print(repr(parser.tokens))
    # for r in res:
    #     r.print()
    #     print('Walking')
    #     r.walk()