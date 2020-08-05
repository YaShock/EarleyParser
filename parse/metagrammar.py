from collections import namedtuple
import re


Terminal = namedtuple('Terminal', ['typ', 'value'])
Token = namedtuple('Token', ['typ', 'value', 'line', 'col', 'indent'])
# Either a rule or a token
Variable = namedtuple('Variable', ['ref', 'typ', 'terms'])
# Used for parsing rules
Term = namedtuple('Term', ['assignment', 'value', 'typ', 'params'])
Rule = namedtuple('Rule', ['name', 'params', 'choices', 'begin', 'end'])


class Metagrammar(object):
    def __init__(self):
        self.tokens = []
        self.variable_rules = []
        # Terminal rule: (name, product of terminals)
        self.terminal_rules = []
        self.top_level_rule_idx = None
        self.symbols = []
        self.rule_id = 0

        self.log = False

        token_specification = [
            ('COMMENT', r'#.*'),
            ('DOUBLE_QUOTED', r'(\"(\\.|[^\"])*\")'),
            ('SINGLE_QUOTED', r'\'.*?\''),
            ('ID', r'[a-zA-Z_]\w*'),
            ('NUMBER', r'\d'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COLON', r':'),
            ('EXCL', r'!'),
            ('EQUALS', r'='),
            # ('LT', r'<'),
            # ('GT', r'>'),
            ('OR', r'\|'),
            ('COMMA', r','),
            ('SKIP', r'[ \t]'),
            ('NEWLINE', r'\n'),
        ]
        self.tok_regex = '|'.join('(?P<%s>%s)' %
                                  pair for pair in token_specification)
        self.get_token = re.compile(self.tok_regex).match
        self.keywords = {'begin', 'expansion', 'end'}

    def process_grammar(self, input_filename, output_filename):
        with open(input_filename) as inp:
            try:
                # Init
                self.tokens.clear()
                self.variable_rules.clear()
                self.terminal_rules.clear()
                self.top_level_rule_idx = None
                self.symbols.clear()
                self.rule_id = 0

                # Tokenize and parse
                self.tokens = self._tokenize(inp)
                self.current_token = self.next_token = None
                self._next()
                self._parse_stmt_list()

                # TODO: before generating, validate rules
                # Rule assignments have to refer to known symbols

                # Generate
                self._generate_output(output_filename)
            except SyntaxError as error:
                print(error)

    def _tokenize(self, input):
        line = 1
        pos = 0
        indent_level = 0
        base_indent = None
        expect_indent = None
        python_token = None
        python_start_line = 0
        python_start_pos = 0
        last_typ = None

        def check_indent(line, indent_level, expect_indent):
            if expect_indent is not None and indent_level != expect_indent:
                raise SyntaxError(
                    'Unexpected indentation on line {}'.format(
                        line))

        while True:
            content = input.readline()

            # Read leading whitespace
            leading_ws = self._parse_whitespace(content, pos)
            pos = len(leading_ws)

            # Add PYTHON_CODE token after dedent
            # Add to python token otherwise
            # TODO: this is a hack, is there a better way?
            if python_token is not None:
                ind_lvl = self._parse_indent(leading_ws, base_indent, line)
                last_typ = 'PYTHON_CODE'
                if ind_lvl < 2:
                    yield Token(
                        'PYTHON_CODE',
                        python_token,
                        python_start_line,
                        python_start_pos,
                        2)
                    python_token = None
                else:
                    python_token += content[len(base_indent) * 1:]
                    line += 1
                    pos = 0
                    expect_indent = None
                    continue

            if content == '':
                break

            while True:
                # print('inner loop')
                mo = self.get_token(content, pos)

                if mo is None:
                    raise SyntaxError(
                        'Unexpected symbol \'{}\' on line {}, column {}'.format(
                            content[pos], line, pos + 1))

                typ = mo.lastgroup

                # Ignore comments and empty lines
                if typ == 'NEWLINE' or typ == 'COMMENT':
                    line += 1
                    pos = 0
                    break
                elif typ != 'SKIP':
                    # Determine indent level
                    ind_lvl = self._parse_indent(leading_ws, base_indent, line)
                    if indent_level == 0 and ind_lvl == 1:
                        base_indent = leading_ws
                    indent_level = ind_lvl

                    check_indent(line, indent_level, expect_indent)

                    val = mo.group(typ)
                    if typ == 'ID' and val in self.keywords:
                        if indent_level != 1:
                            raise SyntaxError(
                                "Unexpected indentation before a keyword on line {}".format(
                                    line))
                        typ = val
                        # It will be a PYTHON_CODE token until indent decreases
                        if val == 'begin' or val == 'end':
                            python_token = ''
                            python_start_line = line
                            python_start_pos = pos

                    # Have to indent after keyword and colons
                    if typ == 'COLON' and (last_typ in self.keywords or last_typ == 'RPAREN'):
                        expect_indent = indent_level + 1
                    else:
                        expect_indent = None

                    last_typ = typ
                    yield Token(typ, val, line, mo.start(), indent_level)

                pos = mo.end()

    def _parse_whitespace(self, content, pos):
        if len(content) == 0:
            return ''
        i = pos
        while content[i].isspace() and content[i] != '\n':
            i += 1
        return content[pos:i]

    def _parse_indent(self, content, base_indent, line):
        level = 0
        indent = ''
        pos = 0
        while pos < len(content):
            if not content[pos].isspace():
                break

            indent += content[pos]
            pos += 1

            if indent == base_indent:
                level += 1
                indent = ''

        # Does not match base indentation
        if indent != '' and base_indent is not None:
            raise SyntaxError(
                'Unexpected indentation on line {}'.format(
                    line))

        # New base indent
        if indent != '' and level == 0:
            # self.base_indent = indent
            level = 1

        return level

    def _parse_stmt_list(self):
        while self.next_token:
            self._next()
            self._parse_stmt()

    def _parse_stmt(self):
        t = self.current_token
        # if t.typ == 'COMMENT':
            # self._log('Found comment: ' + repr(self.current_token.value))
        # elif t.typ == 'LT':
            # self._parse_option()
        if t.typ == 'EXCL':
            rule = self._parse_rule(True)
            self.top_level_rule_idx = len(self.variable_rules)
            self.variable_rules.append(rule)
        elif t.typ == 'ID':
            nt = self.next_token
            if nt.typ == 'COLON':
                self.terminal_rules.append(self._parse_token())
            elif nt.typ == 'LPAREN':
                self.variable_rules.append(self._parse_rule(False))
            else:
                raise SyntaxError(
                    "Expected symbol '(' or ':', got {} on line {}, column {}".format(
                        nt.typ, nt.line, nt.col))
        else:
            SyntaxError("Expected symbol \'!\' or an identifier, got %s on line %d, column %d" % (
                t.typ, t.line, t.col))

    def _parse_option(self):
        self._next()
        opt = self._accept('ID')
        t = self.current_token
        if opt != 'delim':
            raise SyntaxError(
                "Unknown option on line {}, column {}".format(t.line, t.col))
        self._accept('GT')
        self._accept('COLON')
        val = self._parse_terminal()
        # self.output.write('grammar.delim = \'%s\'\n' % val)
        self._log('Found option: ' + repr((opt, val)))

    def _parse_token(self):
        name = self.current_token.value

        if name in self.symbols:
            raise SyntaxError('Redefinition of symbol {} on line {}, column {}'.format(
                name, self.current_token.line))

        self._next()
        self._accept('COLON')
        product = self._parse_token_product()
        self.symbols.append(name)
        self._log('Found token: ' + repr((name, product)))
        return (name, product)

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

    def _parse_rule(self, is_top_rule):
        if is_top_rule:
            if self.top_level_rule_idx is not None:
                raise SyntaxError(
                    "Redefinition of top level rule on line {}, column {}".format(
                        self.current_token.line, self.current_token.col))
            self._accept('EXCL')
        (name, params) = self._parse_rule_name()

        if name in self.symbols:
            raise SyntaxError('Redefinition of symbol {} on line {}'.format(
                name, self.current_token.line))

        self._log('Found rule name: ' + repr(name))
        self._accept('COLON')
        body = self._parse_rule_body()
        self.symbols.append(name)
        return Rule(name, params, body[0], body[1], body[2])

    def _parse_rule_body(self):
        t = self.current_token
        begin = end = None
        if t.typ == 'begin':
            begin = self._parse_python_block('begin')
            self._next()
            self._log('Found begin block:\n' + begin)
        choices = self._parse_expansion_block()
        t = self.current_token
        if t.typ == 'end':
            end = self._parse_python_block('end')
            self._log('Found end block:\n' + end)
        return (choices, begin, end)

    def _parse_python_block(self, block_name):
        self._accept(block_name)
        self._accept('COLON')
        self._expect('PYTHON_CODE')
        return self.current_token.value

    def _parse_expansion_block(self):
        self._accept('expansion')
        self._accept('COLON')
        choices = self._parse_exp_choices()
        self._log('Found expansion choices: ' + repr(choices))
        return choices

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
        value = None
        params = None
        term_typ = None
        if self.next_token.typ == 'EQUALS':
            assignment = self._accept('ID')
            self._next()
        t = self.current_token
        if t.typ == 'SINGLE_QUOTED' or t.typ == 'DOUBLE_QUOTED':
            term_typ = 'Terminal'
            value = self._parse_terminal()
            self._next()
        elif t.typ == 'ID':
            term_typ = 'Variable'
            if self.next_token.typ == 'LPAREN':
                rule = self._parse_rule_name()
                value = '%s' % rule[0]
                params = rule[1]
            else:
                token = self._accept('ID')
                value = '%s' % token
        else:
            raise SyntaxError(
                "Expected symbol 'TERMINAL', \"REGEX\", TOKEN NAME or RULE NAME, got {} on line {}, column {}".format(
                    t.typ, t.line, t.col))
        return Term(assignment, value, term_typ, params)

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
            raise SyntaxError(
                "Expected symbol ')' or a parameter, got {} on line {}, column {}".format(
                    t.typ, t.line, t.col))
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
            typ = 'Literal'
        elif t.typ == 'DOUBLE_QUOTED':
            typ = 'Regex'
        else:
            raise SyntaxError(
                "Expected symbol 'LITERAL' or \"REGEX\", got {} on line {}, column {}".format(
                    t.typ, t.line, t.col))
        return Terminal(typ, t.value[1:-1])

    def _next(self):
        self.current_token, self.next_token = self.next_token, next(
            self.tokens, None)
        return self.current_token

    def _expect(self, typ):
        t = self.current_token
        if t.typ != typ:
            raise SyntaxError(
                "Expected symbol {}, got {} on line {}, column {}".format(
                    typ, t.typ, t.line, t.col))

    def _accept(self, typ):
        self._expect(typ)
        val = self.current_token.value
        self._next()
        return val

    def _generate_output(self, output_path):
        with open(output_path, mode='w') as output:
            self._write_header(output)

            for token in self.terminal_rules:
                self._write_token(output, token)

            for rule in self.variable_rules:
                self._write_rule(output, rule)

            top_rule = self.variable_rules[self.top_level_rule_idx]
            output.write('grammar.top_rule = {}\n'.format(top_rule.name))

    def _write_header(self, output):
        output.write(
            'from parse.grammar import Grammar, Terminal, Variable, Rule, Production\n')
        output.write('grammar = Grammar()\n')

    def _write_token(self, output, token):
        name, product = token
        for term in product:
            value = term.value if term.typ == 'Regex' else re.escape(term.value)
            output.write(
                "{} = Rule(Variable('{}'), Production(Terminal('{}')))\n".format(
                    name, name, value))
            self._write_token_function(output, name)
            output.write('grammar.add_rule(%s)\n' % name)

    def _write_token_function(self, output, name):
        id = self._next_id()
        output.write("def {}_{}_fn(node):\n".format(name, id))
        output.write("    return node.children[0].data.value\n\n")
        output.write("{}.fn = {}_{}_fn\n\n".format(name, name, id))

    def _write_rule(self, output, rule):
        name = rule.name

        def get_value(term):
            if term.typ == 'Variable':
                return term.value
            terminal = term.value
            if terminal.typ == 'Regex':
                return terminal.value
            return re.escape(terminal.value)

        for prod in rule.choices:
            prod_str = ', '.join("{}('{}')".format(
                term.typ, get_value(term)) for term in prod)
            output.write("{} = Rule(Variable('{}'), Production({}))\n".format(
                name, name, prod_str))
            self._write_rule_prod(
                output, name, rule.params, prod, rule.begin, rule.end)
            output.write('grammar.add_rule({})\n'.format(name))

    def _write_rule_prod(self, output, name, params, prod, begin, end):
        rule_params = ['node']
        if params:
            rule_params.extend(params)
        params_str = ','.join(rule_params)
        id = self._next_id()
        output.write('def {}_{}_fn({}):\n'.format(name, id, params_str))

        if begin:
            output.write(begin + '\n')

        # TODO: what if begin and end have different indents?
        # Could be a SyntaxError?
        base_indent = ''
        if begin:
            base_indent = self._parse_whitespace(begin, 0)
        elif end:
            base_indent = self._parse_whitespace(end, 0)
        self._write_rule_choice(output, prod, base_indent)

        if end:
            output.write(end + '\n')

        output.write('{}.fn = {}_{}_fn\n\n'.format(name, name, id))

    def _write_rule_choice(self, output, prod, base_indent):
        for idx, term in enumerate(prod):
            if term.typ == 'Variable':
                var = 'node.children[{}]'.format(idx)
                params = [var]
                if term.params:
                    params.extend(term.params)
                params_str = ','.join(params)

                if term[0] is not None:
                    assign = '{} = '.format(term[0])
                else:
                    assign = ''
                output.write('{}{}{}.fn({})\n'.format(
                    base_indent, assign, var, params_str))

    def _next_id(self):
        self.rule_id += 1
        return self.rule_id

    def _log(self, message):
        if self.log:
            print(message)


def main():
    import sys
    if len(sys.argv) != 3:
        print('Usage:')
        print('metagrammar.py <grammar_file> <generate_file>')
        return
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    print('Process {} {}'.format(input_file, output_file))

    mg = Metagrammar()
    mg.process_grammar(input_file, output_file)

    # Testing
    # import importlib
    # from earley import Parser

    # module = importlib.import_module('this')
    # g = module.grammar

    # print('------------CREATED GRAMMAR------------')
    # # print('Delim option: ' + g.delim)
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
    # # print(repr(parser.tokens))
    # for r in res:
    #     r.print()
    #     # print('Walking')
    #     r.walk()


if __name__ == '__main__':
    main()
