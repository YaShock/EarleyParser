from grammar import Term, Variable, Rule, Production
import string
import re

def contains_whitespace(s):
    return any([c in s for c in string.whitespace])

class ContextBuilder(object):
    """docstring for ContextBuilder"""
    def __init__(self, grammar):
        self.grammar = grammar

    def parse_line(self, line):
        if line[0] == '/' and line[1] == '/':
            return
        lst = line.split('->')
        if len(lst) != 2:
            raise ValueError('Invalid rule syntax: ->')
        if contains_whitespace(line[0]):
            raise ValueError('Invalid rule syntax: whitespace in the variable')
        var_name = lst[0].strip()
        if var_name[0] == '<' and var_name[-1] == '>':
            self.parse_option(var_name.strip('<>'), lst[1])
        else:
            self.parse_rule(var_name, lst[1])

    def parse_rule(self, var_name, val):
        lst = val.split('::=')
        if len(lst) > 2:
            raise ValueError('Invalid rule syntax: more than one ::=')
        elif len(lst) == 2:
            fn = lst[1].strip()
            fn_enter = fn + '_enter'
            fn_exit = fn + '_exit'
        else:
            fn_enter = None
            fn_exit = None
            
        variable = self.grammar.variables.setdefault(var_name, Variable(var_name))
        rules = lst[0].split('|')
        for rule in rules:
            terms = rule.split()
            term_list = []
            for term in terms:
                if term[0] == '\"' and term[-1] == '\"':
                    term_list.append(Term(term.strip('\"')))
                elif term[0] == '\'' and term[-1] == '\'':
                    term_list.append(Term(re.escape(term.strip('\''))))
                else:
                    var = self.grammar.variables.setdefault(term, Variable(term))
                    term_list.append(var)
            r = Rule(variable, Production(*term_list))
            self.grammar.add_rule(r)
            self.generated_file.write('    dict[%i] = (semantics.%s, semantics.%s)\n' % (id(r), fn_enter, fn_exit))

    def parse_option(self, var_name, val):
        val = val.strip()
        if val[0] != '\'' or val[-1] != '\'':
            raise ValueError('Invalid option syntax: the value must be enclosed in \'')
        val = val.strip('\'')
        if var_name == 'delim':
            self.grammar.delim = val
        else:
            raise ValueError('Invalid option syntax: unknown option name')

    def read_file(self, file):
        self.generated_file = open('generated.py', 'w')
        self.generated_file.write('import semantics\n')
        self.generated_file.write('dict = {}\n')
        self.generated_file.write('def create():\n')
        for line in file:
            self.parse_line(line)
        self.generated_file.close()