from grammar import Term, Variable, Rule, Production

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

    def parse_rule(self, var_name, val, fn_enter=None, fn_exit=None):
        variable = self.grammar.variables.setdefault(var_name, Variable(var_name))
        rules = val.split('|')
        for rule in rules:
            terms = rule.split()
            term_list = []
            for term in terms:
                if term[0] == '\'' and term[-1] == '\'':
                    term_list.append(Term(term.strip('\'')))
                else:
                    var = self.grammar.variables.setdefault(term, Variable(term))
                    term_list.append(var)
            self.grammar.add_rule(Rule(variable, Production(*term_list)), fn_enter, fn_exit)

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
        for line in file:
            self.parse_line(line)