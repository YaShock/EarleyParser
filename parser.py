import copy
import re

class Term(object):
    """docstring for Term"""
    def __init__(self, matcher_text):
        self.value = None
        self.matcher_text = matcher_text
    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self.matcher_text == other.matcher_text
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.matcher_text)
    def __repr__(self):
        if self.value:
            return "\'%s\'" % self.value
        else:
            return self.matcher_text
    def part_of(self, token):
        if re.match(self.matcher_text, token):
            self.value = token
            return True
        return False    

class Variable(object):
    """docstring for Variable"""
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.name)

class Rule(object):
    """docstring for Rule"""
    def __init__(self, variable, production):
        self.variable = variable
        self.production = production
    def __repr__(self):
        return "%s -> %s" % (self.variable.name, repr(self.production))
    def __eq__(self, other):
        return (self.variable, self.production) == (other.variable, other.production)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.variable, self.production))

class Production(object):
    """docstring for Production"""
    def __init__(self, *terms):
        #terms are variables or terminals
        self.terms = terms
    def __repr__(self):
        return " ".join(str(t) for t in self.terms)
    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.terms)
    def __len__(self):
        return len(self.terms)
    def __iter__(self):
        return iter(self.terms)
    def __getitem__(self, index):
        return self.terms[index]

class State(object):
    """docstring for State"""
    num = 0
    def __init__(self, rule, dotPos, orig_pos, end_pos, back_pointers=[]):
        self.index = State.num
        State.num += 1
        self.rule = rule
        self.dotPos = dotPos
        self.orig_pos = orig_pos
        self.end_pos = end_pos
        self.back_pointers = list(back_pointers)
    def __repr__(self):
        terms = [str(p) for p in self.rule.production]
        terms.insert(self.dotPos, u"$")
        pointers = " ".join(str(i.index) for i in self.back_pointers)
        return "%d. %-1s -> %-8s [%s-%s] [%-s]" % (self.index, self.rule.variable, " ".join(terms), self.orig_pos, self.end_pos, pointers)
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.rule, self.dotPos, self.orig_pos, self.back_pointers) == (other.rule, other.dotPos, other.orig_pos, other.back_pointers)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.rule, self.dotPos, self.orig_pos))
    def finished(self):
        return self.dotPos >= len(self.rule.production)
    def next(self):
        if self.finished():
            return None
        return self.rule.production[self.dotPos]

class Tree(object):
    def __init__(self, data=None, children=None):
        self.children = []
        if children is not None:
            self.children.extend(children)
        self.data = data
    def add(self, child):
        self.children.append(child)
    def print(self, level=0):
        text = "\t"*level+str(self.data)
        print(text)
        for child in self.children:
            child.print(level+1)

class Grammar(object):
    """docstring for Grammar"""
    def __init__(self, topRule=None):
        self.topRule = topRule
        self.rules = set()
        self.terminals = set()
        self.variables = {}

    def __iter__(self):
        return iter(self.rules)

    def add_rule(self, rule):
        self.rules.add(rule)
        if self.topRule is None:
            self.topRule = rule
        for term in rule.production.terms:
            if not isinstance(term, Variable):
                self.terminals.add(term)

    def is_terminal(self, token):
        return token in self.terminals

    def read_file(self, file):
        for line in file:
            self.parse_rule(line)

    def parse_rule(self, line):
        lst = []
        if ' -> ' in line:
            lst = line.split(' -> ')
        else:
            lst = line.split('->')
        if len(lst) != 2:
            raise ValueError('Invalid rule syntax: ->')
        if ' ' in line[0]:
            raise ValueError('Invalid rule syntax: space in the variable name')
        var_name = lst[0].strip()
        variable = self.variables.setdefault(var_name, Variable(var_name))
        rules = lst[1].split('|')
        for rule in rules:
            terms = rule.split()
            term_list = []
            for term in terms:
                if term[0] == '\'' and term[-1] == '\'':
                    term_list.append(Term(term.strip('\'')))
                else:
                    var = self.variables.setdefault(term, Variable(term))
                    term_list.append(var)
            self.add_rule(Rule(variable, Production(*term_list)))

class EarleyParser(object):
    """docstring for EarleyParser"""
    def __init__(self, grammar):
        self.grammar = grammar

    def __init_states(self, text):
        self.state_list = []
        self.text = text
        for k in range(len(self.tokens)+1):
            self.state_list.append(set())

    def tokenize(self, text):
        self.tokens = text.split(' ')

    def parse(self, text):
        self.tokenize(text)
        self.__init_states(text)
        self.state_list[0].add(State(self.grammar.topRule, 0, 0, 0))
        for k in range(len(self.tokens)+1):
            #print("\nk = %d" % k)
            active = set(self.state_list[k])
            seen = set(self.state_list[k])
            while active:
                for state in active:
                    if not state.finished():
                        if not self.grammar.is_terminal(state.next()):
                            self.predict(state, k)
                        else:
                            self.scan(state, k)
                    else:
                        self.complete(state, k)
                seen |= active
                active = self.state_list[k]-seen
            # print()
            # for state in self.state_list[k]:
            #     print(state)
        result = []
        for st in self.state_list[-1]:
            if st.rule == self.grammar.topRule:
                result.append(self.construct_tree(st))
        return result

    def predict(self, state, k):
        for rule in self.grammar:
            if state.next() == rule.variable:
                self.state_list[k].add(State(rule, 0, k, k))

    def scan(self, state, k):
        if k >= len(self.tokens):
            return
        if state.next().part_of(self.tokens[k]):
            self.state_list[k+1].add(State(copy.deepcopy(state.rule), state.dotPos+1, state.orig_pos, k+1, state.back_pointers))

    def complete(self, state, k):
        for s in self.state_list[state.orig_pos]:
            if s.next() == state.rule.variable:
                newState = State(s.rule, s.dotPos+1, s.orig_pos, k, s.back_pointers)
                newState.back_pointers.append(state)
                self.state_list[k].add(newState)

    def construct_tree(self, state, level=0):
        tree = Tree()
        tree.data = repr(state.rule.variable)
        j = 0
        for i in range(len(state.rule.production)):
            node = Tree()
            if state.back_pointers:
                if not self.grammar.is_terminal(state.rule.production[i]):
                    node = self.construct_tree(state.back_pointers[j], level+1)
                    j += 1
            node.data = repr(state.rule.production[i])
            tree.add(node)
        return tree

grammar = Grammar()
file = open('cf.txt')
grammar.read_file(file)

parser = EarleyParser(grammar)

# for rule in grammar.rules:
#     print(rule)

lst = parser.parse('load whatever')
for t in lst:
    t.print()

lst = parser.parse("get terms frequency between 1.5 and 4.8")
for t in lst:
    t.print()

lst = parser.parse("delete words : lel sdjfhslhsljgk")
for t in lst:
    t.print()