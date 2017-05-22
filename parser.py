import copy

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

class FloatTerm(object):
    index = 0
    def __init__(self):
        self.val = None
        FloatTerm.index = FloatTerm.index + 1
    def __eq__(self, other):
        if isinstance(other, str):
            try:
                self.val = float(other)
                return True
            except ValueError:
                return False
        elif isinstance(other, FloatTerm):
            return self.index == other.index
        return False
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(__class__.__name__)
    def __repr__(self):
        if self.val:
            return str(self.val)
        else:
            return __class__.__name__

class StringTerm(object):
    index = 0
    def __init__(self):
        self.val = None
        StringTerm.index = StringTerm.index + 1
        self.index = StringTerm.index
    def __eq__(self, other):
        if isinstance(other, str):
            try:
                float(other)
                return False
            except ValueError:
                self.val = str(other)
                return True
        elif isinstance(other, StringTerm):
            return self.index == other.index
        return False
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((__class__.__name__, self.index))
    def __repr__(self):
        if self.val:
            return str(self.val)
        else:
            return __class__.__name__

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
        return "%d %-1s -> %-8s [%s-%s] [%-s]" % (self.index, self.rule.variable, " ".join(terms), self.orig_pos, self.end_pos, pointers)
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

class EarleyParser(object):
    """docstring for EarleyParser"""
    def __init__(self, topRule):
        self.topRule = topRule
        self.grammar = set()
        self.terminals = set()

    def add(self, rule):
        self.grammar.add(rule)
        for term in rule.production.terms:
            if not isinstance(term, Variable):
                self.terminals.add(term)

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
        self.state_list[0].add(State(self.topRule, 0, 0, 0))
        for k in range(len(self.tokens)+1):
            print("\nk = %d" % k)
            active = set(self.state_list[k])
            seen = set(self.state_list[k])
            while active:
                for state in active:
                    if not state.finished():
                        if not self.is_terminal(state.next()):
                            self.predict(state, k)
                        else:
                            self.scan(state, k)
                    else:
                        self.complete(state, k)
                seen |= active
                active = self.state_list[k]-seen
            print()
            for state in self.state_list[k]:
                print(state)
        print("\nFinal completed states")
        for st in self.state_list[-1]:
            if st.rule == self.topRule:
                print(st)
                self.print_state_tree(st)
                print()
        # print("\nChoosen:")
        # for st in self.state_list[-1]:
        #     if st.rule == self.topRule:
        #         e = st
        #         break
        # if self.state_list[-1]:
        #     self.print_state_tree(e)
        #     return e

    def is_terminal(self, token):
        return token in self.terminals

    def predict(self, state, k):
        for rule in self.grammar:
            if state.next() == rule.variable:
                self.state_list[k].add(State(rule, 0, k, k))

    def scan(self, state, k):
        if k >= len(self.tokens):
            return
        if state.next() == self.tokens[k]:
            self.state_list[k+1].add(State(copy.deepcopy(state.rule), state.dotPos+1, state.orig_pos, k+1, state.back_pointers))


    def complete(self, state, k):
        for s in self.state_list[state.orig_pos]:
            if s.next() == state.rule.variable:
                newState = State(s.rule, s.dotPos+1, s.orig_pos, k, s.back_pointers)
                newState.back_pointers.append(state)
                self.state_list[k].add(newState)

    def print_state_tree(self, state, level=0):
        j = 0
        for i in range(len(state.rule.production)):
            text = "\t"*level+str(state.rule.production[i])
            print(text)
            if state.back_pointers:
                if not self.is_terminal(state.rule.production[i]):
                    self.print_state_tree(state.back_pointers[j], level+1)
                    j += 1


P = Variable("P")
S = Variable("S")
M = Variable("M")
T = Variable("T")

parser = EarleyParser(Rule(P, Production(S)))

parser.add(Rule(S, Production(S, '+', M)))
parser.add(Rule(S, Production(M)))
parser.add(Rule(M, Production(M, '*', T)))
parser.add(Rule(M, Production(T)))
parser.add(Rule(T, Production('1')))
parser.add(Rule(T, Production('2')))
parser.add(Rule(T, Production('3')))
parser.add(Rule(T, Production('4')))

parser.parse("2 + 3 * 4")