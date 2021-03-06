import re


class Terminal(object):
    """docstring for Terminal"""

    def __init__(self, matcher_text):
        self.value = None
        self.matcher_text = matcher_text

    def __eq__(self, other):
        if not isinstance(other, Terminal):
            return False
        return self.matcher_text == other.matcher_text

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.matcher_text)

    def __repr__(self):
        if self.value:
            return "%s" % self.value
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
        # terms are variables or terminals
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


class Grammar(object):
    """docstring for Grammar"""

    def __init__(self, top_rule=None):
        self.top_rule = top_rule
        self.rules = set()
        self.terminals = set()
        self.terminal_map = {}

    def __iter__(self):
        return iter(self.rules)

    def add_rule(self, rule):
        # print(repr(rule))
        self.rules.add(rule)
        if self.top_rule is None:
            self.top_rule = rule
        for term in rule.production.terms:
            if not isinstance(term, Variable):
                if rule.variable.name in self.terminal_map:
                    val = self.terminal_map[rule.variable.name]
                    self.terminal_map[rule.variable.name] = '%s|%s' % (
                        val, term)
                else:
                    # TODO: "ORing" terms with the same variable
                    self.terminal_map[rule.variable.name] = term
                self.terminals.add(term)

    def is_terminal(self, token):
        return token in self.terminals
