from .grammar import Term, Variable, Rule, Production
import importlib
import string
import re

def contains_whitespace(s):
    return any([c in s for c in string.whitespace])

class ContextBuilder(object):
    """docstring for ContextBuilder"""
    def __init__(self, grammar):
        self.grammar = grammar

    def parse_line(self, line):
        if (line[0] == '/' and line[1] == '/') or line.isspace():
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
            fn_enter = 'semantics.' + fn + '_enter'
            fn_exit = 'semantics.' + fn + '_exit'
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
            self.generated_file.write('    dict[%i] = (%s, %s)\n' % (id(r), fn_enter, fn_exit))

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
        self.generated_file = open('./generated/generated.py', 'w')
        self.generated_file.write('from . import semantics\n')
        self.generated_file.write('dict = {}\n')
        self.generated_file.write('def create():\n')
        for line in file:
            self.parse_line(line)
        self.generated_file.close()

    def build(self):
        file = open('generated/grammar.cf')
        self.read_file(file)
        file.close()
        module = importlib.import_module('generated.generated')
        module.create()
        for rule in self.grammar.rules:
            d = module.dict[id(rule)]
            rule.fn_enter = d[0]
            rule.fn_exit = d[1]

def walk_tree(tree):
    if tree.fn_enter:
        tree.fn_enter(tree)
    for child in tree.children:
        walk_tree(child)
    if tree.fn_exit:
        tree.fn_exit(tree)