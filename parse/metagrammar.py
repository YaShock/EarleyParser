import importlib
from collections import namedtuple
import re
import sys

Token = namedtuple('Token', ['typ', 'value', 'line', 'col'])
Variable = namedtuple('Variable', ['name'])
Rule = namedtuple('Variable', ['name', 'params'])

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
            ('EXCL',    r'!'),
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
        self.log = False

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

    def _log(self, message):
        if self.log:
            print(message)

    def process_grammar(self, grammar_text, output_filename):
        with open(output_filename, 'w') as o:
            self.output = o
            # o.write('dict = {}\n')
            self._parse_grammar(grammar_text)
        # self._set_rule_functions(output_filename)
        # return self.grammar

    # def _set_rule_functions(self, output_filename):
    #     # trim '.py' from the file name
    #     module = importlib.import_module(output_filename[0:-3].replace('/', '.'))
    #     for rule in self.grammar.rules:
    #         value = module.dict.get(id(rule))
    #         rule.fn = value

    def _parse_grammar(self, grammar_text):
        # self.grammar = Grammar()
        self.output.write('grammar = Grammar()\n')
        self.tokens = self._tokenize(grammar_text)
        self.current_token = self.next_token = None
        self._next()
        self._parse_stmt_list()

    def _parse_stmt_list(self):
        while(self.next_token):
            try:
                self._next()
                self._parse_stmt()
            except SyntaxError as error:
                print(error)

    def _parse_stmt(self):
        t = self.current_token
        if t.typ == 'COMMENT':
            self._log('Found comment: ' + repr(self.current_token.value))
        elif t.typ == 'LT':
            self._parse_option()
        elif t.typ == 'EXCL':
            self._parse_rule()
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
        self.output.write('grammar.delim = %s\n' % val)
        # self.grammar.delim = val
        self._log('Found option: ' + repr((opt, val)))

    def _parse_token(self):
        name = self.current_token.value
        self._next()
        self._accept('COLON')
        product = self._parse_token_product()
        for term in product:
            # rule = Rule(Variable(name), Production(term))
            # self.grammar.add_rule(rule)
            self.output.write('%s = Rule(Variable(%s), Production(Term(\'%s\')))\n' % (name, name, term))
            # self._write_token_function(rule)
        self._log('Found token: ' + repr((name, product)))

    def _write_token_function(self, rule):
        self.output.write('def %s_%s_fn(node):\n' % (rule.variable.name, id(rule)))
        self.output.write('        return node.children[0].data.value\n\n')
        self.output.write('%s.fn = %s_%s_fn\n\n' % (rule.variable.name, rule.variable.name, id(rule)))
        # self.output.write('dict[%i] = %s_%s_fn\n\n' % (id(rule), rule.variable.name, id(rule)))

    def _parse_token_product(self):
        t = self.current_token
        prod = []
        prod.append(self._parse_terminal())
        self._log('Found a token term: ' + t.value)
        while self.next_token.typ == 'OR':
            self._next()
            t = self._next()
            prod.append(self._parse_terminal())
            self._log('Found a token term: ' + t.value)
        return prod

    def _parse_rule(self):
        is_top_rule = False
        if self.current_token.typ == 'EXCL':
            self._accept('EXCL')
            is_top_rule = True
        (rule_name, rule_params) = self._parse_rule_name()
        self._log('Found rule name: ' + repr(rule_name))
        self._accept('COLON')
        body = self._parse_rule_body()
        choices = body[0]
        for choice in choices:
            prod = Production(*[term[1] for term in choice])
            rule = Rule(Variable(rule_name), prod)
            prod_str = ', '.join('%s' % term for term in prod)            
            self.output.write('%s = Rule(Variable(%s), Production(%s))\n' % (rule_name, rule_name, prod_str))
            # self.grammar.add_rule(rule)
            if is_top_rule:
                self.output.write('grammar.top_rule = rule\n')
                # self.grammar.top_rule = rule
            self._write_rule_function(rule, rule_params, choice, body[1], body[2])

    def _write_rule_function(self, rule, rule_params, choice, begin, end):
        params = ['node']
        if rule_params:
            params.extend(rule_params)
        paramString = ','.join(params)
        self.output.write('def %s_%s_fn(%s):\n' % (rule.variable.name, id(rule), paramString))
        if begin:
            self.output.write(begin + '\n')
        self._write_rule_choice(rule, choice)
        if end:
            self.output.write(end + '\n')
        self.output.write('%s.fn = %s_%s_fn\n\n' % (rule.variable.name, rule.variable.name, id(rule)))
        # self.output.write('dict[%i] = %s_%s_fn\n\n' % (id(rule), rule.variable.name, id(rule)))

    def _write_rule_choice(self, rule, choice):
        for idx, term in enumerate(choice):
            if isinstance(term[1], Variable):
                var = 'node.children[%i]' % idx
                params = [var]
                if term[2]:
                    params.extend(term[2])
                paramString = ','.join(params)

                if term[0] is not None:
                    assign = '%s = ' % term[0]
                else:
                    assign = ''
                self.output.write('        %s%s.fn(%s)\n' % (assign, var, paramString))

    def _parse_rule_body(self):
        t = self.current_token
        begin = end = None
        if t.typ == 'begin':
            begin = self._parse_begin_block()
            self._next()
            self._log('Found begin block: ' + begin)
        choices = self._parse_expansion_block()
        t = self.current_token
        if t.typ == 'end':
            end = self._parse_end_block()
            self._log('Found end block: ' + end)
        return (choices, begin, end)

    def _parse_begin_block(self):
        self._accept('begin')
        self._accept('COLON')
        self._expect('PYTHON_CODE')
        return self.current_token.value[1:-1]

    def _parse_expansion_block(self):
        self._accept('expansion')
        self._accept('COLON')
        choices = self._parse_exp_choices()
        self._log('Found expansion choices: ' + repr(choices))
        return choices

    def _parse_end_block(self):
        self._accept('end')
        self._accept('COLON')
        self._expect('PYTHON_CODE')
        return self.current_token.value[1:-1]

    def _parse_exp_choices(self):
        choices = [self._parse_exp_product()]
        self._log('Found expansion product: ' + repr(choices[0]))
        while self.current_token.typ == 'OR':
            self._next()
            prod = self._parse_exp_product()
            self._log('Found expansion product: ' + repr(prod))
            choices.append(prod)
        return choices

    def _parse_exp_product(self):
        prod = [self._parse_exp_term()]
        self._log('Found expansion term: ' + repr(prod[0]))
        while self.current_token.typ == 'COMMA':
            self._next()
            term = self._parse_exp_term()
            self._log('Found expansion term: ' + repr(term))
            prod.append(term)
        return prod

    def _parse_exp_term(self):
        assignment = None
        term = None
        params = None
        if self.next_token.typ == 'EQUALS':
            assignment = self._accept('ID')
            self._next()
        t = self.current_token
        if t.typ == 'SINGLE_QUOTED' or t.typ == 'DOUBLE_QUOTED':
            term = 'Term(\'%s\')' % self._parse_terminal()
            self._next()
        elif t.typ == 'ID':
            if self.next_token.typ == 'LPAREN':
                rule = self._parse_rule_name()
                term = 'Variable(\'%s\')' % rule[0]
                params = rule[1]
            else:
                token = self._accept('ID')
                term = 'Variable(\'%s\')'% token
        else:
            raise SyntaxError("Expected symbol \'TERMINAL\', \"REGEX\", TOKEN NAME or RULE NAME, got %s on line %d, column %d" % (t.typ, t.line, t.col))
        return (assignment, term, params)

    def _parse_rule_name(self):
        name = self.current_token.value
        self._next()
        self._accept('LPAREN')
        t = self.current_token
        params = None
        if t.typ == 'ID':
            params = self._parse_params()
            self._log('Found params: ' + repr(params))
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

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # from grammar import Grammar, Term, Variable, Rule, Production
        # from earley import Parser

        grammar_filename = sys.argv[1]
        output_filename = sys.argv[2]

        text = ''
        with open(grammar_filename, 'r') as grammar_file:
            text = grammar_file.read()

        mg = Metagrammar()
        # mg.log = True
        mg.process_grammar(text, output_filename)
        # print('------------CREATED GRAMMAR------------')
        # print('Delim option: ' + g.delim)
        # print('Terminals: ' + repr(g.terminals))
        # print('Rules:')
        # for rule in g.rules:
        #     print(rule)
        #     # if rule.fn:
        #     #     print('Functions: ' + repr(rule.fn))

        # print('Top rule: ' + repr(g.top_rule))
        # print('Parsing input:')
        # parser = Parser(g)    
        # res = parser.parse(input())
        # #print(repr(parser.tokens))
        # for r in res:
        #     r.print()
        #     # print('Walking')
        #     r.walk()